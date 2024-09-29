import hashlib
import json
from textwrap import dedent
from urllib.parse import urlparse
from time import time 
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain:
    # A classe "Blockchain" é responsável por cuidar da "corrente"; Ela vai salvar as transações
    # e ter alguns metodos pra poder adicionar novos blocos na "corrente".
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.current_transactions = []
        
        # cria o bloco inicial
        self.new_block(previous_hash=1, proof=100)
        
    def register_node(self, adress):
        """
        Adiciona um novo node pra lista de nodes
        :param adress: <str> Endereço do Node. Eg. 'http://92.168.0.5:5000'
        :return: Noada
        """
        
        parsed_url = urlparse(adress)
        self.nodes.add(parsed_url.netloc)
        
    def valid_chain(self, chain):
        """
        Determina se dado Blockchain é válido
        :param chain: <list> Blockchain
        :return <bool> True se válido, False se não
        """
        
        last_block = chain[0]
        current_index = 1
        
        while current_index <len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # checa se a proof of work ta correta
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
            
        return True
    
    def resolve_conflicts(self):
        """
        Esse é o consenso do algoritmo, resolve os conflitos
        trocando a chain pela a mais longa na rede
        :return: <bool> True if our chain was replaced, False if not 
        """
        
        neighbours = self.nodes
        new_chain = None
        
        # Procurando apenas pelas correntes maiores que a atual
        max_lenght = len(self.chain)
        
        # Pega e verifica as correntes de todos os nodes na rede
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            
            if response.status_code == 200:
                lenght = response.json()['lenght']
                chain = response.json()['chain']
                
                # checa se o tamanho é maior e se a corrente é válida
                if lenght > max_lenght and self.valid_chain(chain):
                    max_lenght = lenght
                    new_chain = chain
        # Troca a corrente se a gente descobriu uma nova corrente maior que a anterior
        if new_chain:
            self.chain = new_chain
            return True
        return False
    
           
    def new_block(self, proof, previous_hash=None):
        # cria um novo bloco e adiciona ele adiciona ele na chain
        """
        Cria um novo Bloco na Blockchain
        :param proof: <int> A prova dada pelo algorítimo de trabalho
        :param previous_hash: (opicional) <str> Hash do bloco anterior
        :return: <dict> Novo Bloco
        """
        
        block = {
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        
        # Reseta a atual lista de transações
        self.current_transactions = []
        
        self.chain.append(block)
        return block
    
    
    def new_transaction(self, sender, recipient, amount):
        # adiciona uma nova transação apra a lista de transações
        """
        Cria uma nova transação para o próximo bloco mineirado.
        :param sender: <str> Endereço do enviante (Sender)
        :param recipient: <str> Endereço do recipiente
        :param amount: <int> Quantidade (Amount)
        :return: <int> Indexação do bloco que vai se atuar na transação
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
    
        return self.last_block['index'] + 1
        # Agora, a "new_transaction()" adiciona uma transação para a lista da transação
        # enquanto retorna o valor do bloco indexado que vai ser adicionado para a tran-
        # sação seguinte a ser minerada
        
        
    @property
    def last_block(self):
        return self.chain[-1]
    
    
    @staticmethod
    def hash(block):
        # faz o que ta escrito na definição né.
        """
        Cria um hash SHA-256 de um bloco(?)
        :param block: <dict> Block
        :return: <str> 
        """
        
        # tem que prestar atenção pra ver se o dicionario é solicitado
        # ou vão ser hashes inconsistentes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def proof_of_work(self, last_proof):
        """
        Algorítmo simples de prova de trabalho:
        - encontra um número p' tanto quanto hash(pp') contenha 4 zeros na frente,
        onde p é o p' anterior.
        - p é a prova de trabalho anterior, e p' é a nova prova
        :param last_proof: <int>
        :return: <int>
        """
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
            
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Valida a prova: Hash(last_proof, proof) contém 4 zeros na frente?
        :param last_proof: <int> Prova anterior
        :param proof: <int> Prova anterior
        :return: <bool> True se for correto, False se não for.
        """
        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    # Usei so 4 zeros pra não dificultar o interpretação do algorítmo, zero portanto é
    # suficiente, já que 1 zero muda totalmente o tempo pra encontrar a solução
    # classe ta quase completa, falta pouco pra interagir com os requests de HTTP 
    # MUAHAHAHAHAHHAAHDAHUSIDHOHBO I! YIYASDA
    
# instancia o Node
app = Flask(__name__)
    
# Gera um endereço global único pra esse node
node_identifier = str(uuid4()).replace('-', '')
    
    # Instancia o Blockchain
blockchain = Blockchain()
    
@app.route('/mine', methods=['GET'])
def mine():
    # vamos rodar o algoritimo da prova de trabalho pra poder pegar 
    # a próxima prova.
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
        
    # O programa precisa receber uma recompensa por ter achado a prova.
    # O enviante é 0 significando que esse node mineirou uma nova coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
        
    # Cria o novo Bloco adicionado ele pra corrente
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
        
    response = {
        'message': "Novo bloco criado",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
        
    
    
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
        
    # checa se os campos requiridos estão no POST data]
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
        
     # cria uma nova transação
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        
    response = {'message': f'A transação vai ser adicionada ao Bloco {index}'}
    return jsonify(response), 201
    
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    
    @property
    def last_block(self):
        # retorna o ultimo bloco na corrente
        pass
    
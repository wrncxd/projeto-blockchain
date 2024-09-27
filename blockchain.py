import hashlib
import json

from time import time 
from uuid import uuid4


class Blockchain(object): 
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    def new_block(self):
        """
        Cria um novo bloco na BlockChain
        :param proof: <int> A prova dada pela prova de trabalho do algoritimo
        :param previous_hash: (Opicional) <str> Hash do bloco anterior
        :return: <dict> Novo bloco.
        """
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            
        }
        # Reseta a linha atual de transações
        self.current_transactions: []
        
        self.chain.append(block)
        return block
    
    def new_transaction(self):
        # adiciona uma nova transação para a lista de transações
        """
        Crea uma nova transação para ir para o proximo bloco buscado
        :param sender: <str> Endereço do Enviante (Sender)
        :param recipient: <str> Endereço do recebedor
        :param amount: <int> Quantidade transferida
        :return: <int> O valor indexo do bloco que vai na transação"""
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        return self.last.block['index'] + 1
    
    def proof_of_work(self, last_proof):
        """
        Prova simples de algoritimo de trabalho
         - encontre um numero p' que tanto quanto hash(pp') contenha 4 zeros no começo,
         onde p é o antigo p'
         - p é a antiga prova, e p' é a nova prova
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
        Válida a prova: Hash tem 4 zeros iniciais?(last_proof, proof)
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    
    
    def hash(block):
        # da um hash em um bloco
        """
        Cria um SHA-256 hash de um bloco
        :param block: <dict> Bloco
        :return: <str>
        """
        
        # tem que prestar atenção para que o diciionario seja chamado, se nao vao ser hashes inconsistentes 
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        # retorna o ultimo bloco na corrente
        return self.chain[-1]
    
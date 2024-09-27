def Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    def new_block(self):
        # cria um novo bloco e adiciona ele pra corrente
        block = {
            'index': 1
            'timestamp': 1506057125.900785
            'transactions':´[
                {
                    'sender': "8527147fe1f5426f9dd545de4b27ee00"
                    'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f"
                    'amount': 5,
                }
            ], 
            'proof': 324984774000
            'previus_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        }
    
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
    
    
    @staticmethod
    def hash(block):
        # da um hash em um bloco
        pass
    
    @property
    def last_block(self):
        # retorna o ultimo bloco na corrente
        pass
    
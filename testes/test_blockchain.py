import hashlib
import json
from unittest import TestCase

from blockchain import Blockchain


class BlockchainTestCase(TestCase):
    
    def setUp(self):
        self.blockchain = Blockchain()
        
    
    def create_block(self, proof=123, previous_hash='abc'):
        self.blockchain.new_block(proof, previous_hash)
        
    def create_transactions(self, sender='a', recipient='b', amount=1):
        self.blockchain.new_transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
        )
        
        
class TestRegisterNodes(BlockchainTestCase):
    
    def test_valid_nodes(self):
        blockchain = Blockchain()
        
        blockchain.register_node('http://192.168.0.1:5000')
        
        self.assertIn('192.168.0.1:5000', blockchain.nodes)
        
    def test_malformed_nodes(self):
        blockchain = Blockchain()
        
        blockchain.register_node('http://192.168.0.1:5000')
        
        self.assertNotIn('http://192.168.0.1:5000', blockchain.nodes)
        
    def test_idempotency(self):
        blockchain = Blockchain()
        
        blockchain.register_node('http://192.168.0.1:5000')
        blockchain.register_node('http://192.168.0.1:5000')
        
        assert len(blockchain.nodes) == 1
        

class TestBlocksAndTransactions(BlockchainTestCase):
    
    def test_block_creation(self):
        self.create_block()
        
        latest_block = self.blockchain.last_block
        
        # o bloco genesis é criado na inialização, então a nossa length tem que ser 2
        assert len(self.blockchain.chain) == 2
        assert latest_block['index'] == 2
        assert latest_block['timestamp'] is not None
        assert latest_block['proof'] == 123
        assert latest_block['previous_hash'] == 'abc'
    
    
    def test_create_transaction(self):
        self.create_transactions()
        
        transaction = self.blockchain.current_transactions[-1]
        
        assert transaction
        assert transaction['sender'] == 'a'
        assert transaction['recipient'] == 'b'
        assert transaction['previous_hash'] == 1
        
    def test_block_resets_transactions(self):
        self.create_transactions()
        
        initial_lenght = len(self.blockchain.current_transactions)
        
        self.create_block()
        
        current_lenght = len(self.blockchain.current_transactions)
        
        assert initial_lenght == 1
        assert current_lenght == 0
        
    def test_return_last_block(self):
        self.create_block()
        
        created_block = self.blockchain.last_block
        
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertIs(created_block, self.blockchain.chain[-1])
        

class TestHashingAndProofs(BlockchainTestCase):
    
    def test_hash_is_correct(self):
        self.create_block()
        
        new_block = self.blockchain.last_block
        new_block_json = json.dumps(self.blockchain.last_block, sort_keys=True).encode()
        new_hash = hashlib.sha256(new_block_json).hexdigest()
        
        # Testa se o hash gerado tem o comprimento correto e é igual ao hash calculado.
        assert len(new_hash) == 64
        assert new_hash == self.blockchain.hash(new_block)
    
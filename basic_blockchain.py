### Create a Blockchain ###

# Import Libraries

import datetime
import threading
import time
import hashlib
import json
from flask import Flask, jsonify, request

### Build Blockchain
class User:
    def __init__(self, username): 
        self.username = username
        self.vault = 1000

    def vault_add(self, amount):
        self.vault += amount

    def vault_subtract(self, amount):
        if self.vault >= amount:
            self.vault -= amount
            return True
        return False
    
    def to_dict(self):
        return {
            'username': self.username,
            'vault': self.vault
        }
        
users = {}        

#Printer Accounts
SecretPrinter = User("SecretPrinter")
users["SecretPrinter"] = SecretPrinter
SecretPrinter.vault_add(100)

def add_coins_periodically():
    while True:
        time.sleep(30) 
        SecretPrinter.vault_add(50)
        print(f"Added 50 coins to SecretPrinter. Current balance: {SecretPrinter.vault}")

thread = threading.Thread(target=add_coins_periodically)
thread.daemon = True  
thread.start()
        
class Transaction:
    def __init__(self, sender: User, receiver: User, amount: float): 
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def execute(self):
        if self.sender.vault_subtract(self.amount):
            self.receiver.vault_add(self.amount)
            return True
        return False

    def to_dict(self):
        return {
            'sender': self.sender.to_dict(),
            'receiver': self.receiver.to_dict(),
            'amount': self.amount
        }




class Blockchain: 
    
    def __init__(self): 
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash='0', transactions=[])
        
    def create_block(self, proof, previous_hash, transactions): 
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': transactions}
        self.chain.append(block)
        return block
    
    def add_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction.to_dict())
        
    def get_previous_block(self): 
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof): 
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else: 
                new_proof += 1
        return new_proof
    
    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

### Mine Blockchain

# Create Web App
app = Flask(__name__)

# Create Blockchain
blockchain = Blockchain()

# Mine a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    pending_transactions = blockchain.pending_transactions
    block = blockchain.create_block(proof, previous_hash, pending_transactions)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': pending_transactions}
    
    blockchain.pending_transactions = []
    
    return jsonify(response), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.get_json()
    username = user_data.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    if username in users:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username)
    users[username] = new_user

    return jsonify({'message': f'User {username} created successfully'}), 200



@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    
    sender_username = json['sender']
    receiver_username = json['receiver']

    if sender_username not in users:
        return jsonify({'message': 'Transaction failed'}), 400

    if receiver_username not in users:
        return jsonify({'message': 'Transaction failed'}), 400

    sender = users[sender_username]
    receiver = users[receiver_username]
    amount = json['amount']
    transaction = Transaction(sender, receiver, amount)
    if transaction.execute():
        blockchain.add_transaction(transaction)
        return jsonify({'message': 'Transaction will be added to Block'}), 200
    else:
        return jsonify({'message': 'Transaction failed'}), 400

# Get a full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        block_copy = block.copy()
        block_copy['transactions'] = block['transactions']
        chain_data.append(block_copy)

    response = {'chain': chain_data, 'length': len(chain_data)}
    return jsonify(response), 200


# Confirm chain is valid
@app.route('/confirm_chain', methods = ['GET'])
def confirm_chain():
    response = {'valid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200






# Run app
app.run(host = '0.0.0.0', port = 5070)
    



    





from datetime import datetime
import hashlib
import json
from flask import Flask, jsonify, request


class Blockchain:
    __leading_zeros = 5

    def __init__(self):
        self.chain = []
        self.transaction_pool = []
        self.completed_transactions = []
        self.users = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        self.satoshi()
        nonce, hash, seconds = self.mine()
        print(f"Genesis block mined in {seconds} seconds.")
        self.create_block(nonce, hash)

    def satoshi(self):
        self.create_user('God')
        self.create_user('Satoshi')
        self.users['God']['balance'] += 1000
        transaction = {'sender': 'God',
                       'receiver': 'Satoshi',
                       'amount': 1000,
                       'timestamp': str(datetime.now())}
        self.transaction_pool.append(transaction)

    def create_block(self, nonce, hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.now()),
                 'nonce': nonce,
                 'transactions': self.transaction_pool,
                 'previous_hash': self.hash(self.get_previous_block()),
                 'hash': hash
                 }
        self.chain.append(block)
        self.complete_transactions()
        return block

    def create_user(self, name):
        self.users[name] = {
            'balance': 0,
            'transactions': [],
        }

    def complete_transactions(self):
        for t in self.transaction_pool:
            self.users[t['sender']]['transactions'].append(t)
            self.users[t['receiver']]['transactions'].append(t)
            self.users[t['sender']]['balance'] -= t['amount']
            self.users[t['receiver']]['balance'] += t['amount']
        self.completed_transactions.append(self.transaction_pool)
        self.transaction_pool = []

    def get_previous_block(self):
        if len(self.chain) == 0:
            return {}
        return self.chain[-1]

    def mine(self):
        start = datetime.now()
        nonce = 1
        previous_hash = self.hash(self.get_previous_block())
        static_hash_input = str(self.transaction_pool) + previous_hash
        while True:
            hash_input = f"{nonce}{static_hash_input}"
            hash = hashlib.sha256(hash_input.encode()).hexdigest()
            if hash.startswith('0' * self.__leading_zeros):
                break
            nonce += 1
        seconds = (datetime.now() - start).total_seconds()
        print(f"Block mined in {seconds} seconds.")
        return nonce, hash, seconds

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def validate_chain(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if self.hash(previous_block) != block['previous_hash']:
                return False
            hash_input = f"{block['nonce']}{str(block['transactions'])}{self.hash(previous_block)}"
            hash = hashlib.sha256(hash_input.encode()).hexdigest()
            if hash[:self.__leading_zeros] != '0' * self.__leading_zeros or hash != block['hash']:
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction_to_pool(self, sender, receiver, amount):
        transaction = {'sender': sender,
                       'receiver': receiver,
                       'amount': amount,
                       'timestamp': str(datetime.now())}
        if not self.validate_transaction(transaction):
            return False, 'Invalid transaction. Transaction not added to pool.'
        self.transaction_pool.append(transaction)
        return True, f"Transaction added to pool and will be included in Block {blockchain.get_previous_block()['index'] + 1}"

    def validate_transaction(self, transaction):
        if transaction['sender'] not in self.users or transaction['receiver'] not in self.users:
            return False
        if transaction['amount'] <= 0 or self.users[transaction['sender']]['balance'] < transaction['amount']:
            return False
        return True

    def get_user_balances(self):
        user_balances = {username: user['balance']
                         for username, user in self.users.items()}
        return user_balances


app = Flask(__name__)

blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    nonce, hash, seconds = blockchain.mine()
    block = blockchain.create_block(nonce, hash)
    block['message'] = f"Congratulations, you just mined a block in {seconds} seconds!"
    return jsonify(block), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/confirm_chain', methods=['GET'])
def confirm_chain():
    response = {'valid': blockchain.validate_chain()}
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    values = request.get_json()
    success, message = blockchain.add_transaction_to_pool(
        values['sender'], values['receiver'], values['amount'])
    response = {
        'transaction added': success,
        'message': message}
    return jsonify(response), 201


@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    response = {'transaction_pool': blockchain.transaction_pool,
                'completed_transactions': blockchain.completed_transactions}
    return jsonify(response), 200


@app.route('/get_users', methods=['GET'])
def get_users():
    return jsonify(blockchain.users), 200


@app.route('/get_user_balances', methods=['GET'])
def get_user_balances():
    balances = blockchain.get_user_balances()
    return jsonify(balances), 200


@app.route('/create_user', methods=['POST'])
def create_user():
    values = request.get_json()
    blockchain.create_user(values['name'])
    response = {'message': 'Account creation successful.',
                'username': values['name'],
                'status': blockchain.users[values['name']]}
    return jsonify(response), 201


app.run(host='0.0.0.0', port=5000)


from uuid import uuid4

from flask import Flask, request, jsonify

import pow
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()
miner_address = str(uuid4())


@app.route('/transactions', methods=['POST'])
def create_transaction():
    transaction = request.get_json()

    required_keys = ['sender', 'receiver', 'amount']

    if not all(key in transaction for key in required_keys):
        return 'Invalid keys in request.', 400

    index = blockchain.new_transaction(transaction['sender'], transaction['receiver'], transaction['amount'])

    response = {'message': f'Transaction will be added in block {index}.'}
    return jsonify(response), 201


@app.route('/blocks', methods=['POST'])
def create_block():
    previous_block = blockchain.previous_block
    previous_proof = previous_block['proof']
    new_proof = pow.generate_new_proof(previous_proof)

    blockchain.new_transaction('0', miner_address, 1)

    previous_hash = blockchain.hash_block(previous_block)
    block = blockchain.new_block(new_proof, previous_hash)

    response = {
        'message': 'New block created.',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 201


@app.route('/blocks', methods=['GET'])
def read_blocks():
    resolved = blockchain.resolve_chain_conflicts()

    if resolved:
        blocks = {
            'message': 'Your chain is valid.',
            'blockchain': blockchain.chain,
            'length': len(blockchain.chain)
        }
    else:
        blocks = {
            'message': 'Your chain was not valid. It was updated.',
            'blockchain': blockchain.chain,
            'length': len(blockchain.chain)
        }

    return jsonify(blocks), 200


@app.route('/nodes', methods=['POST'])
def create_node():
    response = request.get_json()

    if 'nodes' not in response:
        return 'Invalid keys in request.', 400

    nodes = response['nodes']

    for node in nodes:
        blockchain.new_node(node)

    response = {
        'message': 'Node added succesfully.',
        'number_of_nodes': len(blockchain.nodes)
    }
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)


import datetime
import json
import hashlib
import urllib.parse as url

import requests

import pow


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()
        self.new_block(100, 1)

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block in the chain.

        :param int proof: Proof given by PoW algorithm
        :param previous_hash: (Optional) Hash of the previous block
        :type previous_hash: str or None
        :return dict: The new block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.pending_transactions = []
        self.chain.append(block)

        return block

    @property
    def previous_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, receiver, amount):
        """
        Creates a new transaction that needs to go to the next block.

        :param str sender: Address of the sender
        :param str receiver: Address of the receiver
        :param int amount: Amount to be transfered
        :return int: Index of the block that will hold this transaction
        """

        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        return self.previous_block['index'] + 1

    def new_node(self, address):
        """
        Adds a new node to our blockchain nodes list.

        :param str address: URL address of the node
        :return: None
        """

        parsed_address = url.urlparse(address)
        self.nodes.add(parsed_address.netloc)

    @classmethod
    def validate_chain(cls, chain):
        """
        Validates the blockchain of a node.

        :param list chain: Blockchain of a node
        :return bool: True if the chain is valid, False if not
        """

        previous_block = chain[0]

        for block in chain[1:]:
            if block['previous_hash'] != cls.hash_block(previous_block):
                return False

            if not pow.validate_proof(previous_block['proof'], block['proof']):
                return False

            previous_block = block

        return True

    def resolve_chain_conflicts(self):
        """
        Resolves blockchain conflicts by replacing our chain with the longest valid one.

        :return bool: True if our chain was replaced, False if not
        """

        new_chain = None
        longest_length = len(self.chain)

        for node in self.nodes:
            response = requests.get(f'http://{node}/blocks')

            if response.status_code == 200:
                chain = response.json()['blockchain']
                length = response.json()['length']

                if length > longest_length and self.validate_chain(chain):
                    new_chain = chain
                    longest_length = length

        if new_chain is not None:
            self.chain = new_chain
            return True

        return False

    @staticmethod
    def hash_block(block):
        """
        Creates a SHA-256 hash of a block.

        :param dict block: Block to hash
        :return str: SHA-256 hash of the block in HEX representation
        """

        serialized_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(serialized_block).hexdigest()

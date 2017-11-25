
import datetime
import json
import hashlib


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
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

    @staticmethod
    def hash_block(block):
        """
        Creates a SHA-256 hash of a block.

        :param dict block: Block to hash
        :return str: SHA-256 hash of the block in HEX representation
        """

        serialized_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(serialized_block).hexdigest()

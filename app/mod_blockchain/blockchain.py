"""
This is responsible for handling block chains and creating new blocks on the chain. A new block is structured as below
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
"""
import hashlib
import json
from time import time


class Blockchain(object):
    """
    Blockchain class implementation
    """

    def __init__(self):
        """
        Creates a new instance of a Blockchain. When instantiated, a new genesis block is created (Block without any
        predecessors), we will also need to add proof to the genesis block
        """
        self.current_transactions = []
        self.chain = []

        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        creates a new block and adds it to the chain
        :param previous_hash: (Optional) Previous hash of the block in the chain
        :type previous_hash int
        :param proof Proof given by proof of work algorithm
        :type proof int
        :return: new Block
        :rtype: dict
        """
        block = dict(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.chain[-1])
        )

        # reset the current list of transactions
        self.current_transactions = []

        # add the block to the chain
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the block
        :param sender Address of sender
        :type sender str
        :param recipient Address of recipient
        :type recipient str
        :param amount Amount being sent
        :type amount int
        :return: Index of the block that will hold this transaction
        :rtype: int
        """
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        })

        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        :param block:
        :type block dict
        :return: Hash of the given block
        :rtype: str
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """Returns the last block on the chain"""
        return self.chain[-1]


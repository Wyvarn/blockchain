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
from urllib.parse import urlparse
from app import logger
from requests import get


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
        self.nodes = set()
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        creates a new block and adds it to the chain
        :param previous_hash: (Optional) Previous hash of the block in the chain
        :type previous_hash str
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
            previous_hash=previous_hash or self.hash(self.chain[-1]),
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
        self.current_transactions.append(
            {"sender": sender, "recipient": recipient, "amount": amount}
        )

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

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof
        :type last_proof int
        :return: Proof of work
        :rtype: int
        """
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :type last_proof int
        :param proof: Current Proof
        :type proof int
        :return: True if correct, False if not.
        :rtype: bool
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        Adds a new node to the list of nodes
        :param address: Address of node e.g http://192.168.1.0:8000
        :type address str
        :return: None
        :rtype: None
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts a URL without scheme
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("Invalid URL")

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: Blockchain
        :type chain Blockchain
        :return: True if valid, False otherwise
        :rtype: bool
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            logger.debug(f"Last block {last_block}")
            logger.debug(f"block {block}")
            logger.debug("\n-----------\n")

            # check that the hash of the block is correct
            last_block_hash = self.hash(block)

            if block["previous_hash"] != last_block_hash:
                return False

            # check that the proof of work is correct

            # Check that the Proof of Work is correct
            if not self.valid_proof(
                last_block["proof"], block["proof"], last_block_hash
            ):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = get(f"http://{node}/chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

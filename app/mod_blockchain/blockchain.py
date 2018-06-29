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


class Blockchain(object):
    """
    Blockchain class implementation
    """

    def __init__(self):
        self.current_transactions = []
        self.chain = []

    def new_block(self):
        """
        creates a new block and adds it to the chain
        :return:
        """
        pass

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

        :param block:
        :return:
        """
        pass

    @property
    def last_block(self):
        """Returns the last block on the chain"""
        pass

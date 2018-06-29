from . import block
from flask import jsonify, request
from uuid import uuid4
from .blockchain import Blockchain

# generates a globally unique address for this node
node_identifier = str(uuid4()).replace("-", "")

blockchain = Blockchain()


@block.route("/transactions/new", methods=["POST"])
def new_transaction():
    return "Add a new transaction"


@block.route("/mine", methods=["POST"])
def mine_block():
    return "Mine a new block"


@block.route("/chain", methods=["GET"])
def get_chain():
    response = dict(
        chain=blockchain.chain,
        length=len(blockchain.chain)
    )
    return jsonify(response), 200


from . import block
from flask import jsonify, request
from uuid import uuid4
from .blockchain import Blockchain
from app import logger

# generates a globally unique address for this node
node_identifier = str(uuid4()).replace("-", "")

blockchain = Blockchain()


@block.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    logger.debug(f"Received values in creating new transaction {values}")

    required = ["sender", "recipient", "amount"]

    if not all(value in values for value in required):
        return "Missing values", 400

    # create a new transaction
    index = blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])

    response = dict(
        message=f"Transaction will be added to block {index}"
    )

    return jsonify(response), 201


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


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
    """
    Our mining endpoint is where the magic happens, and it’s easy. It has to do three things:
    1. Calculate the Proof of Work
    2. Reward the miner (us) by adding a transaction granting us 1 coin
    3. Forge the new Block by adding it to the chain

    :return: json response
    :rtype: tuple
    """
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    # forge a new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = dict(
        message="New block forged",
        index=block["index"],
        transactions=block["transactions"],
        proof=block["proof"],
        previous_hash=block["previous_hash"]
    )

    return jsonify(response), 200


@block.route("/chain", methods=["GET"])
def get_chain():
    response = dict(
        chain=blockchain.chain,
        length=len(blockchain.chain)
    )
    return jsonify(response), 200


@block.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@block.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200
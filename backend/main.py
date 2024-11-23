import os

from blockchain import Blockchain
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Response
from network import Network
from node import Node

load_dotenv(override=True)
port = os.getenv('PORT') or 5000

app = Flask(__name__)

blockchain = Blockchain()
network = Network()

@app.route('/chain', methods=['GET'])
def get_chain() -> tuple[Response, int]:
	chain_data = []

	for block in blockchain.chain:
		chain_data.append(block.__dict__)

	response = {
		'chain': chain_data,
		'length': len(chain_data)
	}

	return jsonify(response), 200

@app.route('/node/id', methods=['GET'])
def node_get_id() -> tuple[Response, int]:
	response = {
		'nodeID': network.own_node_id
	}

	return jsonify(response), 200

@app.route('/node/register', methods=['POST'])
def node_register() -> tuple[Response, int]:
	data = request.get_json()

	if not data['address']:
		return jsonify({'message': 'Invalid address'}), 400

	new_node = Node(data['address'])
	new_node_id = new_node.retrieve_node_id()

	if not new_node_id:
		return jsonify({'message': 'Node ID retrieval failed'}), 400

	if network.update_node_address(new_node):
		return jsonify({'message': 'Node updated'}), 200

	network.add_node(new_node)
	return jsonify({'message': 'Node registered'}), 201

@app.route('/node/registered', methods=['GET'])
def node_get_registered() -> tuple[Response, int]:
	response = {
		'nodes': [node.to_json_format() for node in network.nodes]
	}

	return jsonify(response), 200

@app.route('/node/resolve', methods=['POST'])
def node_resolve_conflicts() -> tuple[Response, int]:
	if not network.nodes:
		return jsonify({'message': 'No nodes registered'}), 409

	resolved = network.resolve_conflicts(blockchain)

	if resolved:
		return jsonify({'message': 'Chain resolved'}), 200

	return jsonify({'message': 'Chain not resolved'}), 409

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)

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

@app.route('/mine', methods=['POST'])
def mine()  -> tuple[Response, int]:
	block_index = blockchain.mine()

	if not block_index:
		return jsonify({'message': 'No transactions to mine'}), 400

	mined_block = blockchain.chain[-1]
	response = {
		'message': 'Block mined successfully!',
		'block': mined_block.to_dict(),
		'pending_transactions_cleared': True
	}
	return jsonify(response), 200

@app.route('/order', methods=['POST'])
def order() -> tuple[Response, int]:

    data = request.get_json()
    print("Received order data:", data)

    response = {
        'message': 'Order request received.',
        'data_received': data
    }
    return jsonify(response), 200

@app.route('/order/check', methods=['POST'])
def order_check() -> tuple[Response, int]:

    data = request.get_json()

    if 'order_id' not in data:
        return jsonify({'message': 'Order ID is missing'}), 400

    response = {
        'message': 'Order check request received.',
        'order_id': data['order_id'],
        'status': 'Pending'
    }
    return jsonify(response), 200

@app.route('/order/new', methods=['POST'])
def order_new() -> tuple[Response, int]:

    data = request.get_json()

    blockchain.add_new_transaction(data)

    response = {
        'message': 'New order transaction created.',
        'transaction': data
    }
    return jsonify(response), 200

@app.route('/order/update', methods=['POST'])
def order_update() -> tuple[Response, int]:

    data = request.get_json()

    if 'order_id' not in data or 'updates' not in data:
        return jsonify({'message': 'Order ID or update fields are missing'}), 400

    response = {
        'message': 'Order update request received.',
        'order_id': data['order_id'],
        'updates': data['updates']
    }
    return jsonify(response), 200

@app.route('/order/transfer', methods=['POST'])
def order_transfer() -> tuple[Response, int]:

    data = request.get_json()

    required_fields = ['order_id', 'new_receiver']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields in transfer data'}), 400

    response = {
        'message': 'Order transfer request received.',
        'order_id': data['order_id'],
        'new_receiver': data['new_receiver']
    }
    return jsonify(response), 200

@app.route('/order/complete', methods=['POST'])
def order_complete() -> tuple[Response, int]:

    data = request.get_json()

    if 'order_id' not in data:
        return jsonify({'message': 'Order ID is missing'}), 400

    response = {
        'message': 'Order complete request received.',
        'order_id': data['order_id']
    }
    return jsonify(response), 200

@app.route('/organization/create', methods=['POST'])
def organization_create() -> tuple[Response, int]:

    data = request.get_json()

    required_fields = ['organization_name', 'details']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields in organization data'}), 400

    response = {
        'message': 'Organization creation request received.',
        'organization_data': data
    }
    return jsonify(response), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)

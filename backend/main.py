import os

from blockchain import Blockchain
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Response
from network import Network
from node import Node
from transaction.complete_order import CompleteOrder
from transaction.create_order import CreateOrder
from transaction.create_organization import CreateOrganization
from transaction.transfer_order import TransferOrder
from transaction.update_order import UpdateOrder

load_dotenv(override=True)
port = os.getenv('PORT') or 5000

app = Flask(__name__)

blockchain = Blockchain()
network = Network()

def check_missing_fields(data: dict, required_fields: list[str]) -> str:
	missing_fields = [field for field in required_fields if field not in data]

	if missing_fields:
		return 'Missing fields: ' + ', '.join(missing_fields)

	return ''

@app.route('/chain', methods=['GET'])
def chain_get() -> tuple[Response, int]:
	chain_data = []

	for block in blockchain.chain:
		chain_data.append(block.__dict__)

	response = {
		'chain': chain_data,
		'length': len(chain_data)
	}

	return jsonify(response), 200

@app.route('/mine', methods=['POST'])
def mine_block()  -> tuple[Response, int]:
	block_index = blockchain.mine()

	if not block_index:
		return jsonify({'message': 'No transactions to mine'}), 409

	mined_block = blockchain.chain[block_index]
	return jsonify(mined_block.to_dict()), 201

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

@app.route('/order/<order_code>', methods=['GET'])
def order_check(order_code: str) -> tuple[Response, int]:
	if not order_code:
		return jsonify({'message': 'Order code is missing'}), 400

	data = blockchain.get_order_all_transactions(order_code)

	if not data:
		return jsonify({'message': 'Order not found'}), 404

	return jsonify(data), 200

@app.route('/order/new', methods=['POST'])
def order_new() -> tuple[Response, int]:
	data = request.get_json()

	message = check_missing_fields(data, ['createdBy', 'data'])
	if message:
		return jsonify({'message': message}), 400

	tx = CreateOrder(data['createdBy'], data['data'])
	
	if not blockchain.add_new_transaction(tx):
		return jsonify({'message': 'Failed to create a new order'}), 409

	return jsonify(tx.to_json_format()), 201

@app.route('/order/update', methods=['POST'])
def order_update() -> tuple[Response, int]:
	data = request.get_json()

	message = check_missing_fields(data, ['createdBy', 'data', 'orderCode'])
	if message:
		return jsonify({'message': message}), 400

	tx = UpdateOrder(data['createdBy'], data['data'], data['orderCode'])

	if not blockchain.add_new_transaction(tx):
		return jsonify({'message': 'Failed to update the order'}), 409

	return jsonify(tx.to_json_format()), 201

@app.route('/order/transfer', methods=['POST'])
def order_transfer() -> tuple[Response, int]:
	data = request.get_json()

	message = check_missing_fields(data, ['createdBy', 'data', 'orderCode', 'newOwner'])
	if message:
		return jsonify({'message': message}), 400

	tx = TransferOrder(data['createdBy'], data['data'], data['orderCode'], data['newOwner'])

	if not blockchain.add_new_transaction(tx):
		return jsonify({'message': 'Failed to transfer the order'}), 409

	return jsonify(tx.to_json_format()), 201

@app.route('/order/complete', methods=['POST'])
def order_complete() -> tuple[Response, int]:
	data = request.get_json()

	message = check_missing_fields(data, ['createdBy', 'data', 'orderCode'])
	if message:
		return jsonify({'message': message}), 400

	tx = CompleteOrder(data['createdBy'], data['data'], data['orderCode'])

	if not blockchain.add_new_transaction(tx):
		return jsonify({'message': 'Failed to complete the order'}), 409

	return jsonify(tx.to_json_format()), 201

@app.route('/organization/create', methods=['POST'])
def organization_create() -> tuple[Response, int]:
	data = request.get_json()

	message = check_missing_fields(data, ['data'])
	if message:
		return jsonify({'message': message}), 400

	tx = CreateOrganization(data['data'])

	if not blockchain.add_new_transaction(tx):
		return jsonify({'message': 'Failed to create an organization'}), 409

	return jsonify(tx.to_json_format()), 201

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)

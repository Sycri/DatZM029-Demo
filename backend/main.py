from blockchain import Blockchain
from flask import Flask, jsonify

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
	chain_data = []

	for block in blockchain.chain:
		chain_data.append(block.__dict__)

	response = {
		'chain': chain_data,
		'length': len(chain_data)
	}

	return jsonify(response), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)

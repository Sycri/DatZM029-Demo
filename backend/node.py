import requests

from block import Block

class Node:
	def __init__(self, address: str, node_id: str = None):
		self.address = address
		self.node_id = node_id
		self.resolved_at = None

	def get_chain(self) -> tuple[int, list[Block]]:
		response = requests.get('http://' + self.address + '/chain')

		if response.status_code != 200:
			return None, None

		try:
			response_json = response.json()
		except:
			return None, None

		chain_data = response_json['chain']

		return response_json['length'], [Block.from_dict(block) for block in chain_data]

	def retrieve_node_id(self) -> str:
		response = requests.get('http://' + self.address + '/node/id')

		if response.status_code != 200:
			return None

		try:
			response_json = response.json()
		except:
			return None

		self.node_id = response_json['nodeID']
		return self.node_id

	def to_json_data(self) -> dict:
		return {
			'address': self.address,
			'nodeID': self.node_id,
			'resolvedAt': self.resolved_at
		}

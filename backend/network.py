import json
import os
import time
import uuid

from blockchain import Blockchain
from node import Node

class Network:
	nodes_file = 'data/nodes.json'

	def __init__(self):
		self.own_node_id = str(uuid.uuid4()).replace('-', '')
		self.nodes: list[Node] = []

		if os.path.exists(self.nodes_file):
			self.load_from_disk()
		else:
			self.save_to_disk()

	def add_node(self, node: Node):
		self.nodes.append(node)
		self.save_to_disk()

	def update_node_address(self, node: Node) -> bool:
		for n in self.nodes:
			if n.node_id == node.node_id:
				n.address = node.address
				self.save_to_disk()
				return True

		return False

	def resolve_conflicts(self, blockchain: Blockchain) -> bool:
		new_chain = None
		max_length = len(blockchain.chain)
		resolved = False

		for node in self.nodes:
			length, node_chain = node.get_chain()
			if not node_chain:
				continue

			if length != len(node_chain):
				continue

			if length > max_length and Blockchain.is_valid_chain(node_chain):
				new_chain = node_chain
				max_length = length

			node.resolved_at = time.time_ns()
			resolved = True

		if new_chain:
			blockchain.replace_chain(new_chain)

		if resolved:
			self.save_to_disk()

		return resolved

	def from_json_format(self, data: dict):
		self.own_node_id = data['ownNodeID']

		for n in data['nodes']:
			node = Node(n['address'], n['nodeID'])

			if 'resolvedAt' in n:
				node.resolved_at = n['resolvedAt']

			self.nodes.append(node)

	def to_json_format(self) -> dict:
		return {
			'ownNodeID': self.own_node_id,
			'nodes': [node.to_json_format() for node in self.nodes]
		}

	def save_to_disk(self):
		if os.path.exists(self.nodes_file):
			os.replace(self.nodes_file, self.nodes_file + '.old')

		with open(self.nodes_file, 'w') as f:
			json.dump(self.to_json_format(), f)

	def load_from_disk(self):
		self.nodes = []

		with open(self.nodes_file, 'r') as f:
			self.from_json_format(json.load(f))

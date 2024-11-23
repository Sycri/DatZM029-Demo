import hashlib
import json
import time

class Block:
	def __init__(self, index: int, transactions: list, previous_hash: str, timestamp: int = None, nonce: int = 0):
		self.index = index
		self.transactions = transactions
		self.previous_hash = previous_hash
		self.timestamp = timestamp or time.time_ns()
		self.nonce = nonce

	def get_static_data(self) -> str:
		return json.dumps({
			'index': self.index,
			'transactions': self.transactions,
			'previous_hash': self.previous_hash,
			'timestamp': self.timestamp
		}, sort_keys=True)

	def compute_hash(self, static_data: str) -> str:
		block_string = static_data + str(self.nonce)
		return hashlib.sha256(block_string.encode()).hexdigest()

	def to_dict(self) -> dict:
		return {
			'index': self.index,
			'transactions': self.transactions,
			'previous_hash': self.previous_hash,
			'timestamp': self.timestamp,
			'nonce': self.nonce,
			'hash': self.hash
		}

	@staticmethod
	def from_dict(data: dict):
		block = Block(
			index=data['index'],
			transactions=data['transactions'],
			previous_hash=data['previous_hash'],
			timestamp=data['timestamp'],
			nonce=data['nonce']
		)
		block.hash = data['hash']

		return block

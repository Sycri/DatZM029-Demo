import hashlib
import json
import time

class Block:
	def __init__(self, index: int, transactions: list, previous_hash: str, nonce: int = 0):
		self.index = index
		self.transactions = transactions
		self.timestamp = time.time_ns()
		self.previous_hash = previous_hash
		self.nonce = nonce

	def get_static_data(self) -> str:
		return json.dumps({
			'index': self.index,
			'transactions': self.transactions,
			'timestamp': self.timestamp,
			'previous_hash': self.previous_hash
		}, sort_keys=True)

	def compute_hash(self, static_data: str) -> str:
		block_string = static_data + str(self.nonce)
		return hashlib.sha256(block_string.encode()).hexdigest()

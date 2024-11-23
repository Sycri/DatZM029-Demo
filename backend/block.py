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

	# Convert data to dict
	def to_dict(self) -> dict:
		return {
			"index": self.index,
			"transactions": self.transactions,
			"timestamp": self.timestamp,
			"previous_hash": self.previous_hash,
			"nonce": self.nonce,
			"hash": self.hash
		}
	 # Class method to create a Block instance from a dictionary
	@classmethod
	def from_dict(cls, data: dict):
		block = cls(
			index=data["index"],
			transactions=data["transactions"],
			previous_hash=data["previous_hash"],
			nonce=data["nonce"]
		)
		block.timestamp = data["timestamp"]
		block.hash = data["hash"]
		return block
	
import abc
import hashlib
import json
import time

from block import Block

class BaseTransaction(abc.ABC):
	def __init__(self, type: int, created_by: str, data: dict):
		self.timestamp = time.time_ns()

		self.type = type
		self.created_by = created_by
		self.data = data

		self.prev_tx_id: str = None
		self.prev_tx_block_id: str = None
		self.tx_id: str = None

	def get_static_data(self) -> str:
		return json.dumps({
			'timestamp': self.timestamp,
			'type': self.type,
			'created_by': self.created_by,
			'data': self.data,
			'prev_tx_id': self.prev_tx_id,
			'prev_tx_block_id': self.prev_tx_block_id
		}, sort_keys=True)

	def generate_tx_id(self):
		transaction_string = self.get_static_data()
		return hashlib.sha256(transaction_string.encode()).hexdigest() 

	def to_dict(self) -> dict:
		return {
			'timestamp': self.timestamp,
			'type': self.type,
			'created_by': self.created_by,
			'data': self.data,
			'prev_tx_id': self.prev_tx_id,
			'prev_tx_block_id': self.prev_tx_block_id,
			'tx_id': self.tx_id
		}

	def to_json_format(self) -> dict:
		return {
			'timestamp': self.timestamp,
			'type': self.type,
			'createdBy': self.created_by,
			'data': self.data,
			'prevTxID': self.prev_tx_id,
			'prevTxBlockID': self.prev_tx_block_id,
			'txID': self.tx_id
		}

	@abc.abstractmethod
	def validate(self, *_) -> bool:
		pass

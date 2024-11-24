import json
from typing import override

from transaction.base_order import BaseOrder

class TransferOrder(BaseOrder):
	def __init__(self, created_by: str, data: str, order_code: str, new_owner: str):
		self.new_owner = new_owner
		super().__init__(3, created_by, data, order_code)

	@override
	def get_static_data(self) -> str:
		return json.dumps({
			'timestamp': self.timestamp,
			'type': self.type,
			'created_by': self.created_by,
			'data': self.data,
			'prev_tx_id': self.prev_tx_id,
			'prev_tx_block_id': self.prev_tx_block_id,
			'order_code': self.order_code,
			'new_owner': self.new_owner
		}, sort_keys=True)

	@override
	def to_dict(self) -> dict:
		return {
			'timestamp': self.timestamp,
			'type': self.type,
			'created_by': self.created_by,
			'data': self.data,
			'prev_tx_id': self.prev_tx_id,
			'prev_tx_block_id': self.prev_tx_block_id,
			'tx_id': self.tx_id,
			'order_code': self.order_code,
			'new_owner': self.new_owner
		}

	@override
	def to_json_format(self) -> dict:
		return {
			'timestamp': self.timestamp,
			'type': self.type,
			'createdBy': self.created_by,
			'data': self.data,
			'prevTxID': self.prev_tx_id,
			'prevTxBlockID': self.prev_tx_block_id,
			'txID': self.tx_id,
			'orderCode': self.order_code,
			'newOwner': self.new_owner
		}

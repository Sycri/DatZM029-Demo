import json
from typing import override

from block import Block
from transaction.base_transaction import BaseTransaction

class BaseOrder(BaseTransaction):
	def __init__(self, type: int, created_by: str, data: dict, order_code: str):
		self.order_code = order_code
		super().__init__(type, created_by, data)

	@override
	def get_static_data(self) -> str:
		return json.dumps({
			'timestamp': self.timestamp,
			'type': self.type,
			'created_by': self.created_by,
			'data': self.data,
			'prev_tx_id': self.prev_tx_id,
			'prev_tx_block_id': self.prev_tx_block_id,
			'order_code': self.order_code
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
			'order_code': self.order_code
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
			'orderCode': self.order_code
		}

	def get_order_prev_tx(self, chain: list[Block], pending_transactions: list[BaseTransaction]) -> tuple[dict, int]:
		for tx in reversed(pending_transactions):
			# 1 - CreateOrder, 2 - UpdateOrder, 3 - TransferOrder, 4 - CompleteOrder
			if tx['type'] in [1, 2, 3, 4] and tx['order_code'] == self.order_code:
				return tx, chain[-1].index + 1

		for block in reversed(chain):
			for tx in reversed(block.transactions):
				# 1 - CreateOrder, 2 - UpdateOrder, 3 - TransferOrder, 4 - CompleteOrder
				if tx['type'] in [1, 2, 3, 4] and tx['order_code'] == self.order_code:
					return tx, block.index

		return None, None

	@override
	def validate(self, chain: list[Block], pending_transactions: list[BaseTransaction]) -> bool:
		# Verify that the order was created, updated or transfered before
		prev_tx, prev_tx_block_id = self.get_order_prev_tx(chain, pending_transactions)
		if not prev_tx:
			return False

		# Verify that a completed order is not being changed
		if prev_tx['type'] == 4:
			return False

		# Verify that the order is being changed by the organization that currently owns it
		if (prev_tx['type'] != 3 and prev_tx['created_by'] != self.created_by) \
			or (prev_tx['type'] == 3 and prev_tx['new_owner'] != self.created_by):
			return False

		self.prev_tx_id = prev_tx['tx_id']
		self.prev_tx_block_id = prev_tx_block_id
		return True

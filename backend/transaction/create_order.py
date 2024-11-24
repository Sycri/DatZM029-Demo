from typing import override
import uuid

from block import Block
from transaction.base_order import BaseOrder
from transaction.base_transaction import BaseTransaction

class CreateOrder(BaseOrder):
	def __init__(self, created_by: str, data: dict):
		super().__init__(1, created_by, data, self.generate_order_code())

	def generate_order_code(self):
		return str(uuid.uuid4()).replace('-', '').upper()

	def get_org_tx(self, chain: list[Block], pending_transactions: list[BaseTransaction]) -> tuple[str, int]:
		for tx in reversed(pending_transactions):
			if tx['type'] == 0 and tx['tx_id'] == self.created_by:
				return tx['tx_id'], chain[-1].index + 1

		for block in reversed(chain):
			for tx in reversed(block.transactions):
				if tx['type'] == 0 and tx['tx_id'] == self.created_by:
					return tx['tx_id'], block.index

		return None, None

	@override
	def validate(self, chain: list[Block], pending_transactions: list[BaseTransaction]) -> bool:
		# Verify that the order was created by an existing organization
		prev_tx_id, prev_tx_block_id = self.get_org_tx(chain, pending_transactions)
		if not prev_tx_id:
			return False

		self.prev_tx_id = prev_tx_id
		self.prev_tx_block_id = prev_tx_block_id
		return True

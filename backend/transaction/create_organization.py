from typing import override

from block import Block
from transaction.base_transaction import BaseTransaction

class CreateOrganization(BaseTransaction):
	def __init__(self, data: dict, created_by: str = None):
		super().__init__(0, created_by, data)

	@override
	def validate(self, *_) -> bool:
		return True

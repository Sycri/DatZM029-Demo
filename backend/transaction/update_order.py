from transaction.base_order import BaseOrder

class UpdateOrder(BaseOrder):
	def __init__(self, created_by: str, data: dict, order_code: str):
		super().__init__(2, created_by, data, order_code)

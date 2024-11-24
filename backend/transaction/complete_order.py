from transaction.base_order import BaseOrder

class CompleteOrder(BaseOrder):
	def __init__(self, created_by: str, data: str, order_code: str):
		super().__init__(4, created_by, data, order_code)

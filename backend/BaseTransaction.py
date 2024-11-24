import json
import hashlib
import time
from typing import Optional

# Base class for all transactions
class BaseTransaction:
    def __init__(self, organization: str, prev_transaction_id: Optional[str] = None, order_code: Optional[str] = None):
        self.timestamp = time.time()
        self.organization = organization
        self.prev_transaction_id = prev_transaction_id
        self.order_code = order_code
        # Section with transaction ID - replace with implemented blockchain
        self.transaction_id = self.generate_transaction_id()

    def generate_transaction_id(self):
        transaction_string = f"{self.timestamp}{self.organization}{self.prev_transaction_id}{self.order_code}"
        return hashlib.sha256(transaction_string.encode()).hexdigest() 
    # EO Section with transaction ID

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

# Transaction to create a new order
class CreateOrder(BaseTransaction):
    def __init__(self, organization: str, order_details: dict):
        super().__init__(organization)
        self.order_details = order_details
        self.order_code = self.generate_order_code()

    def generate_order_code(self):
        order_string = f"{self.organization}{self.timestamp}{self.order_details}"
        return hashlib.sha256(order_string.encode()).hexdigest() # Replace with other version of how to generate order code

# Transaction to update an existing order
class UpdateOrder(BaseTransaction):
    def __init__(self, organization: str, prev_transaction_id: str, order_code: str, updated_details: dict):
        super().__init__(organization, prev_transaction_id, order_code)
        self.updated_details = updated_details

# Transaction to transfer an order from one organization to another
class TransferOrder(BaseTransaction):
    def __init__(self, organization: str, prev_transaction_id: str, order_code: str, new_organization: str):
        super().__init__(new_organization, prev_transaction_id, order_code)
        self.old_organization = organization

# Transaction to create a new organization
class CreateOrganization(BaseTransaction):
    def __init__(self, organization: str, organization_details: dict):
        super().__init__(organization)
        self.organization_details = organization_details

"""
# Example Usage
if __name__ == "__main__":
    # Create a new organization
    org_creation = CreateOrganization("OrgA", {"name": "Organization A", "address": "123 Blockchain Ave."})
    print("Create Organization Transaction:")
    print(org_creation.to_json())

    # Create a new order
    create_order = CreateOrder("OrgA", {"item": "Laptop", "quantity": 10})
    print("\nCreate Order Transaction:")
    print(create_order.to_json())

    # Update the order
    update_order = UpdateOrder("OrgA", create_order.transaction_id, create_order.order_code, {"quantity": 12})
    print("\nUpdate Order Transaction:")
    print(update_order.to_json())

    # Transfer the order to another organization
    transfer_order = TransferOrder("OrgA", update_order.transaction_id, create_order.order_code, "OrgB")
    print("\nTransfer Order Transaction:")
    print(transfer_order.to_json())
"""
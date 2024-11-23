import os
import json
import re
from block import Block

class Blockchain:
	difficulty = 2

	def __init__(self):
		self.chain = []
		self.pending_transactions = []

		os.makedirs('data', exist_ok=True)
		if os.path.exists('data/block_0.json'):
			self.load_from_disk() # Load existing chain if it exists
		else:
			self.create_genesis_block()

	def create_genesis_block(self):
		genesis_block = Block(0, [], '0')
		genesis_block.hash = genesis_block.compute_hash(genesis_block.get_static_data())
		self.chain.append(genesis_block)
		self.save_to_disk()

	@property
	def last_block(self) -> Block:
		return self.chain[-1]

	def add_new_transaction(self, transaction):
		self.pending_transactions.append(transaction)

	@staticmethod
	def is_valid_proof(proof: str) -> bool:
		return proof.startswith('0' * Blockchain.difficulty)

	@staticmethod
	def proof_of_work(block: Block) -> str:
		static_data = block.get_static_data()

		block.nonce = 0
		proof = block.compute_hash(static_data)

		while not Blockchain.is_valid_proof(proof):
			block.nonce += 1
			proof = block.compute_hash(static_data)

		return proof

	def is_valid_block(self, block: Block, previous_block: Block, proof: str) -> bool:
		if previous_block.index + 1 != block.index:
			return False

		if previous_block.hash != block.previous_hash:
			return False

		if not Blockchain.is_valid_proof(proof):
			return False

		return proof == block.compute_hash(block.get_static_data())

	def add_block(self, block: Block, proof: str) -> bool:
		if not self.is_valid_block(block, self.last_block, proof):
			return False

		block.hash = proof
		self.chain.append(block)
		self.save_to_disk(block.index)
		return True

	def mine(self) -> int|bool:
		if not self.pending_transactions:
			return False

		last_block = self.last_block
		new_block = Block(
			index=last_block.index + 1,
			transactions=self.pending_transactions,
			previous_hash=last_block.hash
		)

		proof = self.proof_of_work(new_block)

		self.add_block(new_block, proof)
		self.pending_transactions = []
		return new_block.index

	def is_valid_chain(self) -> bool:
		for i in range(1, len(self.chain)):
			current_block = self.chain[i]
			previous_block = self.chain[i - 1]

			proof = current_block.hash
			if not self.is_valid_block(current_block, previous_block, proof):
				return False

		return True
	
	def save_to_disk(self, from_index: int = 0):
		for block in self.chain[from_index:]:
			block_file = f'data/block_{block.index}.json'

			with open(block_file, 'w') as f:
				json.dump(block.to_dict(), f)

	def load_from_disk(self):
		self.chain = []

		# Use pattern to match by file name block_<number>.json
		name_pattern = re.compile(r'^block_(\d+)\.json$')

		# Sort matching files by block number
		block_files = sorted(
			[i for i in os.listdir('data') if name_pattern.match(i)], # Get file names that match the pattern
			key=lambda x: int(x.split('_')[1].split('.')[0]) # Get block number
		)

		for block_file in block_files:
			with open(f'data/{block_file}', 'r') as f:
				block = Block.from_dict(json.load(f))
				self.chain.append(block)

from random_strategy import Random
import random


class Simple:
	def __init__(self):
		self.WALL = 0
		self.EMPTY = 1
		self.FOOD = 2
		self.GHOST = 3
		self.PACMAN = 4

	''' The simple strategy: 
						Go after food.
						Try and avoid ghosts.
	'''
	def move(self, board, pos, adv_pos, score):
		r = Random()
		poss_moves = r.get_poss_moves(board, pos)
		unsafe_moves = self.retrieve_subset(board, poss_moves, self.GHOST)
		gourmand_moves = self.retrieve_subset(board, poss_moves, self.FOOD)
		neutral_moves = self.retrieve_subset(board, poss_moves, self.EMPTY)

		if len(poss_moves) == 0:
			print "Blocked! No move possible!"
			return None

		# Try to go where the food is
		if len(gourmand_moves) != 0:
			j = random.randrange(0, len(gourmand_moves))
		elif len(neutral_moves) != 0:
			j = random.randrange(0, len(neutral_moves))
		else:
			j = random.randrange(0, len(unsafe_moves))

		return poss_moves[j]

	'''
		minus = True => retrieve_subset of elems in set
						with a value other than elem
	'''
	def retrieve_subset(self, board, set, elem, minus=False):
		if minus:
			return [(l,c) for (l,c) in set if board[l][c] == elem]	
		return [(l,c) for (l,c) in set if board[l][c] == elem]
		
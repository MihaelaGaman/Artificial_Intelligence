from utils import valid_pos, \
				check_free_cell
import random

class Random:
	def __init__(self):
		self.WALL = 0
		self.EMPTY = 1
		self.FOOD = 2
		self.GHOST = 3
		self.PACMAN = 4

	def move(self, board, pos, adv_pos, score):
		return self.get_next_pos(board, self.PACMAN, pos)


	'''
	Get a random next move from all the possible moves.
	'''
	def get_next_pos(self, board, actor, curr_pos):
		L = len(board)
		C = len(board[0])

		# generate possible moves
		poss_moves = self.get_poss_moves(board, curr_pos)
		if len(poss_moves) == 0:
			return None
		j = random.randrange(0, len(poss_moves))

		return poss_moves[j]

	'''
	Given the current position and the board, generate all possible
	possitions.
	'''
	def get_poss_moves(self, board, curr_pos):
		L = len(board)
		C = len(board[0])
		(cl, cc) = curr_pos
		poss_moves = [(cl -1, cc), (cl + 1, cc), (cl, cc - 1), (cl, cc + 1)]
		
		aux = [m for m in poss_moves if valid_pos(L, C, m)]
		
		return [elem for elem in aux if check_free_cell(board, elem[0], elem[1]) \
		or board[elem[0]][elem[1]] == 4]
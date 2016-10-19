import copy
import math

class Expectimax:

	def __init__(self):
		self.WALL = 0
		self.EMPTY = 1
		self.FOOD = 2
		self.GHOST = 3
		self.PACMAN = 4

	def move(self, board, pos, adv_pos, score):

		inf = float('inf')
		mininf = float('-inf')

		res = self.expectimax(board, pos, adv_pos, 2, True, False)
	
		return res[1]

	def expectimax(self, board, pos, adv_pos, depth, maximizingPlayer, chance):
		inf = float('inf')
		mininf = float('-inf')

		if maximizingPlayer:
			possible = [(pos[0], pos[1] + 1), \
					(pos[0], pos[1] - 1), \
					(pos[0] - 1, pos[1]), \
					(pos[0] + 1, pos[1])]
			children = [ch for ch in possible if self.validCell(ch[0], ch[1], board)]

			if len(children) == 0 or depth == 0:
				return (0, (None, None))

			v = (mininf, (None, None))

			for chld in children:
				restore_val = board[chld[0]][chld[1]]
				board[chld[0]][chld[1]] = self.PACMAN

				computedVal = self.expectimax(board, chld, adv_pos,\
				 depth - 1, False, False)
				old_v = copy.deepcopy(v)
				v = (max(v[0], computedVal), v[1])

				if v[0] != old_v[0]:
					v = (v[0], chld)

				# Undo:
				board[chld[0]][chld[1]] = restore_val

			return v
		elif not maximizingPlayer and not chance:
			children = []
			for adv in adv_pos:
				possible = [(adv[0], adv[1] + 1), \
					(adv[0], adv[1] - 1), \
					(adv[0] - 1, adv[1]), \
					(adv[0] + 1, adv[1])]
				
				child_list = [ch for ch in possible if self.validCell(ch[0], ch[1], board)]
				children.append(child_list)

				if len(children) == 0 or depth == 0:
					return (0, pos)

			s = 0
			n = 0
			for i in range(len(children)):
				for j in range(len(children[i])):
					chld = children[i][j]
					
					restore_val = board[chld[0]][chld[1]]
					board[chld[0]][chld[1]] = self.GHOST
					chld_pos = copy.deepcopy(adv_pos)
					chld_pos[i] = chld

					s += self.expectimax(board, pos, chld_pos, \
						depth, False, True)
					n += 1;
					
					# Undo:
					board[chld[0]][chld[1]] = restore_val

			return s / n

		else:
			return self.computeMyWin(board, pos[0], pos[1])


	def validCell(self, l, c, board):
		h = len(board)
		w = len(board[0])

		if l < 0 or l >= h or c < 0 or c >= w:
			return False

		if board[l][c] == self.WALL or board[l][c] == self.GHOST:
			return False
		return True

	def euclideanDist(self, l1, c1, l2, c2):
		return float(math.sqrt(float(math.pow((l2 - l1), 2)) \
			+ float(math.pow((c2 - c1), 2))))
	
	# Get elems of same type (ghosts/food)
	def get_elems(self, board, elem_type):
		return [(l, c) for l in range(len(board)) \
			for c in range(len(board[0])) \
				if board[l][c] == elem_type]

	def get_min_dist_elem(self, board, elem_type, l, c):
		elems = self.get_elems(board, elem_type)
		elems_dist = [self.euclideanDist(float(l), float(c), float(i), float(j)) \
			for (i, j) in elems]

		if len(elems_dist) == 0:
			return 0

		return min(elems_dist)

	def computeMyWin(self, board, l, c):
		closest_food = self.get_min_dist_elem(board, self.FOOD, l, c)
		closest_ghost = self.get_min_dist_elem(board, self.GHOST, l, c)
		no_food_left = float(len(self.get_elems(board, self.GHOST)))

		if closest_ghost == 0.0:
			closest_ghost = 0.001


		g = -1.5 * closest_food - 2.5 * 1.0/closest_ghost - 4.0 * no_food_left

		return g

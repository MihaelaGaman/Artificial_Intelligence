import random
import copy
import time

'''
Params: no of lines (L)
		no of cols (C)
Build map with food.
'''
def build_map(L, C, food):
	return [[food for i in range(0, L)] for j in range(0, C)]


'''
No other thing than food in the cell (or empty)
'''
def check_free_cell(board, l, c):
	return board[l][c] == 1 or board[l][c] == 2

'''
Change board by adding new_elem at each pos in positions.
'''
def change_board(positions, new_elem, board):
	new_board = copy.deepcopy(board)
	for (l, c) in positions:
		new_board[l][c] = new_elem

	return new_board

'''
Number of food left on board.
'''
def get_food_no(board, food):
	return sum([item for l in board for item in l if item == food]) / 2

'''
Check that pos is in limits.
'''
def valid_pos(L, C, pos):
	return pos[0] < L and pos[1] < C and pos[0] >= 0 and pos[1] >= 0

'''
Matrix-like display of the board.
'''
def display_board(board):
	for l in board:
		str_board_line = ""
		for elem in l:
			str_board_line += "" + str(elem) + " "
		print str_board_line

	print("---------------------------------------------")
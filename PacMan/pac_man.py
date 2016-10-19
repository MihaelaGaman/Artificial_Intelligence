import random
import copy
import time
import argparse

from utils import display_board, \
					change_board, \
					get_food_no, \
					valid_pos, \
					check_free_cell, \
					build_map

from expectimax import Expectimax
from strategy import Minimax
from file_map import read_map, \
					 get_character

from random_strategy import Random
from simple_strategy import Simple

''' 
	Params: the min/max no of objects (ghosts, food, walls)
			total no of lines/cols
'''
def obj_generation(min_obj, max_obj, L, C, board):
	# How many objects?
	no = random.randrange(min_obj, max_obj)

	# list of already generated positions
	obj_pos = []
	for i in range(0, no):
		#randomly generate line, col
		l = random.randrange(0, L)
		c = random.randrange(0, C)

		# Do not generate a new object in a cell where we already
		# have an object
		while len(obj_pos) != 0 and (l, c) in obj_pos \
			and not check_free_cell(board, l, c):
			l = random.randrange(0, L)
			c = random.randrange(0, C)

		obj_pos.append((l, c))

	return obj_pos

'''
	Actions taken at the move of an actor (ghost or PACMAN).
'''
def move(board, actor, curr_pos, prev_value):
	(cl, cc) = curr_pos
	r = Random()
	x = r.get_next_pos(board, actor, (cl, cc))

	if x == None:
		return board, (cl, cc), prev_value

	(nl, nc) = x

	restore_val = board[nl][nc]
	board[nl][nc] = actor
	board[cl][cc] = prev_value

	return board, (nl, nc), restore_val

'''
	Return strategy constructor by its type.
'''
def get_strategy(strategy_type):
	if strategy_type == "minimax":
		return Minimax()
	elif strategy_type == "expectimax":
		return Expectimax()
	elif strategy_type == "simple":
		return Simple()
	else:
		return Random()

'''
	The criteria for winning:
		All food on the board should be eaten.
'''
def win(board, score):
	if get_food_no(board, 2) == 0:
		print "============ PACMAN wins! ================="
		print "Score: ", score
		return True
	return False

'''
	Loose:
		PACMAN is not on board anymore.
'''
def loose(board, score):
	for l in board:
		for elem in l:
			if elem == 4:
				return False
	print "============ PACMAN looses! ================="
	print "Score: ", score
	return True

'''
	Move continuosly until the end of the game or for max_moves.
	Params:
		strategy : {"minimax", "expectimax", "random", "simple"}
		board
		pacman_pos
		ghosts_pos - a list
'''
def continuously_move(board, pacman_pos, ghosts_pos, strategy):
	# Ghosts sit initially on empty cells
	restore_info = [1 for g in ghosts_pos]
	s = get_strategy(strategy)
	score = 0

	# moves
	m = 0

	while m < 100:
		m += 1
		display_board(board)

		# Move PACMAN
		old_pos = copy.deepcopy(pacman_pos)
		pacman_pos = s.move(board, old_pos, ghosts_pos, score)
		board[old_pos[0]][old_pos[1]] = 1
		if board[pacman_pos[0]][pacman_pos[1]] == 2:
			print "Gotcha!"
			score += 1
		board[pacman_pos[0]][pacman_pos[1]] = 4

		# Check win
		if win(board, score):
			return score

		# Move ghosts
		for i in range(0, len(ghosts_pos)):
			board, ghosts_pos[i], restore_info[i] = \
			move(board, 3, ghosts_pos[i], restore_info[i])
			if loose(board, score):
				return score
		
		# delay the board change to see what happens.
		time.sleep(0.5)

	return score

'''
	Build random board using the dimensions given as command line args.
	The symbols on the board:
		Wall:   0
		Empty:  1
		Food:   2
		Ghost:  3
		PACMAN: 4

'''
def random_board(H, W):
	board = build_map(H, W)

	ghosts_pos = obj_generation(2, 3, H, W, board)
	board = change_board(ghosts_pos, 3, board)

	walls_pos = obj_generation(3, 10, H, W, board)
	board = change_board(walls_pos, 0, board)

	pacman_pos = obj_generation(1, 2, H, W, board)
	board = change_board(pacman_pos, 4, board)
	display_board(board)

	return board, ghosts_pos, walls_pos, pacman_pos

# Main method
def main():
	s1 = 0
	s2 = 0
	s3 = 0
	s4 = 0
	for i in range(15):
		parser = argparse.ArgumentParser(description='Process game options.')
		parser.add_argument('--mode', type=int, default=1,
                   help='mode of map construction')
		parser.add_argument('--filename', type=str, default='map.txt',
                   help='Map name')

		args = parser.parse_args()
		if args.mode == 1:
			board = read_map(args.filename)
			ghosts_pos = get_character(board, 3)
			walls_pos = get_character(board, 0)
			pacman_pos = get_character(board, 4)
		else:
			board, ghosts_pos, walls_pos, pacman_pos = \
			random_board(7, 7)

		if i % 4 == 0:
			s1 += continuously_move(board, pacman_pos[0], ghosts_pos, "minimax")
			print s1
		elif i % 4 == 1:
			s2 += continuously_move(board, pacman_pos[0], ghosts_pos, "expectimax")
			print s2
		elif i % 4 == 2:
			s3 += continuously_move(board, pacman_pos[0], ghosts_pos, "simple")
			print s3
		else:
			s4 += continuously_move(board, pacman_pos[0], ghosts_pos, "random")
			print s4

	s1 = s1 / 5
	s2 = s2 / 5
	s3 = s3 / 5
	s4 = s4 / 5

	print "Expectimax = ", s2
	print "Minimax = ", s1
	print "Simple = ", s3
	print "Random = ", s4

main()

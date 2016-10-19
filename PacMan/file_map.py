import re

def read_map(file_name):
	board = []
	f = open(file_name, 'r')

	for l in f:
		print l
		aux = re.split(' ', l)
		board.append(map(int, aux)) 

	print board
	f.close()

	return board

def get_character(board, sign):
	H = len(board)
	W = len(board[0]) 
	return [(i, j) for i in range(H) for j in range(W) if board[i][j] == sign]
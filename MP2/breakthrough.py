
from node import Node 
import random

#global definitions:
black_list = []
white_list = []


# goal is to create an 8x8 grid
# 'B' demarcates black pieces, 'W' demarcates white pieces, and ' ' demarcates empty positions
# This function reads in the grid from the text file and generates the 
# 2D array to traverse through. NOTE: to access (x,y) locations in the maze
# you must call it as grid[y][0][x]. 
def read_grid():
	grid = [[' ' for x in range(10)] for y in range(10)]
	for numy in range(10):
		for numx in range(10):
			if numx == 0 or numx == 9:
				grid[numy][numx] = '%'
			if numy == 0 or numy == 9:
				grid[numy][numx] = '%'
			
			if(numx>0 and numx<9):
				if(numy == 1 or numy == 2):
					grid[numy][numx] = 'B'
				if(numy == 7 or numy == 8):
					grid[numy][numx] = 'W'

	#textFile = open(gridname, "r")
	#for line in textFile:
	#	grid.append(line.strip().split('\r\n '))

	#textFile.close()

	return grid

# This function adds the (x,y) positions of the white and black pieces to their respective
# lists. 
def populate_lists():
	grid = read_grid()
	global black_list
	global white_list

	# for ypos, line in enumerate(grid): 
	# 	for string in line: 
	# 		for xpos, char in enumerate(string):
	# 			if char == 'B':
	# 				black_list.append((xpos, ypos))
	# 			if char == 'W':
	# 				white_list.append((xpos, ypos))
	for ypos in range(10):
		for xpos in range(10):
			if grid[ypos][xpos] == 'B':
				black_list.append((xpos,ypos))
			if grid[ypos][xpos] == 'W':
				white_list.append((xpos, ypos))

					
#implement depth-limited minimax for search tree of depth 3; assuming we are the white player
# def minimax(gridname, node, depth, heuristic_type, isMax, which_list):
# 	global black_list
# 	global white_list
# 	grid = read_grid(gridname)
# 	populate_lists(gridname)

# 	x = node.x 
# 	y = node.y

# 	#when you reach the depth limit, return the heuristic value
# 	if depth == 3:
# 		if heuristic_type == 'defensive':
# 			return defensive_heuristic(len(white_list)) 
# 		else: #use the offensive heuristic
# 			return offensive_heuristic(len(black_list))
# 	if isMax: #maximizing player is WHITE
# 		max_value = -9999
# 		for child in node.children:
# 			if (child.state!= '%' and child.state!= 'W'):
# 				if(child.state == 'B' and (child.action == 0 or child.action == 1)):
# 					black_list.remove((child.x, child.y))
# 				child_value = minimax(gridname, child, depth+1, heuristic_type, False)
# 				max_value = max(max_value, child_value)
# 		return max_value
# 	else: #minimizing player is BLACK
# 		min_value = -9999
# 		for child in node.children:
# 			if(child.state!= '%' and child.state!= 'B'):
# 				if(child.state == 'W' and (child.action == 0 or child.action == 1)):
# 					white_list.remove((child.x, child.y))
# 				child_value = minimax(gridname, child, depth+1, heuristic_type, True)
# 				min_value = min(min_value, child_value)
# 		return min_value

# minimax is given a game state
# obtains valid moves from the game state 
# simulates all valid moves on clones of the game state 
# evaluates each game state which follows a valid move
# returns the best move
def minimax(node, depth, heuristic_type):
	score = 0 
	# if depth = 3 or if game over 
	if depth == 2 or (len(black_list) == 0 or len(white_list) == 0): 
		print "REACHED DEPTH"
		if heuristic_type == 'defensive':
			return defensive_heuristic(len(white_list))
		else:
			return offensive_heuristic(len(black_list))
	#print "Node type: MINIMAX" + str(type(node))
	moves = get_possible_moves(node, 'white').possiblemoves	
	best_move = moves[0]
	best_score = float('-inf')
	for move in moves:
		clone = move
		score = min_player(clone, depth + 1, heuristic_type)
		#print "The score is: " + str(score) 
		if score > best_score: 
			best_move = move
			best_score = score
	return best_move

def min_player(node, depth, heuristic_type):
	score = 0 
	if depth == 2 or (len(black_list) == 0 or len(white_list) == 0): 
		print "REACHED DEPTH-MIN"
		if heuristic_type == 'defensive':
			return defensive_heuristic(len(white_list))
		else:
			return offensive_heuristic(len(black_list))
	#print "Node type: MIN" + str(type(node))
	moves = get_possible_moves(node, 'black').possiblemoves
	best_score = float('inf')
	for move in moves:
		clone = move
		score = max_player(clone, depth + 1, heuristic_type)
		print "The score is: " + str(score)
		if score < best_score:
			best_move = move 
			best_score = score 
	return best_score

def max_player(node, depth, heuristic_type):
	score = 0 
	if depth == 2 or (len(black_list) == 0 or len(white_list) == 0): 
		print "REACHED DEPTH- MAX"
		if heuristic_type == 'defensive':
			return offensive_heuristic(len(white_list))
		else:
			return offensive_heuristic(len(black_list))
	#print "Node type: MAX" + str(type(node))
	moves = get_possible_moves(node, 'white').possiblemoves
	best_score = float('-inf')
	for move in moves:
		clone = move
		score = min_play(clone, depth + 1, heuristic_type)
		if score > best_score:
			best_move = move
			best_score = score
	return best_score

def defensive_heuristic(num_pieces_remaining):
	return 2 * num_pieces_remaining + random.random()

def offensive_heuristic(num_opposing_remaining):
	return 2 * (30 - num_opposing_remaining) + random.random()

def get_possible_moves(node, which_list):
	if which_list == 'white':
		use_list = white_list
	else:
		use_list = black_list

	for piece in use_list:
		x = piece[0]
		y = piece[1]

		if which_list == 'white':
			newy = y-1
			newchar = 'W'
		else:
			newy = y+1
			newchar = 'B'

	 	if is_valid(x-1, newy, 0, which_list): #left diagonal
	 		#print "(" + str(x) + ", " + str(y) + ") can move left diagonal."
	 		temp_grid0= read_grid()
	 		temp_grid0[y][x] = ' ' #vacate old spot
	 		temp_grid0[newy][x-1] = newchar #move to new spot
	 		#print_grid(temp_grid0)
	 		leftnode = Node(temp_grid0)
			node.possiblemoves.append(leftnode)
	 	if is_valid(x, newy, 1, which_list): #straight
	 		#print "(" + str(x) + ", " + str(y) + ") can move straight."
	 		temp_grid1 = read_grid()
	 		temp_grid1[y][x] = ' '
	 		temp_grid1[newy][x] = newchar
	 		#print_grid(temp_grid1)
	 		straightnode = Node(temp_grid1)
	 		node.possiblemoves.append(straightnode)
	 	if is_valid(x+1, newy, 2, which_list): #right diagonal
	 		#print "(" + str(x) + ", " + str(y) + ") can move right diagonal."
	 		temp_grid2 = read_grid()
			temp_grid2[y][x] = ' '
			temp_grid2[newy][x+1] = newchar
			#print_grid(temp_grid2)
			rightnode = Node(temp_grid2)
	 		node.possiblemoves.append(rightnode)
	return node

def print_grid(gridname):
	print('\n'.join([''.join(['{:1}'.format(item) for item in row]) for row in gridname]))

# 0 = left diagonal, 1 = straight, 2 = right diagonal
def is_valid(x, y, action, which_list):
	grid = read_grid()

	#make sure its a valid point within (0, 0) to (9, 9)
	if which_list is 'white':
		if (x >= 0 and x <= 9 and y >= 0 and y <= 9):
			if (grid[y][x]== '%' or grid[y][x] == 'W'): #if it's a border or occupied, return false right away
				return False
			else:
				if (grid[y][x] == ' '):
					return True
				else:
					if (grid[y][x] == 'B' and (action == 0 or action ==2)): #if it's occupied by black and you moved straight
						black_list.remove((x, y))
						return True
					else:
						return False
				
		else:
			return False
	else: 
		if (x >= 0 and x <= 9 and y >= 0 and y <= 9):
			if (grid[y][x]== '%' or grid[y][x] == 'B'): #if it's a border or occupied, return false right away
				return False
			else:
				if(grid[y][x] == ' '):
					return True
				else:
					if (grid[y][x] == 'W' and (action == 0 or action == 2)): #if it's occupied by white and you moved straight
						white_list.remove((x,y))
						return True
					else:
						return False
		else:
			return False

def main(gridname):
	grid = read_grid()

	populate_lists()
	print "Black list:" + str(black_list)
	print "Num black pieces: " + str(len(black_list))
	print "White list:" + str(white_list)
	print "Num white pieces: " + str(len(white_list))
	
	new_game = Node(grid)
	get_possible_moves(new_game, 'white')
	#print grid

	print "Number of possible moves: " + str(len(new_game.possiblemoves))
	#print minimax(gridname, node, 1, defensive, True)
	game = minimax(new_game, 0, 'defensive')
	print_grid(game.state)

if __name__ == '__main__':
	main("new_game.txt")
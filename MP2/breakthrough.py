from node import Node 
import random
import sys
import copy
from operator import itemgetter

#global definitions:
black_list = []
white_list = []


# goal is to create an 8x8 grid
# 'B' demarcates black pieces, 'W' demarcates white pieces, and ' ' demarcates empty positions
# This function reads in the grid from the text file and generates the 
# 2D array to traverse through. NOTE: to access (x,y) locations in the maze
# you must call it as grid[y][0][x]. 
def make_grid():
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

	return grid

# This function adds the (x,y) positions of the white and black pieces to their respective
# lists. 
def populate_lists(gridname):
	grid = gridname
	global black_list
	global white_list
	black_list = []
	white_list = []

	for ypos in range(10):
		for xpos in range(10):
			if grid[ypos][xpos] == 'B':
				black_list.append((xpos,ypos))
			if grid[ypos][xpos] == 'W':
				white_list.append((xpos, ypos))

# read a grid and check to see if white/black has made it to the other end
def goal_check(gridname):
	if gridname == None: 
		return False
	
	if len(black_list) == 0 or len(white_list) == 0: 
		return True

	for xpos in range(10):
		if gridname[1][xpos] == 'W' or gridname[8][xpos] == 'B':
			return True
	
	return False
		
					
# minimax is given a game state
# obtains valid moves from the game state 
# simulates all valid moves on clones of the game state 
# evaluates each game state which follows a valid move
# returns the best move
def minimax(node, depth, heuristic_type, player_color):
	global white_list 
	global black_list
	score = 0 
	# if depth = 3 or if game over 
	if player_color:
		use_list = white_list 
		opposing_list = black_list
	else: 
		use_list = black_list
		opposing_list = white_list

	if depth == 2 or (len(black_list) == 0 or len(white_list) == 0) or goal_check(node.state): 
		#print "REACHED DEPTH"
		if heuristic_type == 0:
			return defensive_heuristic(len(use_list))
		if heuristic_type == 1:
			return offensive_heuristic(len(opposing_list))
		if heuristic_type == 2:
			return offensive_heuristic2(use_list, player_color, len(opposing_list))
		if heuristic_type == 3:
			return defensive_heuristic2(len(use_list), use_list)
	populate_lists(node.state)
	moves = get_possible_moves(node, player_color).possiblemoves
	print "moves:" + str(len(moves))
	best_move = moves[0]
	best_score = float('-inf')
	for move in moves:
		clone = move
		score = min_player(clone, depth + 1, heuristic_type, player_color)
		# #print "The score is: " + str(score) 
		if score > best_score: 
		 	best_move = move
		 	best_score = score

	return best_move

def min_player(node, depth, heuristic_type, player_color):
	global white_list 
	global black_list
	score = 0 

	if player_color:
		use_list = white_list 
		opposing_list = black_list
	else: 
		use_list = black_list
		opposing_list = white_list

	if depth == 2 or (len(black_list) == 0 or len(white_list) == 0) or goal_check(node.state): 
		#print "REACHED DEPTH-MIN"
		if heuristic_type == 0:
			return defensive_heuristic(len(use_list))
		if heuristic_type == 1:
			return offensive_heuristic(len(opposing_list))
		if heuristic_type == 2:
			return offensive_heuristic2(use_list, player_color, len(opposing_list))
		if heuristic_type == 3:
			return defensive_heuristic2(len(use_list), use_list)
	#print "Node type: MIN" + str(type(node))
	opposing_player = not player_color
	#print "opposing player is: " + str(opposing_player)
	populate_lists(node.state)
	moves = get_possible_moves(node, opposing_player).possiblemoves
	best_score = float('inf')
	for move in moves:
		clone = move
		score = max_player(clone, depth + 1, heuristic_type, player_color)
		#print "The score is: " + str(score)
		if score < best_score:
			best_move = move 
			best_score = score 
	return best_score

def max_player(node, depth, heuristic_type, player_color):
	global white_list 
	global black_list
	score = 0 

	if player_color:
		use_list = white_list
		opposing_list = black_list 
	else: 
		use_list = black_list
		opposing_list = white_list

	if depth == 2 or (len(black_list) == 0 or len(white_list) == 0) or goal_check(node.state): 
		#print "REACHED DEPTH- MAX"
		if heuristic_type == 0:
			return defensive_heuristic(len(use_list))
		if heuristic_type == 1:
			return offensive_heuristic(len(opposing_list))
		if heuristic_type == 2:
			return offensive_heuristic2(use_list, player_color, len(opposing_list))
		if heuristic_type == 3:
			return defensive_heuristic2(len(use_list), use_list)
	#print "Node type: MAX" + str(type(node))
	populate_lists(node.state)
	moves = get_possible_moves(node, player_color).possiblemoves
	best_score = float('-inf')
	for move in moves:
		clone = move
		score = min_player(clone, depth + 1, heuristic_type, player_color)
		if score > best_score:
			best_move = move
			best_score = score
	return best_score

def defensive_heuristic(num_pieces_remaining):
	return 2 * num_pieces_remaining + random.random()

def defensive_heuristic2(num_pieces_remianing, black_list):
	numChain = 0
	prevRow = []
	curRow = []
	step = 8
	for x in range(0, len(black_list)):
		for z in range(0, len(curRow)):
			prevRow[z] = curRow[z]
		del curRow[:]
		for i in black_list:
			if i.x == x:
				curRow.append(i)

		for a in prevRow:
			for b in curRow:
				if abs(a.y-b.y) <= 1
					numChain += 1

	return numChain





def offensive_heuristic(num_opposing_remaining):
	return 2 * (30 - num_opposing_remaining) + random.random()

def offensive_heuristic2(own_list, player_color, num_opposing_remaining):
	#offensive heuristic 2 should just focus on getting to the other side
	#pass in (x,y) values of black or white values 
	if player_color: #if white
		farthest = min(own_list, key = itemgetter(1))[1]
	else:
		farthest = max(own_list, key = itemgetter(1))[1]

	return farthest * (40 - num_opposing_remaining) + random.random()

def defensive_heuristic2(num_pieces_remaining, own_list):
	average = 0
	for i in own_list:
		average += i[1]
	average /= num_pieces_remaining
	average = int(round(average))
	total = 0
	for i in own_list:
		diff = abs(average-i[1])
		total += 3-diff

	return total


def get_possible_moves(node, which_list):
	global white_list
	global black_list
	newy = 0 
	if which_list:
		use_list = white_list
	else:
		use_list = black_list

	#print "currently analyzing: " + str(which_list) + " with length " + str(len(use_list))

	temp_list = []
	check_grid = copy.deepcopy(node.state)
	
	for piece in use_list:
		updateflag = False
		x = piece[0]
		y = piece[1]

		if which_list:
			newy = y-1
			newchar = 'W'
		else:
			newy = y+1
			newchar = 'B'

		#when moving pieces need to update the location in the list
	 	if is_valid(check_grid, x-1, newy, 0, which_list): #left diagonal
	 		#print "(" + str(x) + ", " + str(y) + ") can move left diagonal." 
	 		temp_grid0 = copy.deepcopy(check_grid)
	 		temp_grid0[y][x] = ' ' #vacate old spot
	 		temp_grid0[newy][x-1] = newchar #move to new spot
	 		updateflag = True
	 		#temp_list.append((x-1, y))
	 		#print_grid(temp_grid0)
	 		leftnode = Node(temp_grid0)
			node.possiblemoves.append(leftnode)

	 	if is_valid(check_grid, x, newy, 1, which_list): #straight
	 		#print "(" + str(x) + ", " + str(y) + ") can move straight."
	 		temp_grid1= copy.deepcopy(check_grid)
	 		temp_grid1[y][x] = ' '
	 		temp_grid1[newy][x] = newchar
	 		updateflag = True
	 		#temp_list.append((x, newy))
	 		#print_grid(temp_grid1)
	 		straightnode = Node(temp_grid1)
	 		node.possiblemoves.append(straightnode)
	 		
	 	if is_valid(check_grid, x+1, newy, 2, which_list): #right diagonal
	 		#print "(" + str(x) + ", " + str(y) + ") can move right diagonal."
	 		temp_grid2= copy.deepcopy(check_grid)
			temp_grid2[y][x] = ' '
			temp_grid2[newy][x+1] = newchar
			updateflag = True
	 		#temp_list.append((x+1, newy))
			#print_grid(temp_grid2)
			rightnode = Node(temp_grid2)
	 		node.possiblemoves.append(rightnode)
	updateflag = False

	# if updateflag:
	#  	use_list.remove(piece)
	#  	use_list = use_list + temp_list

	updateflag = False

	return node

def print_grid(gridname):
	print('\n'.join([''.join(['{:1}'.format(item) for item in row]) for row in gridname]))

# 0 = left diagonal, 1 = straight, 2 = right diagonal
def is_valid(grid, x, y, action, which_list):
	#make sure its a valid point within (0, 0) to (9, 9)
	global black_list
	global white_list
	#print "black: " + str(len(black_list)) + " white: " + str(len(white_list))

	if which_list:
		if (x >= 0 and x <= 9 and y >= 0 and y <= 9):
			if (grid[y][x]== '%' or grid[y][x] == 'W'): #if it's a border or occupied, return false right away
				return False
			else:
				if (grid[y][x] == ' '):
					return True
				#else:
				if (grid[y][x] == 'B' and (action == 0 or action ==2)): #if it's occupied by black and you moved straight
					return True
				#else:
					#return False
				
		else:
			return False
	else: 
		if (x >= 0 and x <= 9 and y >= 0 and y <= 9):
			if (grid[y][x]== '%' or grid[y][x] == 'B'): #if it's a border or occupied, return false right away
				return False
			else:
				if(grid[y][x] == ' '):
					return True
				#else:
				if (grid[y][x] == 'W' and (action == 0 or action == 2)): #if it's occupied by white and you moved straight
					return True
		else:
			return False

# The same as minimax but branches of the search tree can be eliminated
# alpha and beta are the upper and the lower cutoff limits for when to stop searching
# alpha = the value of the MAX choice we have found so far at any point for MAX
# beta = the value of the  MIN choice we have found so far at any point for MIN
# a/b search updates the values of a/b as it goes along and prunes the remaining branches at a node 
# AS SOON AS THE VALUE OF THE CURRENT NODE IS KNWON TO BEWORSE THAN THE CURRENT A/B 
def alphabeta_search(node, depth, heuristic_type, player_color, alpha, beta):
	global white_list 
	global black_list
	score = 0 
	# if depth = 3 or if game over 
	if player_color:
		use_list = white_list
		opposing_list = black_list

	else: 
		use_list = black_list
		opposing_list = white_list

	if depth == 3 or (len(black_list) == 0 or len(white_list) == 0) or goal_check(node.state): 
		#print "REACHED DEPTH"
		if heuristic_type == 0:
			return defensive_heuristic(len(use_list))
		if heuristic_type == 1:
			return offensive_heuristic(len(opposing_list))
		if heuristic_type == 2:
			return offensive_heuristic2(use_list, player_color, len(opposing_list))
		if heuristic_type == 3:
			return defensive_heuristic2(len(use_list), use_list)
	#print "Node type: MINIMAX" + str(type(node))
	populate_lists(node.state)
	moves = get_possible_moves(node, player_color).possiblemoves	
	best_move = moves[0]
	best_score = float('-inf')
	for move in moves:
		clone = move
		score = min_player_alpha(clone, depth + 1, heuristic_type, player_color, alpha, beta)
		#print "The score is: " + str(score) 
		if score > best_score: 
			best_move = move
			best_score = score

	return best_move

def min_player_alpha(node, depth, heuristic_type, player_color, alpha, beta):
	global white_list 
	global black_list
	score = 0 

	if player_color:
		use_list = white_list 
		opposing_list = black_list
	else: 
		use_list = black_list
		opposing_list = white_list

	if depth == 3 or (len(black_list) == 0 or len(white_list) == 0) or goal_check(node.state): 
		#print "REACHED DEPTH-MIN"
		if heuristic_type == 0:
			return defensive_heuristic(len(use_list))
		if heuristic_type == 1:
			return offensive_heuristic(len(opposing_list))
		if heuristic_type == 2:
			return offensive_heuristic2(use_list, player_color, len(opposing_list))
		if heuristic_type == 3:
			return defensive_heuristic2(len(use_list), use_list)

	#print "Node type: MIN" + str(type(node))
	opposing_player = not player_color
	#print "opposing player is: " + str(opposing_player)
	populate_lists(node.state)
	moves = get_possible_moves(node, opposing_player).possiblemoves
	best_score = float('inf')
	for move in moves:
		clone = move
		score = max_player_alpha(clone, depth + 1, heuristic_type, player_color, alpha, beta)
		#print "The score is: " + str(score)
		if score < best_score:
			best_move = move 
			best_score = score 
		beta = min(beta, best_score)
		if beta <= alpha:
			break
	return best_score

def max_player_alpha(node, depth, heuristic_type, player_color, alpha, beta):
	global white_list 
	global black_list
	score = 0 

	if player_color:
		use_list = white_list 
		opposing_list = black_list
	else: 
		use_list = black_list
		opposing_list = white_list

	if depth == 3 or (len(black_list) == 0 or len(white_list) == 0) or goal_check(node.state): 
		#print "REACHED DEPTH- MAX"
		if heuristic_type == 0:
			return defensive_heuristic(len(use_list))
		if heuristic_type == 1:
			return offensive_heuristic(len(opposing_list))
		if heuristic_type == 2:
			return offensive_heuristic2(use_list, player_color, len(opposing_list))
		if heuristic_type == 3:
			return defensive_heuristic2(len(use_list), use_list)

	#print "Node type: MAX" + str(type(node))
	populate_lists(node.state)
	moves = get_possible_moves(node, player_color).possiblemoves
	best_score = float('-inf')
	for move in moves:
		clone = move
		score = min_player_alpha(clone, depth + 1, heuristic_type, player_color, alpha, beta)
		if score > best_score:
			best_move = move
			best_score = score
		alpha = max(alpha, best_score)
		if beta <= alpha:
			break
	return best_score

def main(gridname):
	global white_list 
	global black_list
	sys.stdout = open ("results.txt", "w")
	grid = make_grid()

	populate_lists(grid)
	# print "Black list:" + str(black_list)
	# print "Num black pieces: " + str(len(black_list))
	# print "White list:" + str(white_list)
	# print "Num white pieces: " + str(len(white_list))
	
	# new_game = Node(grid)
	# get_possible_moves(new_game, 'white')
	# #print grid

	# print "Number of possible moves: " + str(len(new_game.possiblemoves))
	# #print minimax(gridname, node, 1, defensive, True)

	# # False means black player, True means white player
	# game = minimax(new_game, 0, 'defensive', True)
	# print type(game)
	# print_grid(game.state)
	# if goal_check(game.state):
	# 	print "game's over"
	# else:
	# 	print "game's not over"
	# 0 = defensive 
	# 1 = offensive 
	# 2 = offensive 
	# 3 = defensive
	new_game = Node(grid)
	#game = minimax(new_game, 0, 1, True) #white always goes first
	game = alphabeta_search(new_game, 0, 2, True, float('-inf'), float('inf'))
	print_grid(game.state)
	count = 1
	game2 = Node(game.state)
	while (goal_check(game.state)!= True):
		if count %2 == 0: #even so its white so do minimax
			#game2 = minimax(game, 0, 1, True) #white goes first
			game2= alphabeta_search(game, 0, 2, True, float('-inf'), float('inf'))
		else:
			game2 = alphabeta_search(game, 0, 1, False, float('-inf'), float('inf'))
		print "update:"
		print_grid(game2.state)
		populate_lists(game2.state)
		print "Black list:" + str(black_list)
		print "Num black pieces: " + str(len(black_list))
		print "White list:" + str(white_list)
		print "Num white pieces: " + str(len(white_list))
		game = Node(game2.state)
		#player = not player
		count += 1
	print count 

if __name__ == '__main__':
	main("new_game.txt")

from node import Node 

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
def minimax(gridname, node, depth, heuristic_type, isMax):
	global black_list
	global white_list
	grid = read_grid(gridname)
	populate_lists(gridname)

	x = node.x 
	y = node.y

	#when you reach the depth limit, return the heuristic value
	if depth == 3:
		if heuristic_type == 'defensive':
			return defensive_heuristic(len(white_list)) 
		else: #use the offensive heuristic
			return offensive_heuristic(len(black_list))
	if isMax: #maximizing player is WHITE
		max_value = -9999
		for child in node.children:
			if (child.state!= '%' and child.state!= 'W'):
				if(child.state == 'B' and (child.action == 0 or child.action == 1)):
					black_list.remove((child.x, child.y))
				child_value = minimax(gridname, child, depth+1, heuristic_type, False)
				max_value = max(max_value, child_value)
		return max_value
	else: #minimizing player is BLACK
		min_value = -9999
		for child in node.children:
			if(child.state!= '%' and child.state!= 'B'):
				if(child.state == 'W' and (child.action == 0 or child.action == 1)):
					white_list.remove((child.x, child.y))
				child_value = minimax(gridname, child, depth+1, heuristic_type, True)
				min_value = min(min_value, child_value)
		return min_value


def defensive_heuristic(num_pieces_remaining):
	return 2 * num_pieces_remaining + random()

def offensive_heuristic(num_opposing_remaining):
	return 2 * (30 - num_opposing_remaining) + random()

def get_possible_moves():
	for piece in white_list:
		x = piece[0]
		y = piece[1]
	 	if is_valid(x-1,y-1, 0): #left diagonal
	 		print "(" + str(x) + ", " + str(y) + ") can move left diagonal."
	 		temp_grid0= read_grid()
	 		temp_grid0[y][x] = ' ' #vacate old spot
	 		temp_grid0[y-1][x-1] = 'W' #move to new spot
	 		print_grid(temp_grid0)
	# 		leftnode = Node(temp_grid0)
	# 		node.child.append(leftnode)
	 	if is_valid(x, y-1, 1): #straight
	 		print "(" + str(x) + ", " + str(y) + ") can move straight."
	 		temp_grid1 = read_grid()
	 		temp_grid1[y][x] = ' '
	 		temp_grid1[y-1][x] = 'W'
	 		print_grid(temp_grid1)
	# 		straightnode = Node(temp_grid1)
	# 		node.child.append(straightnode)
	 	if is_valid(x+1, y-1, 2): #right diagonal
	 		print "(" + str(x) + ", " + str(y) + ") can move right diagonal."
	 		temp_grid2 = read_grid()
			temp_grid2[y][x] = ' '
			temp_grid2[y-1][x+1] = 'W'
			print_grid(temp_grid2)
	# 		rightnode = Node(temp_grid2)
	# 		node.child.append(rightnode)
	# grid = read_grid()
	# grid[0][0] = 'A'
	# print_grid(grid)

def print_grid(gridname):
	print('\n'.join([''.join(['{:1}'.format(item) for item in row]) for row in gridname]))

# 0 = left diagonal, 1 = straight, 2 = right diagonal
def is_valid(x, y, action):
	grid = read_grid()

	#make sure its a valid point within (0, 0) to (9, 9)
	if (x >= 0 and x <= 9 and y >= 0 and y <= 9):
		if (grid[y][x]== '%' or grid[y][x] == 'W'): #if it's a border or occupied, return false right away
			return False
		else:
			if (grid[y][x] == 'B' and action == 1): #if it's occupied by black and you moved straight
				return False
			else:
				return True
	else:
		return False

def main(gridname):
	grid = read_grid()

	populate_lists()
	print "Black list:" + str(black_list)
	print "Num black pieces: " + str(len(black_list))
	print "White list:" + str(white_list)
	print "Num white pieces: " + str(len(white_list))
	
	# new_game = Node(grid)
	get_possible_moves()
	#print grid

	#print minimax(gridname, node, 1, defensive, True)

if __name__ == '__main__':
	main("new_game.txt")
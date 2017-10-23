
from node import Node 

#global definitions:
black_list = []
white_list = []


# goal is to create an 8x8 grid
# 'B' demarcates black pieces, 'W' demarcates white pieces, and ' ' demarcates empty positions
# This function reads in the grid from the text file and generates the 
# 2D array to traverse through. NOTE: to access (x,y) locations in the maze
# you must call it as grid[y][0][x]. 
def read_grid(gridname):
	textFile = open(gridname, "r")
	grid = []

	for line in textFile:
		grid.append(line.strip().split('\r\n '))

	textFile.close()

	return grid

# This function adds the (x,y) positions of the white and black pieces to their respective
# lists. 
def populate_lists(gridname):
	grid = read_grid(gridname)
	global black_list
	global white_list

	for ypos, line in enumerate(grid): 
		for string in line: 
			for xpos, char in enumerate(string):
				if char == 'B':
					black_list.append((xpos, ypos))
				if char == 'W':
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
	if depth == 3
		if heuristic_type = 'defensive':
			return defensive_heuristic(len(white_list)) 
		else: #use the offensive heuristic
			return offensive_heuristic(len(black_list))
	if isMax: #maximizing player is WHITE
		max_value = -9999
		for child in node.children:
			if (child.state! = '%' and child.state!= 'W'):
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

def get_possible_moves(gridname):
	grid = read_grid(gridname)
	

def main(gridname):
	grid = read_grid(gridname)

	for line in grid: #line is one row of the board
		for s in line: 
			print s

	populate_lists(gridname)
	print "Black list:" + str(black_list)
	print "Num black pieces: " + str(len(black_list))
	print "White list:" + str(white_list)
	print "Num white pieces: " + str(len(white_list))
	
	new_game = Node(grid)

	print minimax(gridname, node, 1, defensive, True)

if __name__ == '__main__':
	main("new_game.txt")
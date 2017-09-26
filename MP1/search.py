from collections import deque
from node import Node

# global definition# 
x_start = 0
y_start = 0
x_end = 0 
y_end = 0
right_bound = 0
down_bound = 0 

# This function reads in the maze from the text file and generates the 
# 2D array to traverse through. NOTE: to access (x,y) locations in the maze
# you must call it as maze[y][0][x]. 									   
def read_map(mapname):
	textFile = open(mapname, "r")
	maze = []

	for line in textFile:
		maze.append(line.strip().split('\r\n '))

	textFile.close()

	return maze

# This function writes back to a text file our 2D array that we read in. 
# Namely used to verify we read in text file correctly. DO NOT CALL.
def write_test_map(mapname):
	maze = read_map(mapname)

	with open(mapname + 'test', 'w') as outFile:
		for item in my_list:
			outFile.write("%s\n"  %item)

# This function finds the (x,y) start position of the maze, marked as 
# 'P' in the text file. It also finds the (x,y) finish position of the maze,
# marked as '.'
def find_start_end(mapname):
	maze = read_map(mapname)
	global x_start 
	global y_start
	global x_end 
	global y_end
	global right_bound
	global down_bound

	for ypos, line in enumerate(maze):
		for string in line:
			for xpos, char in enumerate(string):
				if char == 'P':
					x_start = xpos
					y_start = ypos 
				if char == '.':
					x_end = xpos 
					y_end = ypos
			right_bound = xpos
		down_bound = ypos				

# This function conducts a BFS search of the maze. #
def bfs_search(mapname): 
	maze = read_map(mapname)

	node = Node(x_start, y_start, None)
	cur_x = x_start
	cur_y = y_start

	if(node.x == x_end and node.y == y_end):
		return node ##return solution
	
	frontier = deque([])
	frontiernode = deque([])
	#frontier.append(node)
	frontier.append((node.x, node.y))
	frontiernode.append(node)
	
	explored = {}
	while 1:
		if len(frontier) == 0:
			return None

		node = frontier.popleft()
		nodenode = frontiernode.popleft()

		cur_x = node[0]
		cur_y = node[1]

		explored[(cur_x, cur_y)]= cur_x + cur_y

		#if can move right, move right
		if cur_x < right_bound and maze[cur_y][0][cur_x+1]!= '%': 
			child = Node(cur_x + 1, cur_y, 0) #initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:	
				if (child.x == x_end and child.y == y_end):
					return child
				frontier.append((child.x, child.y))
				frontiernode.append(child)

		#if can move down, move down
		if cur_y < down_bound and maze[cur_y + 1][0][cur_x]!= '%': 
			child = Node(cur_x, cur_y + 1, 1)#initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				frontier.append((child.x, child.y))
				frontiernode.append(child)

		#if can move up, move up
		if cur_y > 0 and maze[cur_y - 1][0][cur_x]!= '%':
			child = Node(cur_x, cur_y - 1, 2) #initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				frontier.append((child.x, child.y))
				frontiernode.append(child)

		#if can move left, move left
		if cur_y > 0 and maze[cur_y][0][cur_x-1]!= '%': 
			child = Node(cur_x - 1, cur_y, 3) #initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				frontier.append((child.x, child.y))
				frontiernode.append(child)
	return None 

# This function implements a depth-first search of the maze and prints the solution in text file.
def dfs_search(mapname): 
	maze = read_map(mapname)

	node = Node(x_start, y_start, None)
	cur_x = x_start
	cur_y = y_start

	if(node.x == x_end and node.y == y_end):
		return node #return solution
	
	frontier = deque([])
	frontiernode = deque([])

	frontier.append((node.x, node.y))
	frontiernode.append(node)

	parentNode = frontiernode.pop()

	explored = {}

	while 1:
		if len(frontier) == 0:
			return None

		explored[(cur_x, cur_y)]= cur_x + cur_y

		#if can move right, move right
		if cur_x < right_bound and maze[cur_y][0][cur_x+1]!= '%' and (cur_x+1, cur_y) not in explored: 
			child = Node(cur_x + 1, cur_y, 0) 
			child.parent = parentNode 	
		
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:	
				#check if child is goal 
				if (child.x == x_end and child.y == y_end):
					return child

				frontier.append((child.x, child.y))
				frontiernode.append(child)
				cur_x = child.x
				cur_y = child.y

		
		#if can move down, move down
		elif cur_y < down_bound and maze[cur_y + 1][0][cur_x]!= '%' and (cur_x, cur_y+1) not in explored: 
			child = Node(cur_x, cur_y + 1, 1)
			child.parent = parentNode

			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child

				frontier.append((child.x, child.y))
				frontiernode.append(child)
				cur_x = child.x
				cur_y = child.y

		# #if can move up, move up
		elif cur_y > 0 and maze[cur_y - 1][0][cur_x]!= '%' and (cur_x, cur_y-1) not in explored:
			child = Node(cur_x, cur_y - 1, 2) 		
			child.parent = parentNode 
			
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				
				frontier.append((child.x, child.y))
				frontiernode.append(child)
				cur_x = child.x
				cur_y = child.y
			
		#if can move left, move left
		elif cur_x > 0 and maze[cur_y][0][cur_x-1]!= '%' and (cur_x-1, cur_y) not in explored: 
			child = Node(cur_x - 1, cur_y, 3) 
			child.parent = parentNode
		
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				#insert child to frontier
				frontier.append((child.x, child.y))
				frontiernode.append(child)
				cur_x = child.x
				cur_y = child.y

		else:
			curnode = frontier.pop()
			cur_y = curnode[0]
			cur_x = curnode[1]
			parentNode = frontiernode.pop()

	#return None
	
def aStar(mapname):
	maze = read_map(mapname)


# This function draws the solution on the input maze. 		
def draw_solution(mapname, solution_path):
	maze = read_map(mapname)
	writemap = mapname[:-4] + "test.txt"

	with open(writemap, 'w') as outFile:
		for ypos, line in enumerate(maze):
			for string in line:
				for xpos, char in enumerate(string):
					if (xpos, ypos) in solution_path and (xpos, ypos)!= (x_start, y_start): 
						outFile.write('.')
				 	else:
						outFile.write(char)
			outFile.write('\n')

# Main function
def main(mapname):
	maze= read_map(mapname)

	for line in maze:
		for s in line: 
			print s

	find_start_end(mapname)
	print "START COORDINATES: (" + str(x_start) + ", " + str(y_start) + ")"
	print "DIMENSIONS: " + str(right_bound) + " by " + str(down_bound)
	
	solution = []

	temp = dfs_search(mapname)
	if temp != None: 
		print 'SUCCESS!'
		print 'End located at: (' + str(temp.x ) + ", " + str(temp.y)  + ")"

		#while(temp!= None):
		#print 'path: ' + str(temp.x) + ", " + str(temp.y)

		while(temp != None):
			print temp.x, temp.y
			solution.append ((temp.x, temp.y))
			temp = temp.parent

	#print solution
	draw_solution(mapname, solution)
	print "Solution drawn to " + mapname[:-4] + "test.txt"

if __name__ == "__main__":
	main("mediumMaze.txt")

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
# Namely used to verify we read in text file correctly.
def write_test_map(mapname):
	maze = read_map(mapname)

	with open(mapname, 'w') as outFile:
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
		return root ##return solution
	
	frontier = deque([])
	#frontier.append(node)
	frontier.append((node.x, node.y))
	
	explored = {}
	while 1:
		if len(frontier) == 0:
			return None
		#node = frontier.popleft()
		node = frontier.popleft()
		#cur_x = node.x 
		#cur_y = node.y
		cur_x = node[0]
		cur_y = node[1]

		explored[(cur_x, cur_y)]= cur_x + cur_y
		#explored[node] = node.x + node.y

		#if can move right, move right
		if cur_x < right_bound and maze[cur_y][0][cur_x+1]!= '%': 
			child = Node(cur_x + 1, cur_y, 0) #initialize child node
			#child.parent = node
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:	
				if (child.x == x_end and child.y == y_end):
					return child
				#frontier.append(child)
				frontier.append((child.x, child.y))

		#if can move down, move down
		if cur_y < down_bound and maze[cur_y + 1][0][cur_x]!= '%': 
			child = Node(cur_x, cur_y + 1, 1)#initialize child node
			#child.parent = node
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				#frontier.append(child)
				frontier.append((child.x, child.y))

		#if can move up, move up
		if cur_y > 0 and maze[cur_y - 1][0][cur_x]!= '%':
			child = Node(cur_x, cur_y - 1, 2) #initialize child node
			#child.parent = node
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				#frontier.append(child)	
				frontier.append((child.x, child.y))

		#if can move left, move left
		if cur_y > 0 and maze[cur_y][0][cur_x-1]!= '%': 
			child = Node(cur_x - 1, cur_y, 3) #initialize child node
			#child.parent = node
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return child
				#frontier.append(child)
				frontier.append((child.x, child.y))
	return None 

def dfs_search(mapname): 
	maze = read_map(mapname)

	node = Node(x_start, y_start, None)
	cur_x = x_start
	cur_y = y_start

	if(node.x == x_end and node.y == y_end):
		return root ##return solution
	
	stackX = []
	stackY = []
	stackX.append(node.x)
	stackY.append(node.y)

	explored = {}

	while 1:
		if len(stackX) and len(stackY) == 0:
			return None
		
		node = stackX.pop()
		
		

# Main function
def main():
	maze= read_map("openMaze.txt")
	#write_test_map("tinySearch_test.txt")

	for line in maze:
		for s in line: 
			print s

	find_start_end("openMaze.txt")
	print "START COORDINATES:" + str(x_start) + ", " + str(y_start)
	print right_bound 
	print down_bound
	
	temp = bfs_search("openMaze.txt")
	if temp != None: 
		print 'SUCCESS!'
		print 'End located at: ' + str(temp.x ) + ", " + str(temp.y) 

if __name__ == "__main__":
	main()
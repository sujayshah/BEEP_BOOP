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
	#cost = 0 
	cur_x = x_start
	cur_y = y_start

	if(node.x == x_end and node.y == y_end):
		#return root ##return solution
		return 'root'
	
	#frontier = Queue.Queue()
	frontier = deque([])
	frontier.append(node)

	explored = {}
	while frontier: #temporary loop 
		if len(frontier) == 0:
			return None
		node = frontier.popleft()
		cur_x = node.x 
		cur_y = node.y
		explored[node] = node.x + node.y

		#if can move right, move right
		if cur_x < right_bound and maze[cur_y][0][cur_x+1]!= '%': 
			child = Node(cur_x + 1, cur_y, 0) #initialize child node
			child.parent = node
			if child not in explored and child not in frontier: #if child not in explored/frontier
				#check if child is goal 
				if (child.x == x_end and child.y == y_end):
					return child
					print 'right'
				#insert child to frontier
				frontier.append(child)

		#if can move down, move down
		if cur_y < down_bound and maze[cur_y+1][0][cur_x]!= '%': 
			child = Node(cur_x, cur_y + 1, 1)#initialize child node
			child.parent = node
			if child not in explored and child not in frontier: #if child not in explored/frontier
				#check if child is goal 
				if (child.x == x_end and child.y == y_end):
					return child
					print 'down'
				#insert child to frontier
				frontier.append(child)

		#if can move up, move up
		if cur_y > 0 and maze[cur_y-1][0][cur_x]!= '%':  
			child = Node(cur_x, cur_y - 1, 2) #initialize child node
			child.parent = node
			if child not in explored and child not in frontier: #if child not in explored/frontier
				#check if child is goal 
				if (child.x == x_end and child.y == y_end):
					return child
					print 'up'
				#insert child to frontier
				frontier.append(child)

		#if can move left, move left
		if cur_y > 0 and maze[cur_y][0][cur_x-1]!= '%': 
			child = Node(cur_x - 1, cur_y, 3) #initialize child node
			child.parent = node
			if child not in explored and child not in frontier: #if child not in explored/frontier
				#check if child is goal 
				if (child.x == x_end and child.y == y_end):
					return child
					print 'left'
				#insert child to frontier
				frontier.append(child)
	return None 

# Main function
def main():
	maze= read_map("mediumMaze.txt")
	#write_test_map("tinySearch_test.txt")

	for line in maze:
		for s in line: 
			print s

	find_start_end("mediumMaze.txt")
	print "START COORDINATES:" + str(x_start) + ", " + str(y_start)
	print right_bound 
	print down_bound
 	#print "PRINTING CHARACTER: "
	#print maze[21][0][1]
	#print maze[21][0][2]
	
	temp = bfs_search("mediumMaze.txt")
	if temp != None: 
		print 'SUCCESS'

if __name__ == "__main__":
	main()
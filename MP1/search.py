import Queue
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

	root = Node(x_start, y_start)
	cost = 0 
	cur_x = 0 
	cur_y = 0 

	if(root.x == x_end and root.y == y_end):
		return root ##return solution
	
	frontier = Queue.Queue()
	frontier.put(root)

	explored = []
	while not frontier.empty(): #temporary loop 
		if frontier.empty():
			return None
		node = frontier.get()
		explored.append(node)

		#if can move right, move right
		#if x_start 




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
	
	#bfs_search("mediumMaze.txt")

if __name__ == "__main__":
	main()
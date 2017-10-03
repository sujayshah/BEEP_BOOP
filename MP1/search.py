from collections import deque
from node import Node
import heapq
import string as stringz

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
# marked as '.' Returns a list of '.''
def find_start_end(mapname):
	maze = read_map(mapname)
	global x_start 
	global y_start
	global x_end 
	global y_end
	global right_bound
	global down_bound
	fruit = []

	for ypos, line in enumerate(maze):
		for string in line:
			for xpos, char in enumerate(string):
				if char == 'P':
					x_start = xpos
					y_start = ypos 
				if char == '.':
					x_end = xpos 
					y_end = ypos
					fruit.append((xpos, ypos))
			right_bound = xpos
		down_bound = ypos
	return fruit					

def heuristic(point1, point2):
	x1 = point1[0]
	y1 = point1[1]

	x2= point2[0]
	y2= point2[1]

	manhattan_distance = abs(x1 - x2) + abs(y1 - y2)

	return manhattan_distance

# This function conducts a BFS search of the maze. Returns pointer to 
# last solution node and total step cost as a tuple (node, cost).
def bfs_search(mapname, infruit): 
	maze = read_map(mapname)

	cost = 0 
	expansion_counter = 0
	fruit = infruit

	node = Node(x_start, y_start, fruit)
	cur_x = x_start
	cur_y = y_start

	#if(node.x == x_end and node.y == y_end):
	#	return (node, cost)
	if(not node.state):
		print "No more fruit left"
		return (node, cost)

	
	frontier = deque([])
	frontiernode = deque([])

	frontier.append((node.x, node.y))
	frontiernode.append(node)
	
	explored = {}
	while 1:
		if len(frontier) == 0:
			return (None, cost, expansion_counter)

		node = frontier.popleft()
		nodenode = frontiernode.popleft()

		cur_x = node[0]
		cur_y = node[1]

		explored[(cur_x, cur_y)]= cur_x + cur_y

		# if can move right, move right
		# state should be represented by tuple: (position, fruit left)
		# goal check should be if fruit list is empty 
		if cur_x < right_bound and maze[cur_y][0][cur_x+1]!= '%': 
			child = Node(cur_x + 1, cur_y, 0) #initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:	
				if (child.x == x_end and child.y == y_end):
					return (child, cost, expansion_counter)
				frontier.append((child.x, child.y))
				frontiernode.append(child)
				#print "Adding: " + str(child.x) + ", " + str(child.y)

		#if can move down, move down
		if cur_y < down_bound and maze[cur_y + 1][0][cur_x]!= '%': 
			child = Node(cur_x, cur_y + 1, 1)#initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return (child, cost, expansion_counter)
				frontier.append((child.x, child.y))
				frontiernode.append(child)
				#print "Adding: " + str(child.x) + ", " + str(child.y)

		#if can move up, move up
		if cur_y > 0 and maze[cur_y - 1][0][cur_x]!= '%':
			child = Node(cur_x, cur_y - 1, 2) #initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return (child, cost, expansion_counter)
				frontier.append((child.x, child.y))
				frontiernode.append(child)
				#print "Adding: " + str(child.x) + ", " + str(child.y)

		#if can move left, move left
		if cur_x > 0 and maze[cur_y][0][cur_x-1]!= '%': 
			child = Node(cur_x - 1, cur_y, 3) #initialize child node
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				if (child.x == x_end and child.y == y_end):
					return (child, cost, expansion_counter)
				frontier.append((child.x, child.y))
				frontiernode.append(child)
				#print "Adding: " + str(child.x) + ", " + str(child.y)
	return (None, cost, expansion_counter)

# This function conducts a dfs search of the maze. Returns pointer to 
# last solution node and total step cost as a tuple (node, cost).
def dfs_search(mapname):
	maze = read_map(mapname)

	cost = 0 
	expansion_counter = 0 

	node = Node(x_start, y_start, None)
	cur_x = x_start 
	cur_y = y_start

	if(cur_x == x_end and cur_y == y_end):
		return (node, cost, expansion_counter)

	frontier = deque([]) #stack of (x, y) coordinates
	frontiernode = deque([]) #stack of nodes
	explored = {} #explored stack

	frontier.append((node.x, node.y)) #add (x_start, y_start)
	frontiernode.append(node) #add root node
	
	# note about deque: peek at leftmost item = deque[0]
	# peek at rightmost item = deque[-1]
	while len(frontier) > 0:
		#print "Before popping, stack looks like: " + str(frontier)
		#print "Before popping, top of stack is: " + str(frontier[-1][0]) + ", " + str(frontier[-1][1])
		nodenode = frontiernode.pop()
		node = frontier.pop()
		cur_x = node[0]
		cur_y = node[1]

		#print "Looking at " +  str(cur_x) + ", " + str(cur_y) + " with action " + str(nodenode.action)

		if (cur_x == x_end and cur_y == y_end):
			return (nodenode, cost, expansion_counter)

		explored[(cur_x, cur_y)]= cur_x + cur_y

		#expand node
		if cur_x < right_bound and maze[cur_y][0][cur_x+1]!= '%': 
			child = Node(cur_x + 1, cur_y, 0) 
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				#print "APPENDING RIGHT: " + str(child.x) + ", " + str(child.y)
				frontier.append((child.x, child.y))
				frontiernode.append(child)

		if cur_y < down_bound and maze[cur_y + 1][0][cur_x]!= '%':  
			child = Node(cur_x, cur_y + 1, 1) 
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				#print "APPENDING DOWN: " + str(child.x) + ", " + str(child.y)
				frontier.append((child.x, child.y))
				frontiernode.append(child)
	
		if cur_y > 0 and maze[cur_y-1][0][cur_x]!= '%': 
			child = Node(cur_x, cur_y - 1, 2) 
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				#print "APPENDING UP: " + str(child.x) + ", " + str(child.y)
				frontier.append((child.x, child.y))
				frontiernode.append(child)

		if cur_x > 0 and maze[cur_y][0][cur_x-1]!= '%':  
			child = Node(cur_x - 1, cur_y, 3) 
			child.parent = nodenode
			if (child.x, child.y) not in explored and (child.x, child.y) not in frontier:
				#print "APPENDING LEFT: " + str(child.x) + ", " + str(child.y)
				frontier.append((child.x, child.y))
				frontiernode.append(child)
	return (None, cost)

def aStar_search(mapname, startNode, endNode):
	maze = read_map(mapname)

	node = startNode
	cur_x = startNode.x
	cur_y = startNode.y

	x_end = endNode.x
	y_end = endNode.y

	if(cur_x == x_end and cur_y == y_end):
		return node 

	frontier = []
	frontierloc = deque([])
	explored= {}
	cost = 0

	heapq.heappush(frontier, (cost, node))
	

	while len(frontier) > 0:

		# print frontier
		temp = heapq.heappop(frontier)
		node = temp[1]
		cur_x = node.x
		cur_y = node.y
		#print node

		cost+=1

		explored[(node.x, node.y)] = node.x + node.y
		
		downcost = -1
		upcost = -1
		rightcost = -1
		leftcost = -1

		if cur_x < right_bound and maze[cur_y][0][cur_x + 1]!= '%': 
			rightnode = Node(cur_x+1, cur_y, None)
			rightnode.parent = node
			rightcost = aStar_heuristic(cost, manhattan_dist(cur_x+1, x_end, cur_y, y_end))

			if(rightnode.x, rightnode.y) not in explored and (rightnode.x, rightnode.y) not in frontierloc:
				if rightnode.x == x_end and rightnode.y == y_end:
					return (rightnode, cost)
				heapq.heappush(frontier, (rightcost, rightnode))
				frontierloc.append((rightnode.x, rightnode.y))


		if cur_y < down_bound and maze[cur_y + 1][0][cur_x]!= '%':
			downnode = Node(cur_x, cur_y+1, None)
			downnode.parent = node
			downcost = aStar_heuristic(cost, manhattan_dist(cur_x, x_end, cur_y+1, y_end))

			if(downnode.x, downnode.y) not in explored and (downnode.x, downnode.y) not in frontierloc:
				if downnode.x == x_end and downnode.y == y_end:
					return (downnode, cost)
				heapq.heappush(frontier, (downcost, downnode))
				frontierloc.append((downnode.x, downnode.y))


		if cur_y > 0 and maze[cur_y - 1][0][cur_x]!= '%':
			upnode = Node(cur_x, cur_y-1, None)
			upnode.parent = node
			upcost = aStar_heuristic(cost, manhattan_dist(cur_x, x_end, cur_y-1, y_end))

			if(upnode.x, upnode.y) not in explored and (upnode.x, upnode.y) not in frontierloc:
				if upnode.x == x_end and upnode.y == y_end:
					return (upnode, cost)
				heapq.heappush(frontier, (upcost, upnode))
				frontierloc.append((upnode.x, upnode.y))
		


		if cur_x > 0 and maze[cur_y][0][cur_x-1]!= '%':
			leftnode = Node(cur_x-1, cur_y, None)
			leftnode.parent = node
			downcost = aStar_heuristic(cost, manhattan_dist(cur_x-1, x_end, cur_y, y_end))

			if(leftnode.x, leftnode.y) not in explored and (leftnode.x, leftnode.y) not in frontierloc:
				if leftnode.x == x_end and leftnode.y == y_end:
					return (leftnode, cost)
				heapq.heappush(frontier, (leftcost, leftnode))
				frontierloc.append((leftnode.x, leftnode.y))

	return None

def aStar_heuristic(cost, dist):
	return cost+dist

def manhattan_dist(x1, x2, y1, y2):
	dist = abs(x1 - x2) - (y1 - y2)
	return dist

def closest_real_dist_heuristic(mapname, fruitList):
	node = Node(x_start, y_start, None)
	cur_x = node.x
	cur_y = node.y
	nextNode = None
	
	order_fruit = []
	while len(fruitList) != 0:
		cost = 0
		for x in range(len(fruitList)):
			food_x = fruitList[x][0]
			food_y = fruitList[x][1]
			fruitNode = Node(food_x, food_y, None) 
			returnFruitCost = aStar_search(mapname, node, fruitNode)
			if returnFruitCost != None: 
				if x == 0 or returnFruitCost[1] < cost:
					cost = returnFruitCost[1]
					nextNode = returnFruitCost[0]
					# print nextNode.x, nextNode.y, cost
			else:
				return None
			
			cur_x = food_x
			cur_y = food_y
		if (nextNode.x, nextNode.y) in fruitList:
			print nextNode.x, nextNode.y
			fruitList.remove((nextNode.x, nextNode.y)) 
			order_fruit.append((nextNode.x, nextNode.y))
			#maze[nextNode.y][0][nextNode.x] = 'A' # temporarily mark the fruit

	return order_fruit


# This function conducts a greedy best-first search of the maze. Returns pointer
# to last solution node and total path cost as a tuple (node, cost). 
def greedybfs_search(mapname):
	maze = read_map(mapname)

	node = Node(x_start, y_start, None)
	cur_x = node.x 
	cur_y = node.y

	if(node.x == x_end and node.y == y_end):
		return node

	frontier= []
	frontierloc = deque([])
	explored= {}
	cost = 0

	heapq.heappush(frontier, (0, node))
	heapq.heappush(frontier,(100000, node)) #here so we can compile

	while len(frontier) > 1:
		temp = heapq.heappop(frontier)
		node = temp[1]
		cost += temp[0]
		#print 'Just popped: ' + str(node.x) + ", " + str(node.y)
		explored[(node.x, node.y)] = node.x + node.y

		if node.x == x_end and node.y == y_end:
			return node

		cur_x = node.x 
		cur_y = node.y
		#right
		if cur_x < right_bound and maze[cur_y][0][cur_x + 1]!= '%':
			#print 'Examining: ' + str(cur_x) + ", " + str(cur_y)
			rightnode = Node(cur_x + 1, cur_y, 0)
			rightnode.parent = node
			rightcost = heuristic((cur_x + 1, cur_y), (x_end, y_end))

			if(rightnode.x, rightnode.y) not in explored and (rightnode.x, rightnode.y) not in frontierloc:
				if rightnode.x == x_end and rightnode.y == y_end:
					return (rightnode, cost)
				heapq.heappush(frontier, (rightcost, rightnode))
				frontierloc.append((rightnode.x, rightnode.y))
				#print 'Pushing: ' + str(rightnode.x) + ", " + str(rightnode.y)

		#down
		if cur_y < down_bound and maze[cur_y + 1][0][cur_x]!= '%':
			#print 'Examining: ' + str(cur_x) + ", " + str(cur_y)
			downnode = Node(cur_x, cur_y + 1, 1)
			downnode.parent = node
			downcost = heuristic((cur_x, cur_y + 1), (x_end, y_end))

			if(downnode.x, downnode.y) not in explored and (downnode.x, downnode.y) not in frontierloc:
				if downnode.x == x_end and downode.y == y_end:
					return (downnode, cost)
				heapq.heappush(frontier, (downcost, downnode))
				frontierloc.append((downnode.x, downnode.y))
				#print 'Pushing: ' + str(downnode.x) + ", " + str(downnode.y)
		#up
		if cur_y > 0 and maze[cur_y - 1][0][cur_x]!= '%':
			#print 'Examining: ' + str(cur_x) + ", " + str(cur_y)
			upnode = Node(cur_x, cur_y - 1, 2)
			upnode.parent = node
			upcost = heuristic((cur_x, cur_y - 1), (x_end, y_end))

			if(upnode.x, upnode.y) not in explored and (upnode.x, upnode.y) not in frontierloc:
				if upnode.x == x_end and upnode.y == y_end:
					return (upnode, cost)
				heapq.heappush(frontier, (upcost, upnode))
				frontierloc.append((upnode.x, upnode.y))
				#print 'Pushing: ' + str(upnode.x) + ", " + str(upnode.y)

		#left
		if cur_y > 0 and maze[cur_y][0][cur_x - 1]!= '%':
			#print 'Examining: ' + str(cur_x) + ", " + str(cur_y)
			leftnode = Node(cur_x - 1, cur_y, 3)
			leftnode.parent = node
			leftcost = heuristic((cur_x - 1, cur_y), (x_end, y_end))

			if(leftnode.x, leftnode.y) not in explored and (leftnode.x, leftnode.y) not in frontierloc:
				if leftnode.x == x_end and leftnode.y == y_end:
					return (leftnode, cost)
				heapq.heappush(frontier, (leftcost, leftnode))
				frontierloc.append((leftnode.x, leftnode.y))
				#print 'Pushing: ' + str(leftnode.x) + ", " + str(leftnode.y)


# This function draws the solution on the input maze. 		
def draw_solution(mapname, solution_path):
	maze = read_map(mapname)
	writemap = mapname[:-4] + "test.txt" 

	with open(writemap, 'w') as outFile:
		for ypos, line in enumerate(maze): 
			for string in line:
				for xpos, char in enumerate(string):
					if (xpos, ypos) in solution_path and (xpos, ypos)!= (x_start, y_start): 
						#print (xpos, ypos)
						#print solution_path.index((xpos,ypos))
						#return
						outFile.write(stringz.printable[solution_path.index((xpos, ypos))])
				 	else:
						outFile.write(char)
			outFile.write('\n')

# Main function
def main(mapname):
	maze= read_map(mapname)

	for line in maze:
		for s in line: 
			print s

	fruit = []
	fruit = find_start_end(mapname)
	print "START COORDINATES: (" + str(x_start) + ", " + str(y_start) + ")"
	print "DIMENSIONS: " + str(right_bound) + " by " + str(down_bound)
	print "END COORDINATES: (" + str(x_end) + ", " + str(y_end) + ")"
	
	solution = []

	#temp2 = dfs_search(mapname)
	#temp = temp2[0]
	#cost = temp2[1]
	#counter = temp2[2]
	
	# temp2 = aStar_search(mapname)

	fruitList = fruit
	temp2 = closest_real_dist_heuristic(mapname, fruitList)
	

	#print solution
	#print "COST: " + str(cost)
	#print "NUMBER OF EXPANDED NODES: " + str(counter)
	print "Fruit:" + str(fruit)
	draw_solution(mapname, temp2)
	print "Solution drawn to " + mapname[:-4] + "test.txt"

if __name__ == "__main__":

	main("mediumSearch.txt")

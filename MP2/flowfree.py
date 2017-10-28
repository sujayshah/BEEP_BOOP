from variable import Variable
import random
from Queue import PriorityQueue

def readFile(filename):
	textFile = open(filename, "r")
	flowFreeMap = []

	for line in textFile:
		flowFreeMap.append(line.strip().split('\r\n '))

	textFile.close()

	return flowFreeMap

def smart_csp_search(grid, colorList, colorLoc, cellList, colorPaths, nextStates):
	for z in range(0, len(grid)):
		print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z]))) 

	print colorPaths

	for i in range(0, len(colorList)):
		print "COLORS", colorList[i]
		most_constrained_var(grid, i, colorList, colorLoc, colorPaths, nextStates)
		print "NEXTSTATES", nextStates.queue

	while not nextStates.empty():
		curAssign = nextStates.get()
		curDist = curAssign[1][0]
		curX = curAssign[1][1]
		curY = curAssign[1][2]
		curVal = curAssign[1][3]
		print "CUR ASSIGN", curAssign

	# grid[curY][curX].assignment = curVal
	# grid[curY][curX].state = 2

	# for z in range(0, len(grid)):
	# 	print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z])))


# This function finds the availability of different paths through neighboring cells
def most_constrained_var(grid, i, colorList, colorLoc, colorPaths, nextStates):
	colorX = colorPaths.get(colorList[i]+'x')[-1] #get current location of path
	colorY = colorPaths.get(colorList[i]+'y')[-1]
	up = down = left = right = False
	numOpen = 0
	if colorX > 0:
		if grid[colorY][colorX-1].assignment == ' ':
			numOpen += 1
			left = True
	if colorX < (len(grid[colorY])-1):
		if grid[colorY][colorX+1].assignment == ' ':
			numOpen += 1
			right = True
	if colorY > 0:
		if grid[colorY-1][colorX].assignment == ' ':
			numOpen += 1
			up = True
	if colorY < (len(grid)-1):
		if grid[colorY+1][colorX].assignment == ' ':
			numOpen += 1
			down = True

	if left:
		nextStates.put((numOpen, (manhattan_distance_ordering(colorList[i], colorLoc, colorX-1, colorY), colorX-1, colorY, colorList[i])))
	if right:
		nextStates.put((numOpen, (manhattan_distance_ordering(colorList[i], colorLoc, colorX+1, colorY), colorX+1, colorY, colorList[i])))
	if up:
		nextStates.put((numOpen, (manhattan_distance_ordering(colorList[i], colorLoc, colorX, colorY-1), colorX, colorY-1, colorList[i])))
	if down:
		nextStates.put((numOpen, (manhattan_distance_ordering(colorList[i], colorLoc, colorX, colorY+1), colorX, colorY+1, colorList[i])))

def manhattan_distance_ordering(i, colorLoc, x, y):
	endPath = colorLoc.get(i+'End')
	return abs(endPath[0]-x) + abs(endPath[1]-y)


# def zig_zag_check(grid, x, y):
# def forward_checking():

##################################################################
def iterative_count():
	global iterations
	iterations = 0

def increment_count():
	global iterations
	iterations += 1

def dumb_csp_search(grid, colorList, colorLoc, cellList):
	increment_count()
	print "ITERATIONS", iterations
	if iterations >= 1000:
		return -1
	for z in range(0, len(grid)):
		print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z])))
	# raw_input("Press Enter")
	allPathsFound = True
	for i in colorList:
		startPath = colorLoc.get(i+'Start')
		endPath = colorLoc.get(i+'End')
		if (findPath(grid, grid[startPath[1]][startPath[0]], grid[endPath[1]][endPath[0]]) == None):
			allPathsFound = False

	for i in range(0, len(grid)):
		for var in grid[i]:
			if(var.state == 0):
				allPathsFound = False

	if allPathsFound == True:
		return grid

	for cell in cellList:
		print "SPACE COORDS ", cell.x, cell.y, cell.domain
		for newAssign in cell.domain:
			if(cell.state == 0):
				print "NEWASSIGN ", newAssign
				cell.assignment = newAssign
				cell.state = 2
				if neighbors(grid, cell, newAssign, colorLoc):
					result = dumb_csp_search(grid, colorList, colorLoc, cellList)
					print "SPACE RETURN", cell.x, cell.y
					print " "
					if(result == -1):
						return -1
					if(result != None):
						return result
				cell.assignment = ' '
				cell.state = 0
				print "Newassign on fail", newAssign, cell.domain[-1]
				if newAssign == cell.domain[-1]:
					return None

	print "FAILED TO FIND VAR"
	print " "		
	return None
	# print space.x, space.y, space.assignment, space.domain, space.state

def neighbors(grid, space, newAssign, colorLoc):
	if (numNeighbors(grid, space, newAssign, colorLoc)):
		if(space.x > 0):
			print "LEFT", (grid[space.y][space.x-1]).assignment
			if(grid[space.y][space.x-1].assignment == newAssign):
				if(numNeighbors(grid, grid[space.y][space.x-1], newAssign, colorLoc) == False):
					return False
	
		if(space.x < len(grid)-1):
			print "RIGHT", (grid[space.y][space.x+1]).assignment
			if(grid[space.y][space.x+1].assignment == newAssign):
				if(numNeighbors(grid, grid[space.y][space.x+1], newAssign, colorLoc) == False):
					return False

		if(space.y > 0):
			print "UP", (grid[space.y-1][space.x]).assignment
			if(grid[space.y-1][space.x].assignment == newAssign):
				if(numNeighbors(grid, grid[space.y-1][space.x], newAssign, colorLoc) == False):
					return False

		if(space.y < len(grid)-1):
			print "DOWN", (grid[space.y+1][space.x]).assignment
			if(grid[space.y+1][space.x].assignment == newAssign):
				if(numNeighbors(grid, grid[space.y+1][space.x], newAssign, colorLoc) == False):
					return False

		return True

	return False
	
def numNeighbors(grid, space, newAssign, colorLoc):
	numNeighbors = 0
	if(space.x > 0):
		if(grid[space.y][space.x-1].assignment == newAssign):
			numNeighbors += 1
	
	if(space.x < len(grid)-1):
		if(grid[space.y][space.x+1].assignment == newAssign):
			numNeighbors += 1

	if(space.y > 0):
		if(grid[space.y-1][space.x].assignment == newAssign):
			numNeighbors += 1

	if(space.y < len(grid)-1):
		if(grid[space.y+1][space.x].assignment == newAssign):
			numNeighbors += 1

	print "numNeighbors", numNeighbors
	if ((colorLoc.get(newAssign + 'Start') == (space.x, space.y)) or (colorLoc.get(newAssign + 'Start') == (space.x, space.y))): 
		return (numNeighbors <= 1)

	return (numNeighbors <= 2)

##################################################################
def findPath(grid, start, goal):
	path = []
	visited = []
	valid = 0

	if (start.x < 0) or (start.y < 0) or (start.x >= len(grid)) or (start.y >= len(grid[0])) or start.assignment == ' ':
		return None
	if(start.x == goal.x and start.y == goal.y):
		return path

	path.append(start)
	visited.append((start.x, start.y))

	while (start.x != goal.x or start.y != goal.y):
		x = start.x
		y = start.y
		if start.x > 0 and (x-1, y) not in visited:
			if (grid[y][x-1]).assignment == start.assignment:
				path.append(grid[y][x-1])
				visited.append((x-1, y))
				valid += 1 

		if start.x < len(grid)-1 and (x+1, y) not in visited:
			if (grid[y][x+1]).assignment == start.assignment:
				path.append(grid[y][x+1])
				visited.append((x+1, y))
				valid += 1

		if start.y > 0 and (x, y-1) not in visited:
			if (grid[y-1][x]).assignment == start.assignment:
				path.append(grid[y-1][x])
				visited.append((x, y-1))
				valid += 1

		if start.y < len(grid)-1 and (x, y+1) not in visited:
			if (grid[y+1][x]).assignment == start.assignment:
				path.append(grid[y+1][x])
				visited.append((x, y+1))
				valid += 1

		if(valid != 1):
			return None

		valid = 0
		start = path[-1]

	return path


def main(filename):
	flowFree = readFile(filename)
	colorList = []
	cellList = []
	colorLoc = {}
	grid = []
	y = 0
	for line in flowFree:
		for s in line: 
			grid2 = []
			print s
			for c in range(0,len(s)):
				if s[c] not in colorList and s[c] != '_':
					colorList.append(s[c])
					colorLoc[s[c]+'Start'] = (c, y)
				
				if s[c] == '_':
					var = Variable(c, y, ' ', None, None)
					var.domain = colorList
					var.state = 0
					cellList.append(var)

				else:
					var = Variable(c, y, s[c], None, None)
					var.domain.append(s[c])
					var.state = 1
					colorLoc[s[c]+'End'] = (c, y)

				grid2.append(var)
			
			grid.append(grid2)
			y+=1
				
	print colorList
	print colorLoc
	

# Reserved for testing solution path// DO NOT UNCOMMENT -- Call in other functions if needed
#-------------------------------------------------------------------------
	# filename = "output55.txt"
	# flowFree = readFile(filename)
	# grid = []
	# y = 0
	# for line in flowFree:
	# 	for s in line: 
	# 		grid2 = []
	# 		print s
	# 		for c in range(0,len(s)):
	# 			if s[c] == '_':
	# 				var = Variable(c, y, ' ', None, None)
	# 				var.domain = colorList
	# 				var.state = 0
	# 			else:
	# 				var = Variable(c, y, s[c], None, None)
	# 				var.domain.append(s[c])
	# 				var.state = 1

	# 			grid2.append(var)
			
	# 		grid.append(grid2)
	# 		y+=1

	# allPathsFound = True
	# for i in colorList:
	# 	startPath = colorLoc.get(i+'Start')
	# 	endPath = colorLoc.get(i+'End')
	# 	if (findPath(grid, grid[startPath[1]][startPath[0]], grid[endPath[1]][endPath[0]]) == None):
	# 		allPathsFound = False

	# print allPathsFound
#--------------------------------------------------------------------------

# UNCOMMENT THESE LINES TO RUN DUMB CSP SOLVER 
	# random.shuffle(cellList)
	# for i in cellList:
	# 	i.domain = []
	# 	for z in colorList:
	# 		i.domain.append(z)
	# 	random.shuffle(i.domain)
	# 	print i.x, i.y, i.domain
	# iterative_count()
	# dumb_csp_search(grid, colorList, colorLoc, cellList)
#---------------------------------------------------------------------------
# UNCOMMENT THESE LINES TO RUN SMART CSP SOLVER 
	nextStates = PriorityQueue()
	colorPaths = {}
	for i in colorList:
		colorStart = colorLoc.get(i+'Start')
		colorPaths[i+'x'] = []
		colorPaths[i+'y'] = []
		colorPaths[i+'x'].append(colorStart[0])
		colorPaths[i+'y'].append(colorStart[1])
	smart_csp_search(grid, colorList, colorLoc, cellList, colorPaths, nextStates)

#----------------------------------------------------------------------------	
	foundPath = True
	for i in colorList:
		startPath = colorLoc.get(i+'Start')
		endPath = colorLoc.get(i+'End')
		if (findPath(grid, grid[startPath[1]][startPath[0]], grid[endPath[1]][endPath[0]]) == None):
			foundPath = False
	if foundPath:
		print "SOLUTION FOUND"
		for z in range(0, len(grid)):
			print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z])))
		return grid
	else:
		print "FAILED TO FIND SOLUTION"
		return None

if __name__ == "__main__" : 
	main("input77.txt")

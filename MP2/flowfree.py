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

def smart_csp_search(grid, colorList, colorLoc, colorPaths):
	# raw_input("Enter")
	# print out the current maze	
	for z in range(0, len(grid)):
		print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z]))) 
	print " "
	print colorPaths
	
	# raw_input("Press enter")
	# check whether a valid solution is found that satisfy...
	# 1) All colors from their starting cell have a clear path to the solution with no branching
	allPathsFound = True
	for i in colorList:
		startPath = colorLoc.get(i+'Start')
		endPath = colorLoc.get(i+'End')
		if (findPath(grid, grid[startPath[1]][startPath[0]], grid[endPath[1]][endPath[0]]) == None):
			allPathsFound = False
	# 2) All cells have been filled in
	for i in range(0, len(grid)):
		for var in grid[i]:
			if(var.state == 0):
				allPathsFound = False
	# Return the grid if a solution has been found recursively
	if allPathsFound == True:
		return grid
	
	# Use this to add the next constrined variables to the priority queue
	nextStates = PriorityQueue();
	successorList = []
	for i in range(0, len(colorList)):
		currentX = colorPaths[colorList[i]+'x'][-1]
		currentY = colorPaths[colorList[i]+'y'][-1]
		successorList.append([])
		successorList[i] = most_constrained_var(grid, currentX, currentY, colorList[i], colorLoc, nextStates)
		# print "SUCCESSORS", successorList[i]
		if successorList[i]:
			for j in range(0, len(successorList[i])):
				nextStates.put((len(successorList[i]), successorList[i][j]))
		# print "Queue", (nextStates.queue)

	if nextStates.empty():
		return None	

	# Pick the next cell to expand from the priority queue according to whichever cell variable is most constrained in priority queue 
	# and has best value according to manhattan distance from goal heuristic
	while not nextStates.empty():
		curAssign = nextStates.get()
		curDir = curAssign[1][0]
		curDist = curAssign[1][1]
		curVal = curAssign[1][2]
		print "Queue", (nextStates.queue)
		assignX = colorPaths[curVal+'x'][-1]
		assignY = colorPaths[curVal+'y'][-1]
		appendedColor = False

		if curDir == 'L':
			nextX = assignX-1
			nextY = assignY
		elif curDir == 'R':
			nextX = assignX+1
			nextY = assignY
		elif curDir == 'U':
			nextX = assignX
			nextY = assignY-1
		elif curDir == 'D':
			nextX = assignX
			nextY = assignY+1
		assignedCell = grid[nextY][nextX]
		assignedCell.assignment = curVal
		assignedCell.state = 2
		pathCheck = True
		for a in range(0, len(colorPaths[curVal+'x'])):
			if neighbors(grid, assignedCell, curVal, colorLoc) == False or squareCheck(grid, assignedCell) == False:
				pathCheck = False
		
		if pathCheck and forward_checking(grid, colorList):	
			colorPaths[curVal+'x'].append(nextX)
			colorPaths[curVal+'y'].append(nextY)

			returnVal = smart_csp_search(grid, colorList, colorLoc, colorPaths)

			if(returnVal != None):
				return grid

			colorPaths[curVal+'x'] = colorPaths[curVal+'x'][:-1]
			colorPaths[curVal+'y'] = colorPaths[curVal+'y'][:-1]
		
		assignedCell.assignment = '_'
		assignedCell.state = 0

		for z in range(0, len(grid)):
			print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z])))
		print " "

# 	# del successorList[:]
# 	# print successorList
# 	# for z in range(0, len(grid)):
# 	# 	print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z])))
# 	# print " "



# # This function finds the availability of different paths through neighboring cells
def most_constrained_var(grid, x, y, colorVal, colorLoc, nextStates):
	successorList = []
	numOpen = 0
	mdL = mdR = mdU = mdD = -1
	up = down = left = right = False
	if x > 0:
		if grid[y][x-1].assignment == '_':
			numOpen += 1
			left = True
			mdL = manhattan_distance_ordering(grid[y][x].assignment, colorLoc, x-1, y)
		elif grid[y][x-1].assignment == grid[y][x].assignment:
			if colorLoc[grid[y][x].assignment+'End'] == (x-1, y):
				return
	if x < len(grid[y])-1:
		if grid[y][x+1].assignment == '_':
			numOpen += 1
			right = True
			mdR = manhattan_distance_ordering(grid[y][x].assignment, colorLoc, x+1, y)
		elif grid[y][x+1].assignment == grid[y][x].assignment:
			if colorLoc[grid[y][x].assignment+'End'] == (x+1, y):
				return
	if y > 0:
		if grid[y-1][x].assignment == '_':
			numOpen += 1
			up = True
			mdU = manhattan_distance_ordering(grid[y][x].assignment, colorLoc, x, y-1)
		elif grid[y-1][x].assignment == grid[y][x].assignment:
			if colorLoc[grid[y][x].assignment+'End'] == (x, y-1):
				return
	if y < len(grid)-1:
		if grid[y+1][x].assignment == '_':
			numOpen += 1
			down = True
			mdD = manhattan_distance_ordering(grid[y][x].assignment, colorLoc, x, y+1)
		elif grid[y+1][x].assignment == grid[y][x].assignment:
			if colorLoc[grid[y][x].assignment+'End'] == (x, y+1):
				return

	successors = []
	if mdL >= 0:
		successors.append(('L', mdL, colorVal))
	if mdR >= 0:
		successors.append(('R', mdR, colorVal))
	if mdU >= 0:
		successors.append(('U', mdU, colorVal))
	if mdD >= 0:
		successors.append(('D', mdD, colorVal))

	while successors:
		minDist = successors[0][1]
		minDir =  successors[0][0]
		for i in range(0, len(successors)):
			if successors[i][1] < minDist:
				minDist = successors[i][1]
				minDir =  successors[i][0]
		successorList.append(successors[successors.index((minDir, minDist, colorVal))])
		successors.remove((minDir, minDist, colorVal))

	return successorList

def squareCheck(grid, assignedCell):
	curX = assignedCell.x
	curY = assignedCell.y
	if curX > 0 and curY > 0:
		if grid[curY][curX].assignment == grid[curY-1][curX].assignment == grid[curY-1][curX-1].assignment == grid[curY][curX-1].assignment:
			return False
	if curX < len(grid[curY])-1 and curY > 0:
		if grid[curY][curX].assignment == grid[curY-1][curX].assignment == grid[curY-1][curX+1].assignment == grid[curY][curX+1].assignment:
			return False
	if curX > 0 and curY < len(grid[curY])-1:
		if grid[curY][curX].assignment == grid[curY+1][curX].assignment == grid[curY+1][curX-1].assignment == grid[curY][curX-1].assignment:
			return False
	if curX < len(grid[curY])-1 and curY < len(grid[curY])-1:
		if grid[curY][curX].assignment == grid[curY+1][curX].assignment == grid[curY+1][curX+1].assignment == grid[curY][curX+1].assignment:
			return False
	return True

def manhattan_distance_ordering(colorVal, colorLoc, x, y):
	endPath = colorLoc.get(colorVal+'End')
	return abs(endPath[0]-x) + abs(endPath[1]-y)

def forward_checking(grid, colorList):
	# for row in grid:
	# 	for col in row:
	return True

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
	#### Change the number below to reflect the depth limit that you want.
	if iterations >= 100000:
		return -1
	for z in range(0, len(grid)):
		print ' '.join(grid[z][y].assignment for y in range(0, len(grid[z])))
	raw_input("Press Enter")
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
				cell.assignment = '_'
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
			# print "LEFT", (grid[space.y][space.x-1]).assignment
			if(grid[space.y][space.x-1].assignment == newAssign):
				if(numNeighbors(grid, grid[space.y][space.x-1], newAssign, colorLoc) == False):
					return False
	
		if(space.x < len(grid)-1):
			# print "RIGHT", (grid[space.y][space.x+1]).assignment
			if(grid[space.y][space.x+1].assignment == newAssign):
				if(numNeighbors(grid, grid[space.y][space.x+1], newAssign, colorLoc) == False):
					return False

		if(space.y > 0):
			# print "UP", (grid[space.y-1][space.x]).assignment
			if(grid[space.y-1][space.x].assignment == newAssign):
				if(numNeighbors(grid, grid[space.y-1][space.x], newAssign, colorLoc) == False):
					return False

		if(space.y < len(grid)-1):
			# print "DOWN", (grid[space.y+1][space.x]).assignment
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

	# print "numNeighbors", numNeighbors
	if ((colorLoc.get(newAssign + 'Start') == (space.x, space.y)) or (colorLoc.get(newAssign + 'Start') == (space.x, space.y))): 
		return (numNeighbors <= 1)

	return (numNeighbors <= 2)

##################################################################
def findPath(grid, start, goal):
	path = []
	visited = []
	valid = 0

	if (start.x < 0) or (start.y < 0) or (start.x >= len(grid)) or (start.y >= len(grid[0])) or start.assignment == '_':
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
					var = Variable(c, y, '_', None, None)
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
	colorPaths = {}
	for i in colorList:
		colorStart = colorLoc.get(i+'Start')
		colorPaths[i+'x'] = []
		colorPaths[i+'y'] = []
		colorPaths[i+'x'].append(colorStart[0])
		colorPaths[i+'y'].append(colorStart[1])
	smart_csp_search(grid, colorList, colorLoc, colorPaths)

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
	main("input55.txt")

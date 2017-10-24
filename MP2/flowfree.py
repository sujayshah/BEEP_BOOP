from variable import Variable

def readFile(filename):
	textFile = open(filename, "r")
	flowFreeMap = []

	for line in textFile:
		flowFreeMap.append(line.strip().split('\r\n '))

	textFile.close()

	return flowFreeMap

def smart_csp_search(grid, colorList, colorLoc, cellList):
	for z in range(0, len(grid)):
		print grid[z][0].assignment, grid[z][1].assignment, grid[z][2].assignment, grid[z][3].assignment, grid[z][4].assignment#, grid[z][5].assignment, grid[z][6].assignment, grid[z][7].assignment
	for z in range(0, len(grid)):
		print grid[z][0].state, grid[z][1].state, grid[z][2].state, grid[z][3].state, grid[z][4].state#, grid[z][5].assignment, grid[z][6].assignment, grid[z][7].assignment 

def dumb_csp_search(grid, colorList, colorLoc, cellList):

	for z in range(0, len(grid)):
		print grid[z][0].assignment, grid[z][1].assignment, grid[z][2].assignment, grid[z][3].assignment, grid[z][4].assignment#, grid[z][5].assignment, grid[z][6].assignment, grid[z][7].assignment
	for z in range(0, len(grid)):
		print grid[z][0].state, grid[z][1].state, grid[z][2].state, grid[z][3].state, grid[z][4].state#, grid[z][5].assignment, grid[z][6].assignment, grid[z][7].assignment 
	# raw_input("Press Enter")
	allPathsFound = True
	for i in colorList:
		startPath = colorLoc.get(i+'Start')
		endPath = colorLoc.get(i+'End')
		# print i+'Start', startPath
		if (findPath(grid, grid[startPath[1]][startPath[0]], grid[endPath[1]][endPath[0]]) == None):
			allPathsFound = False

	for i in range(0, len(grid)):
		for var in grid[i]:
			if(var.state == 0):
				allPathsFound = False

	# print allPathsFound
	if allPathsFound == True:
		return grid

	for cell in cellList:
		print "SPACE COORDS ", cell.x, cell.y
		for newAssign in cell.domain:
			if(cell.state == 0):
				print "NEWASSIGN ", newAssign
				print " "
				cell.assignment = newAssign
				cell.state = 2
				if neighbors(grid, cell, newAssign, colorLoc):
					# print space.x, space.y, space.assignment
					result = dumb_csp_search(grid, colorList, colorLoc, cellList)
					print "SPACE RETURN", cell.x, cell.y
					print " "
					if(result != None):
						return result
				cell.assignment = '_'
				cell.state = 0
				print "Newassign on fail", newAssign, colorList[-1]
				if newAssign == colorList[-1]:
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
		print "STARTCHECK", numNeighbors
		return (numNeighbors <= 1)

	return (numNeighbors <= 2)


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
				
	# for space in grid:
	# 	print space.x, space.y, space.assignment, space.domain
	print colorList
	print colorLoc
	

# Reserved for testing path// DO NOT UNCOMMENT -- Call in other functions if needed
#-------------------------------------------------------------------------
	# yellowStart = colorLoc.get('YStart')
	# yellowEnd = colorLoc.get('YEnd')
	# print "START", grid[yellowStart[1]][yellowStart[0]].x, grid[yellowStart[1]][yellowStart[0]].y, grid[yellowStart[1]][yellowStart[0]].assignment
	# print "END", grid[yellowEnd[1]][yellowEnd[0]].x, grid[yellowEnd[1]][yellowEnd[0]].y, grid[yellowEnd[1]][yellowEnd[0]].assignment
	# print "LEN", len(grid)
	# colorPath = findPath(grid, grid[yellowStart[1]][yellowStart[0]], grid[yellowEnd[1]][yellowEnd[0]])
	# for i in colorPath:
	# 	print i.x, i.y
#--------------------------------------------------------------------------
	
	grid = dumb_csp_search(grid, colorList, colorLoc, cellList)
	# smart_csp_search(grid)

if __name__ == "__main__" : 
	main("input55.txt")

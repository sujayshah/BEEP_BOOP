from variable import Variable

def readFile(filename):
	textFile = open(filename, "r")
	flowFreeMap = []

	for line in textFile:
		flowFreeMap.append(line.strip().split('\r\n '))

	textFile.close()

	return flowFreeMap


def dumb_csp_search(grid):

	for l in range(0, len(grid)):
		for space in grid[l]:
			print space.x, space.y, space.assignment, space.domain, space.state

	print 
	# assignmentList = ["orange", "green", ]

	# for space in grid:
		# print space.x, space.y, space.assignment, space.domain, space.state
		# if space.state == 0:
		# 	for newAssign in space.domain:
		# 		space.assignment = newAssign
		# 		space.state = 2
				# if(space.x > 0 and (getVar(grid, x-1, y)).assignment == 0)
		
	# print space.x, space.y, space.assignment, space.domain, space.state


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
		print start.x, start.y
		x = start.x
		y = start.y

		if start.x > 0 and (x-1, y) not in visited:
			if (grid[x-1][y]).assignment == start.assignment:
				path.append(grid[x-1][y])
				visited.append((x-1, y))
				valid += 1 

		if start.x < len(grid) and (x+1, y) not in visited:
			if (grid[x+1][y]).assignment == start.assignment:
				path.append(grid[x+1][y])
				visited.append((x+1, y))
				valid += 1

		if start.y > 0 and (x, y-1) not in visited:
			if (grid[x][y-1]).assignment == start.assignment:
				path.append(grid[x][y-1])
				visited.append((x, y-1))
				valid += 1

		if start.y < len(grid) and (x, y+1) not in visited:
			if (grid[x][y+1]).assignment == start.assignment:
				path.append(grid[x][y+1])
				visited.append((x, y+1))
				valid += 1

		if(valid != 1):
			return None

		valid = 0
		print "NEWSTART", path[-1].x, path[-1].y
		start = path[-1]
		print "GOAL", goal.x, goal.y
	return path


def main(filename):
	flowFree = readFile(filename)
	colorList = []
	colorLoc = {}
	grid = []
	x = 0
	for line in flowFree:
		for s in line: 
			grid2 = []
			print s
			for c in range(0,len(s)):
				if s[c] not in colorList and s[c] != '_':
					colorList.append(s[c])
					colorLoc[s[c]+'Start'] = (x, c)
				
				if s[c] == '_':
					var = Variable(x, c, ' ', None, None)
					var.domain = colorList
					var.state = 0

				else:
					var = Variable(x, c, s[c], None, None)
					var.domain.append(s[c])
					var.state = 1
					colorLoc[s[c]+'End'] = (x, c)

				grid2.append(var)
			
			grid.append(grid2)
			x+=1
				
	# for space in grid:
	# 	print space.x, space.y, space.assignment, space.domain

	yellowStart = colorLoc.get('YStart')
	yellowEnd = colorLoc.get('YEnd')
	# print yellowStart, yellowEnd
	print "START", grid[yellowStart[0]][yellowStart[1]].x, grid[yellowStart[0]][yellowStart[1]].y, grid[yellowStart[0]][yellowStart[1]].assignment
	print "END", grid[yellowEnd[0]][yellowEnd[1]].x, grid[yellowEnd[0]][yellowEnd[1]].y, grid[yellowEnd[0]][yellowEnd[1]].assignment
	print "LEN", len(grid)
	me = findPath(grid, grid[yellowStart[0]][yellowStart[1]], grid[yellowEnd[0]][yellowEnd[1]])
	# for i in me:
	# 	print i.x, i.y
	# dumb_csp_search(grid)
	# smart_csp_search(grid)

if __name__ == "__main__" : 
	main("inputPathFinder.txt")

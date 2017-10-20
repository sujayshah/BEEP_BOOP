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

	print colorLoc
	yellowStart = colorLoc.get('RStart')
	yellowEnd = colorLoc.get('REnd')

	print "START", grid[yellowStart[1]][yellowStart[0]].x, grid[yellowStart[1]][yellowStart[0]].y, grid[yellowStart[1]][yellowStart[0]].assignment
	print "END", grid[yellowEnd[1]][yellowEnd[0]].x, grid[yellowEnd[1]][yellowEnd[0]].y, grid[yellowEnd[1]][yellowEnd[0]].assignment
	print "LEN", len(grid)
	colorPath = findPath(grid, grid[yellowStart[1]][yellowStart[0]], grid[yellowEnd[1]][yellowEnd[0]])
	for i in colorPath:
		print i.x, i.y
	# dumb_csp_search(grid)
	# smart_csp_search(grid)

if __name__ == "__main__" : 
	main("inputPathFinder.txt")

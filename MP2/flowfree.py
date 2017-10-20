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


def findPath(grid, x, y):
	path = []
	valid = 0
	if (x < 0) or (y < 0) or (x >= len(grid)) or (y >= len(grid[0])) or (grid[x][y]).assignment == ' ':
		return None

	path.append(grid[x][y])
	if x > 0:
		if (grid[x-1][y]).assignment == grid[x][y]:
			path.append(grid[x-1][y])
			valid += 1 

	if x < len(grid)-1:
		if (grid[x+1][y]).assignment == grid[x][y]:
			path.append(grid[x+1][y])
			valid += 1

	if y > 0:
		if (grid[x][y-1]).assignment == grid[x][y]:
			path.append(grid[x][y-1])
			valid += 1

	if y < len(grid)-1:
		if (grid[x][y+1]).assignment == grid[x][y]:
			path.append(grid[x][y+1])
			valid += 1

	return valid if (valid == 1) else None

def main(filename):
	flowFree = readFile(filename)
	colorList = []
	grid = []
	x = 0
	for line in flowFree:
		for s in line: 
			grid2 = []
			print s
			for c in range(0,len(s)):
				if s[c] not in colorList and s[c] != '_':
					colorList.append(s[c])
				
				if s[c] == '_':
					var = Variable(x, c, ' ', None, None)
					var.domain = colorList
					var.state = 0

				else:
					var = Variable(x, c, s[c], None, None)
					var.domain.append(s[c])
					var.state = 1

				grid2.append(var)
			
			grid.append(grid2)
			x+=1
				
	# for space in grid:
	# 	print space.x, space.y, space.assignment, space.domain

	dumb_csp_search(grid)
	# smart_csp_search(grid)

if __name__ == "__main__" : 
	main("input88.txt")

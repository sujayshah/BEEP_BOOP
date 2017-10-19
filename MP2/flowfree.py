from variable import Variable

def readFile(filename):
	textFile = open(filename, "r")
	flowFreeMap = []

	for line in textFile:
		flowFreeMap.append(line.strip().split('\r\n '))

	textFile.close()

	return flowFreeMap


def dumb_csp_search(grid):

	# assignmentList = ["orange", "green", ]

	for space in grid:
		# print space.x, space.y, space.assignment, space.domain, space.state
		if space.state == 0:
			for newAssign in space.domain:
				space.assignment = newAssign
				space.state = 2
				if(space.x > 0 and getVar(grid, x-1, y)) and s
		
		print space.x, space.y, space.assignment, space.domain, space.state


def getVar(grid, x, y):
	for space in grid:
		if (space.x == x and space.y == y):
			return space

	return None

def main(filename):
	flowFree = readFile(filename)
	colorList = []
	grid = []
	x = 0
	for line in flowFree:
		for s in line: 
			print s
			for c in range(0,len(s)):
				if s[c] not in colorList and s[c] != '_':
					colorList.append(s[c])
				
				if s[c] == '_':
					var = Variable(x, c, s[c], None, None)
					var.domain = colorList
					var.state = 0

				else:
					var = Variable(x, c, s[c], None, None)
					var.domain.append(s[c])
					var.state = 1

				
				grid.append(var)
				
			x+=1
				
	# for space in grid:
	# 	print space.x, space.y, space.assignment, space.domain

	dumb_csp_search(grid)
	# smart_csp_search(grid)

if __name__ == "__main__" : 
	main("input88.txt")

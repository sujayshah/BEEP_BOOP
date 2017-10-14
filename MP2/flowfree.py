from variable import Variable

def readFile(filename):
	textFile = open(filename, "r")
	flowFreeMap = []

	for line in textFile:
		flowFreeMap.append(line.strip().split('\r\n '))

	textFile.close()

	return flowFreeMap




def main(filename):
	flowFree = readFile(filename)
	grid = []
	x = 0
	for line in flowFree:
		for s in line: 
			print s
			for c in range(0,len(s)):
				if s[c] == 'O':
					var = Variable(x, c, s[c], None)
					var.domain.append("orange")
				elif s[c] == 'G':
					var = Variable(x, c, s[c], None)
					var.domain.append("green")
				elif s[c] == 'R':
					var = Variable(x, c, s[c], None)
					var.domain.append("red")
				elif s[c] == 'B':
					var = Variable(x, c, s[c], None)
					var.domain.append("blue")
				elif s[c] == 'Y':
					var = Variable(x, c, s[c], None)
					var.domain.append("yellow")
				else:
					var = Variable(x, c, s[c], None)
					var.domain.append("orange")
					var.domain.append("green")
					var.domain.append("red")
					var.domain.append("blue")
					var.domain.append("yellow")
				
				grid.append(var)
				
			x+=1
				
	for space in grid:
		print space.x, space.y, space.assignment, space.domain

if __name__ == "__main__" : 
	main("input77.txt")

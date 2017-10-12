def read_grid(gridname):
	textFile = open(gridname, "r")
	grid = []

	for line in textFile:
		grid.append(line.strip().split('\r\n '))

	textFile.close()

	return grid


def main(gridname):
	read_grid(gridname)

if __name__ == '__main__':
	main("insertgridnamehere.txt")
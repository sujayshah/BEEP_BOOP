# global definition# 
x_start = 0
y_start = 0

# This function reads in the maze from the text file and generates the 
# 2D array to traverse through.  									   
def read_map(mapname):
	textFile = open(mapname, "r")
	maze = []

	for line in textFile:
		maze.append(line.strip().split('\r\n '))

	textFile.close()

	return maze

# This function writes back to a text file our 2D array that we read in. 
# Namely used to verify we read in text file correctly.
def write_test_map(mapname):
	maze = read_map(mapname)

	with open(mapname, 'w') as outFile:
		for item in my_list:
			outFile.write("%s\n"  %item)

# This function finds the (x,y) start position of the maze, marked as 
# 'P' in the text file.
def find_start(mapname):
	maze = read_map(mapname)
	global x_start 
	global y_start

	for ypos, line in enumerate(maze):
		for string in line:
			for xpos, char in enumerate(string):
				if char == 'P':
					x_start = xpos
					y_start = ypos 
					#print xpos, ypos			
# Main function
def main():
	lines2= read_map("tinySearch.txt")
	#write_test_map("tinySearch_test.txt")

	for line in lines2:
		for s in line: 
			print s

	find_start("tinySearch.txt")

	#print "Main print: "
	#print x_start 
	#print y_start

if __name__ == "__main__":
	main()
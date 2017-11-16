
# This function reads in the text file
def read_file(filename):
	textFile = open(filename, "r")
	text = []

	for line in textFile:
		text.append(line.strip().split('\r\n '))

	textFile.close()

	return text

# This
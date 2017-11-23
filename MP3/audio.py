from itertools import islice #islice is used to get the next n items of an iterator

# This function reads in a training file and splices it into lists
# Spectrograms are split into lines of 25 x 10 characters, seperated by 3 blank lines
# 0 - 24 first spectrogram
# 28 - 52 second spectrogram
def read_file(filename):
	f = open(filename)
	clear_file('temp.txt')
	n = 0 
	lines = f.readlines() 
	while not f.readlines():
		for i in range(n, n + 24): #this is the loop that we can do our work in
			write_file('temp.txt', lines[i])
			for char in lines[i]:
				print char
		
		#n = n + 24 + 4
		write_file('temp.txt', lines[n + 25])
		write_file('temp.txt', lines[n + 26])
		write_file('temp.txt', lines[n + 27])

		n = n + 24 + 4

# This function takes in a file and a line to write and appends the line to the file
def write_file(filename, line):
	with open(filename, 'a') as outFile:
			outFile.write("%s" %line)
	
def clear_file(filename):
	open(filename, 'w').close()

# every spectogram is described by 250 binary variables
# W(i, j) = 1 if spectrogram(i, j) = ' ' (high energy)
# W(i, j) = 0 if spectrogram(i, j) = '%' (low energy)
# estimate the likelihoods P(W(i,j)= 1 | class) as proportion of the training data that is high energy

# the goal of the training stage is to estimate the likelihoods P(W(i, j) | class) for 
# every pixel location 
# P(W(i, j) = f| class)) = (# times pixel(i, j) has value f in training examples for this class) /
# (Total # of training examples from this class)
def main(samplename): 
	read_file(samplename)

if __name__ == '__main__':
	main('no_train.txt')
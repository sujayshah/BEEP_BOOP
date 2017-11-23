from itertools import islice #islice is used to get the next n items of an iterator

indiv_high_list = []
indiv_low_list = []


# This function reads in a yes_train file and splices it into lists
# Spectrograms are split into lines of 25 x 10 characters, seperated by 3 blank lines
# 0 - 24 first spectrogram
# 28 - 52 second spectrogram
def read_file(filename):
	f = open(filename)
	clear_file('temp.txt')
	n = 0 
	num_samples = 1 
	lines = f.readlines() 
	#while n < 3665:
	charlist = [0] * 250 ## need to update to global frequency table
	while n < 25:
		for idx, i in enumerate(range(n, n + 25)): #this is the loop that we can do our work in
			write_file('temp.txt', lines[i])

			for col, char in enumerate(lines[i]):
				if col >= 10: #break on col index 10 since this is just the newline character leftover from readlines()
					break

				print "Looking at : " + str(idx * 10 + col), 

				if char == '%':
					print char, 
					charlist[idx * 10 + col] = 0
					print "Set!"
				else: 
					print char
					charlist[idx * 10 + col] = 1
					print "Set!"
				
			#print i
		
		#n = n + 24 + 4
		write_file('temp.txt', lines[n + 25])
		write_file('temp.txt', lines[n + 26])
		write_file('temp.txt', lines[n + 27])

		n = n + 24 + 4
		num_samples = num_samples + 1
		print charlist

	#print num_samples


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
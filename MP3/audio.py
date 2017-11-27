from itertools import islice #islice is used to get the next n items of an iterator

indiv_high_list = []
indiv_low_list = []


# This function reads in a yes_train file and splices it into lists
# Spectrograms are split into lines of 25 x 10 characters, seperated by 3 blank lines
# 0 - 24 first spectrogram
# 28 - 52 second spectrogram
# 131 samples for no_train.txt, 131 samples for yes_train.txt
# total 262 samples 
def read_file(filename):
	f = open(filename)
	clear_file('temp.txt')
	n = 0 
	num_samples = 1 
	lines = f.readlines() 
	charlist = [(0,0)] * 250 #frequency table. (low, high) = ('%', ' ')
	
	while n < 3665:
		for idx, i in enumerate(range(n, n + 25)): #this is the loop that we can do our work in
			write_file('temp.txt', lines[i])

			for col, char in enumerate(lines[i]):
				if col >= 10: #break on col index 10 since this is just the newline character leftover from readlines()
					break

				if char == '%': #low energy
					#print char
					lowprev = charlist[idx * 10 + col][0]
					highprev = charlist[idx * 10 + col][1]
					charlist[idx * 10 + col] = (lowprev + 1, highprev)
				else: 
					#print char
					lowprev = charlist[idx * 10 + col][0]
					highprev = charlist[idx * 10 + col][1]
					charlist[idx * 10 + col] = (lowprev, highprev + 1)
			
		#n = n + 24 + 4
		write_file('temp.txt', lines[n + 25]) #blank lines to separate
		write_file('temp.txt', lines[n + 26])
		write_file('temp.txt', lines[n + 27])

		n = n + 24 + 4 #start reading next sample
		num_samples = num_samples + 1

	#print charlist
	return charlist


# This function takes in a file and a line to write and appends the line to the file
def write_file(filename, line):
	with open(filename, 'a') as outFile:
			outFile.write("%s" %line)
	
def clear_file(filename):
	open(filename, 'w').close()

def train(k): #k value is the value for Laplacian smoothing. 
	no_train = read_file('no_train.txt')
	yes_train = read_file('yes_train.txt')

	likelihood_no = [0] * 250 # times location (i, j) has value '' in training examples from class NO / total # of training examples from this class
	likelihood_yes = [0] * 250  # times location (i, j) has value '' in training examples from class YES/ total # of training examples from this class

	for idx, sample in enumerate(no_train): 
		likelihood_no[idx] = (no_list[idx][1] + k) / (131.0 + (2 * k))

	for idx, sample in enumerate(yes_train): 
	 	likelihood_yes[idx] = (yes_list[idx][1] + k) / (131.0 + (2 * k))


# This function performs a MAP classification of "yes" or "no" according to the learned model
def test():
	no_test = read_file('no_test.txt')
	yes_test = read_file('yes_test.txt')

	for idx, sample in enumerate

# every spectogram is described by 250 binary variables
# W(i, j) = 1 if spectrogram(i, j) = ' ' (high energy)
# W(i, j) = 0 if spectrogram(i, j) = '%' (low energy)
# estimate the likelihoods P(W(i,j)= 1 | class) as proportion of the training data that is high energy

# the goal of the training stage is to estimate the likelihoods P(W(i, j) | class) for 
# every pixel location 
# P(W(i, j) = f| class)) = (# times pixel(i, j) has value f in training examples for this class) /
# (Total # of training examples from this class)
def main(samplename): 
	train(0) #default WITHOUT LAPLACIAN SMOOTHING

if __name__ == '__main__':
	main('yes_train.txt')
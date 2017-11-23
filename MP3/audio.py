from itertools import islice #islice is used to get the next n items of an iterator

def read_file(filename):
	# 0 - 24 first spectogram
	# 28 - 52 
	n = 25
	with open(filename, 'r') as infile: 
		while True: 
			next_n_lines = list(islice(infile, n))
			
			if not next_n_lines:
				break

			for idx, line in enumerate(next_n_lines): 
				write_file('temp.txt', line)
				print line,

def write_file(filename, line):
	with open(filename, 'a') as outFile:
			outFile.write("%s" %line)
	

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
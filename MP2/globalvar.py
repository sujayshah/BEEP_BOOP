

def recurse(val):
	global iterations
	iterations = 0
	iterations = val
	if iterations == 5:
		recurse(2)

def main():
	recurse(5)
	print iterations


if __name__ == "__main__" : 
	main()

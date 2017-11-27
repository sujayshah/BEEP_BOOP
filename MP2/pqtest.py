from Queue import PriorityQueue

def main():

	test = PriorityQueue()
	test.put((2, (1, 0)))
	test.put((2, (0, 1)))
	test.put((1, (2, 0)))
	test.put((1, (1, 4)))
	test.put((3, (2, 1)))
	test.put((3, (4, 1)))
	test.put((3, (3, 2)))
	test.put((3, (4, 2)))
	test.put((3, (4, 4)))
	test.put((3, (3, 3)))

	while not test.empty():
	    next_item = test.get(test)
	    print(next_item)

	print test.empty()
	
if __name__ == "__main__" : 
	main()
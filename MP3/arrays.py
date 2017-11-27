
def main():
	array = [['+','+',' ','+'], [' ','+','+','+'], ['+','+','+',' ']]
	hello = [0, 0, 1]

	myArray = []
	for i in range(0,2):
		myArray.append([])
		for j in range(0,4):
			myArray[i].append([])
			for k in range(0,2):
				myArray[i][j].append(0)
	print myArray[0]

	for image in range(0,len(hello)):
		cur = hello[image]
		for i in range(0,4):
			if array[image][i] == '+':
				myArray[cur][i][0] += 1

	print myArray

if __name__ == '__main__':
	main()

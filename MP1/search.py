def read_map(mapname):
	with open(mapname) as textFile:
		lines = [line.strip().split('\r\n ') for line in textFile]

	return lines

def write_test_map(mapname):
	my_list = read_map("tinySearch.txt")

	with open(mapname, 'w') as outFile:
		for item in my_list:
			outFile.write("%s\n"  %item)

def main():
	lines2= read_map("tinySearch.txt")
	print lines2

	write_test_map("tinySearch_test.txt")

if __name__ == "__main__":
	main()
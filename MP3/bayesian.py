from PIL import Image

def readImages(filename):
	textFile = open(filename, "r")
	lineText = []
	counter = 0
	for line in textFile:
		lineText.append(line[0:28])
		counter += 1
	textFile.close()
	return lineText

def readLabels(filename):
	textFile = open(filename, "r")
	lineText = []
	counter = 0
	for line in textFile:
		lineText.append(int(line[0]))
	textFile.close()
	return lineText

def writeOutput(data):
	file = open("output.txt","w")
	for i in data:
		file.write(i)
		file.write('\n')
	file.close()

def drawImage(pixelData):
	data = ""
	for i in range( 0,28*28 ):
	    data += chr(128) + chr(128) + chr(255)
	im = Image.frombytes("RGB", (28,28), data)
	im.save("test.png", "PNG")

def priorFrequencies(trainingLabels):
	classFrequency = {}
	total = 0.0
	for label in trainingLabels:
		if label not in classFrequency:
			classFrequency[label] = 0.0
		classFrequency[label] += 1.0
		total += 1.0

	# print classFrequency
	# print total
	for i in range(0,10):
		if i not in classFrequency:
			classFrequency[i] = 0.0
		classFrequency[i] /= total
	# print classFrequency

	# percentTotal = 0.0
	# for i in classFrequency:
	# 	percentTotal += classFrequency[i]
	# print percentTotal

	return classFrequency

def storeTrainingData(trainingImages, trainingLabels, trainingClassFrequencies):
	curNumber = None
	pixelData = []
	pixelClassLikelihood = []
	for imageIndex in range(0, len(trainingImages)/28):
		curNumber = trainingLabels[imageIndex]
		pixelData.append([])
		for i in range(0,28):
			pixelData[imageIndex].append(trainingImages[imageIndex*28+i])

	# for i in range(0, len(pixelData)):
	# 	# for j in range(0,28):
	# 	print pixelData[i]
	
	for numClass in range(0,10):
		pixelClassLikelihood.append([])
		for i in range(0,28): 
			pixelClassLikelihood[numClass].append([])
			for j in range(0,28):
				pixelClassLikelihood[numClass][i].append([])
				for frac in range(0,2):
					pixelClassLikelihood[numClass][i][j].append(0)
		
	for imageIndex in range(0, len(trainingImages)/28):
		curNumber = trainingLabels[imageIndex]
		for i in range(0,28):
			# print pixelData[imageIndex][i]
			for j in range(0,28):
				if pixelData[imageIndex][i][j] == '+' or pixelData[imageIndex][i][j] == '#':
					pixelClassLikelihood[curNumber][i][j][0] += 1
				pixelClassLikelihood[curNumber][i][j][1] += 1
	
	return pixelClassLikelihood

def laplacianSmoothing(trainingData, k, V):
	for classValue in range(0,10):
		for i in range(0,28):
			for j in range(0,28):
				trainingData[classValue][i][j][0] += k
				trainingData[classValue][i][j][1] += (k*V)

	print trainingData[1]

# def evaluation():

def main():
	print "Reading Training Data"
	trainingImages = readImages("trainingImages")
	trainingLabels = readLabels("trainingLabels")
	print "Training Data Reading Complete"
	# writeOutput(trainingImages)

	print "Calculating Prior Frequencies in Training Data"
	trainingClassFrequencies = priorFrequencies(trainingLabels)
	print "Prior Frequencies Calculated"
	print "Evaluating Training Data..."
	trainingData = storeTrainingData(trainingImages, trainingLabels, trainingClassFrequencies)
	print "Training Data Evaluation Complete"
	print "Laplacian Smoothing of Training Data Initiated...."
	laplacianSmoothing(trainingData, 1, 10)
	print "Laplacian Smoothing Complete"
	print "Evaluating Test Images"
	# evaluation()
	print "Test Images Evaluated"

	# print trainingData
	# testImages = readImages("testImages")
	# testLabels = readLabels("testLabels")
	
if __name__ == '__main__':
	main()

from PIL import Image
import math

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

def drawImage(pixelData, filename):
	data = ""
	for i in range(0,112*112):
		a = math.log10(float(pixelData[0][0][0])/float(pixelData[0][0][1]))
		# data += chr(255-(63*a)) + chr(0) + chr(0-(63*a))
		data += chr(255) + chr(128) + chr(128)
	im = Image.frombytes("RGB", (112,112), data)
	im.save(filename, "PNG")

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

def testing(testImages, trainingData, trainingClassFrequencies):
	
	classResults = []
	mapResults = []
	intVal = []
	for i in range(0,28):
		intVal.append([])
		for j in range(0, 28):
			intVal[i].append(0)

	for image in range(0, len(testImages)/28):
		classResults.append([])
		for i in range(0,28):
			for j in range(0,28):
				curVal = testImages[28*image+i][j]
				if curVal == '+' or curVal == '#':
					intVal[i][j] = 1
				else:
					intVal[i][j] = 0

		for classVal in range(0,10):
			classResults[image].append(math.log10(trainingClassFrequencies[classVal]))
			for i in range(0, len(intVal)):
				for j in range(0, len(intVal[i])):
					prob = float(trainingData[classVal][i][j][0])/float(trainingData[classVal][i][j][1])
					if intVal[i][j] == 0:
						prob = 1.0-prob
					prob = math.log10(prob)
					classResults[image][classVal] += prob

	for imageResults in classResults:
		max_value = max(imageResults)
		max_index = imageResults.index(max_value)
		mapResults.append(max_index)
	
	return mapResults

def evaluation(testingResults, testLabels):
	success = 0.0
	attempts = 0.0
	for i in range(0, len(testLabels)):
		if testingResults[i] == testLabels[i]:
			success += 1.0
		attempts += 1.0
	return (100*success)/attempts

def digitEvaluation(testingResults, testLabels):
	digitCorrect = []
	for i in range(0,10):
		success = 0.0
		attempts = 0.0
		for digitIterator in range(0, len(testLabels)):
			if testLabels[digitIterator] == i:
				attempts += 1.0
				if testingResults[digitIterator] == i:
					success += 1.0
		digitCorrect.append(100*success/attempts)

	return digitCorrect

def computeConfusionMatrix(testingResults, testLabels):
	confusionMatrix = []
	digitFreq = []
	for i in range(0,10):
		confusionMatrix.append([])
		digitFreq.append(0.0)
		for j in range(0,10):
			confusionMatrix[i].append(0.0)

	for value in range(0, len(testLabels)):
		confusionMatrix[testLabels[value]][testingResults[value]] += 1.0
		digitFreq[testLabels[value]] += 1.0

	for i in range(0,10):
		for j in range(0,10):
			confusionMatrix[i][j] *= 100.0
			confusionMatrix[i][j] /= digitFreq[i]

	return confusionMatrix

def posteriorProb(testImages, testLabels, trainingData, trainingClassFrequencies, highIdxs, lowIdxs):
	myIdx = [[-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1]]
	for value in range(0,10):
		highIdxs.append(-100)
		lowIdxs.append(100)
		for image in range(0, len(testLabels)/28):
			if testLabels[image] == value:
				prob = math.log10(trainingClassFrequencies[value])
				for i in range(0,28):
					for j in range(0,28):
						if testImages[28*image+i][j] == '+' or testImages[28*image+i][j] == '#':
							prob += math.log10(float(trainingData[value][i][j][0])/float(trainingData[value][i][j][1])) 
						else:
							prob += math.log10(1.0-(float(trainingData[value][i][j][0])/float(trainingData[value][i][j][1])))
				if prob > highIdxs[value]:
					highIdxs[value] = prob
					myIdx[value][0] = image
				if prob < lowIdxs[value]:
					lowIdxs[value] = prob
					myIdx[value][1] = image

	return myIdx

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
	print "Laplacian Smoothing of Training Data Initiated..."
	k = 0.1
	laplacianSmoothing(trainingData, k, 10)
	print "Laplacian Smoothing Complete"
	print "Reading Training Data..."
	testImages = readImages("testImages")
	testLabels = readLabels("testLabels")
	print "Training Data Reading Complete"
	print "Evaluating Test Images..."
	testingResults = testing(testImages, trainingData, trainingClassFrequencies)
	print "Test Images Evaluated"
	print "Evaluating Results..."
	percentageCorrect = evaluation(testingResults, testLabels)
	digitCorrect = digitEvaluation(testingResults, testLabels)
	print "Results Evaluated"
	print "With a smoothing constant of", k, ", The Bayes Classifier has correctly identified the digit", percentageCorrect, "% of the time."
	for i in range(0,10):
		print "For digit", i, ", The Bayes Classifier correctly identified it", digitCorrect[i], "% of the time."
	print "Computing Confusion Matrix..."
	confusionMatrix = computeConfusionMatrix(testingResults, testLabels)
	print "Confusion Matrix Calculated"
	print "\n"
	for i in range(0,10):
		print confusionMatrix[i]
	print "\n"
	print "Calculating Images in Each Class With Highest and Lowest Posterior Prob"
	highIdxs = []
	lowIdxs = []
	myIdx = posteriorProb(testImages, testLabels, trainingData, trainingClassFrequencies, highIdxs, lowIdxs)
	print myIdx
	print "Finished Calculating Images With Highest and Lowest Posterior Prob"

	print "Drawing Images..."
	drawImage(trainingData[4], "likelihood1.png")
	# drawImage(trainingData[9], "likelihood2.png")
	# drawImage(1, "oddsRatio.png")
	print "Images Drawn to likelihood1.png, likelihood2.png, and oddsRatio.png"

if __name__ == '__main__':
	main()

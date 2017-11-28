from PIL import Image
import math

#This function reads in file data and saves it in the form of strings for each line
def readImages(filename):
	textFile = open(filename, "r")
	lineText = []
	counter = 0
	for line in textFile:
		lineText.append(line[0:28])
		counter += 1
	textFile.close()
	return lineText

#This function is a modified form of reading file data since it preserves integers rather than converting them into strings
def readLabels(filename):
	textFile = open(filename, "r")
	lineText = []
	counter = 0
	for line in textFile:
		lineText.append(int(line[0]))
	textFile.close()
	return lineText

#This function is able to write a piece of data to an output text file
def writeOutput(data):
	file = open("output.txt","w")
	for i in data:
		file.write(i)
		file.write('\n')
	file.close()

#This function is called in order to create output images of likelihood maps 
def drawImage(pixelData, filename):
	data = ""
	for i in range(0,28):
		for j in range(0,28):
			a = math.log10(float(pixelData[i][j][0])/float(pixelData[i][j][1]))
			data += chr(int(255+(63*a))) + chr(int(255-127*abs(2+a))) + chr(int(0-(63*a)))
	im = Image.frombytes("RGB", (28,28), data)
	im.save(filename, "PNG")

#This function is called in order 
def drawOddsRatio(pixelData1, pixelData2, filename):
	data = ""
	for i in range(0,28):
		for j in range(0,28):
			a = math.log10(float(pixelData1[i][j][0])/float(pixelData1[i][j][1]))-math.log10(float(pixelData2[i][j][0])/float(pixelData2[i][j][1]))
			a = min(4, a+3)
			data += chr(int(63*a)) + chr(int(255-127*abs(2-a))) + chr(int(255-(63*a)))
	im = Image.frombytes("RGB", (28,28), data)
	im.save(filename, "PNG")

#The purpose of this function is to compute the frequency of each digit class in the training label data
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

#The purpose of this function is to create the training stage of the Bayesian classifier.
def storeTrainingData(trainingImages, trainingLabels, trainingClassFrequencies):
	curNumber = None
	pixelData = []
	pixelClassLikelihood = []
	# This iterative loop places data inside lists of training data that are easy to reference
	for imageIndex in range(0, len(trainingImages)/28):
		curNumber = trainingLabels[imageIndex]
		pixelData.append([])
		for i in range(0,28):
			pixelData[imageIndex].append(trainingImages[imageIndex*28+i])
	# This iterative loop creates the output list structure that will be used to pass organized data back
	for numClass in range(0,10):
		pixelClassLikelihood.append([])
		for i in range(0,28): 
			pixelClassLikelihood[numClass].append([])
			for j in range(0,28):
				pixelClassLikelihood[numClass][i].append([])
				for frac in range(0,2):
					pixelClassLikelihood[numClass][i][j].append(0)
		#This is where the image data is processed, each image is stored and computed together with other data in its class
	for imageIndex in range(0, len(trainingImages)/28):
		curNumber = trainingLabels[imageIndex]
		for i in range(0,28):
			for j in range(0,28):
				# Number data consists of '+' and '#' without any discrimination towards either
				if pixelData[imageIndex][i][j] == '+' or pixelData[imageIndex][i][j] == '#':
					pixelClassLikelihood[curNumber][i][j][0] += 1
				pixelClassLikelihood[curNumber][i][j][1] += 1
	
	return pixelClassLikelihood

#This function takes an input Laplacian constant k that smoothes data by giving a slight bump in frequency to pixel values that 
#have not been used in drawing the numbers but may in the future
def laplacianSmoothing(trainingData, k, V):
	for classValue in range(0,10):
		for i in range(0,28):
			for j in range(0,28):
				trainingData[classValue][i][j][0] += k
				trainingData[classValue][i][j][1] += (k*V)

#This function applies the trained Bayesian classifier by giving a new set of data to blindly identify using only data collected in the training stage
def testing(testImages, trainingData, trainingClassFrequencies):	
	classResults = []
	mapResults = []
	intVal = []
	#this list is used to compute whether number data is written at specific pixels on the test image or not
	for i in range(0,28):
		intVal.append([])
		for j in range(0, 28):
			intVal[i].append(0)
	#this iterative loop checks every pixel in the test image and collects the data
	for image in range(0, len(testImages)/28):
		classResults.append([])
		for i in range(0,28):
			for j in range(0,28):
				curVal = testImages[28*image+i][j]
				if curVal == '+' or curVal == '#':
					intVal[i][j] = 1
				else:
					intVal[i][j] = 0
	#this iterative loop computes a separate probability value using logarithms and independent class's probability data 
	#to accumulate all probability data from the test image
		for classVal in range(0,10):
			classResults[image].append(math.log10(trainingClassFrequencies[classVal]))
			for i in range(0, len(intVal)):
				for j in range(0, len(intVal[i])):
					prob = float(trainingData[classVal][i][j][0])/float(trainingData[classVal][i][j][1])
					if intVal[i][j] == 0:
						prob = 1.0-prob
					prob = math.log10(prob)
					classResults[image][classVal] += prob
	# once the results for all classes are filled in their independent lists, a decision is made for every image based on whichever class
	#has the highest probability value
	for imageResults in classResults:
		max_value = max(imageResults)
		max_index = imageResults.index(max_value)
		mapResults.append(max_index)
	
	return mapResults

#This function evaluates the performance of the classifier by checking its results for all images against the solutions. The percentage of
#correct answers is returned back
def evaluation(testingResults, testLabels):
	success = 0.0
	attempts = 0.0
	for i in range(0, len(testLabels)):
		if testingResults[i] == testLabels[i]:
			success += 1.0
		attempts += 1.0
	return (100*success)/attempts

#This function is similar to the above evaluation function. This function calculates the individual performance by the classifier on
#all individual classes, giving a percentage correct based on the number of actual instances of the class value in the test label data
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

#This function computes the confusion matrix for the Bayesian classifier that gives the classifier's performance for all classes and provides a 
#breakdown on the distribution of guesses by the classifier given any actual class value of an image
def computeConfusionMatrix(testingResults, testLabels):
	confusionMatrix = []
	digitFreq = []
	for i in range(0,10):
		confusionMatrix.append([])
		digitFreq.append(0.0)
		for j in range(0,10):
			confusionMatrix[i].append(0.0)
	# This loop iterates and tallies the results of the classifier's guesses by analyzing every guess in the testing data
	for value in range(0, len(testLabels)):
		confusionMatrix[testLabels[value]][testingResults[value]] += 1.0
		digitFreq[testLabels[value]] += 1.0
		# returns the confusion matrix data as percentages
	for i in range(0,10):
		for j in range(0,10):
			confusionMatrix[i][j] *= 100.0
			confusionMatrix[i][j] /= digitFreq[i]

	return confusionMatrix

#This function computes two specific images for every class that have the highest and lowest posterior probability value respectively.
#This function makes it possible to identify normalized shapes that the classifier recognizes, to more deviant shapes of digits that 
#the classifier struggles to identify
def posteriorProb(testImages, testLabels, trainingData, trainingClassFrequencies, highIdxs, lowIdxs):
	#Initialize the index list for all classes
	myIdx = [[-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1]]
	for value in range(0,10):
		highIdxs.append(-100)
		lowIdxs.append(100)
		for image in range(0, len(testLabels)):
			if testLabels[image] == value:
				prob = math.log10(trainingClassFrequencies[value])
				#iterate through each image of a class and calculate the posterior probabilities by iterating through all pixels
				for i in range(0,28):
					for j in range(0,28):
						if testImages[28*image+i][j] == '+' or testImages[28*image+i][j] == '#':
							prob += math.log10(float(trainingData[value][i][j][0])/float(trainingData[value][i][j][1])) 
						else:
							prob += math.log10(1.0-(float(trainingData[value][i][j][0])/float(trainingData[value][i][j][1])))
				#replace the minima and maxima values if a more extreme value is found
				if prob > highIdxs[value]:
					highIdxs[value] = prob
					myIdx[value][0] = image
				if prob < lowIdxs[value]:
					lowIdxs[value] = prob
					myIdx[value][1] = image

	return myIdx

#This is the main function, which calls all functions needed to run the Bayesian classifier in order of initializing data, training the data,
#testing the data, evaluating the data, and finally generating data analysis for the classifier and the data itself
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
	drawImage(trainingData[5], "likelihood1.png")
	drawImage(trainingData[3], "likelihood2.png")
	drawOddsRatio(trainingData[5], trainingData[3], "oddsRatio.png")
	print "Images Drawn to likelihood1.png, likelihood2.png, and oddsRatio.png"

if __name__ == '__main__':
	main()

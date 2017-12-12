from PIL import Image
import math
import random
import numpy as np

#This function reads in file data and saves it in the form of strings for each line
def readImages(filename):
	textFile = open(filename, "r")
	lineText = []
	Image = []
	counter = 0
	for line in textFile:
		if counter == 28:
			lineText.append(Image)
			Image = []
			counter = 0
		counter += 1
		Image.append(list(line[0:28]))
	lineText.append(Image)
	textFile.close()

	return lineText

#This function reads the file data in string format and converts it to a list of integers.
#This makes subsequent computing much easier.
def convertImages(images):
	binaryImage = []
	for imageIndex in images:
		indImages = []
		for lineIndex in imageIndex:
			for pixelVal in lineIndex:
				if pixelVal == '+' or pixelVal == '#':
					indImages.append(1)
				else:
					indImages.append(0)
		binaryImage.append(indImages)
	return binaryImage

#This function is a modified form of reading file data since it preserves integers rather than converting them into strings
def readLabels(filename):
	textFile = open(filename, "r")
	lineText = []
	counter = 0
	for line in textFile:
		lineText.append(int(line[0]))
	textFile.close()
	return lineText

#The purpose of this function is to train the perceptron classifier using the parameters given and adjusting the weight of each image per epoch
def trainingStep(trainingImages, trainingLabels, alphaVal, trainingOrder, epochs, weights):
	trainingImages = np.array(trainingImages)
	trainingLabels = np.array(trainingLabels)
	for i in range(1,epochs):
		weights[i]=weights[i-1]
		numberSuccess = 0.0
		sequence = range(5000)
		if trainingOrder:
			random.shuffle(sequence)
	
		for number in sequence:
			result=[]
			for classVal in range(10):
				product = np.multiply(weights[i,classVal],trainingImages[number])
				sumVal = np.sum(product)
				result.append(sumVal)
		
			guessVal=result.index(max(result))

			if result.index(max(result))==int(trainingLabels[number]):
				numberSuccess += 1.0
			else:
				decayVal = float (alphaVal / (alphaVal + float(i)))
				decayProduct= np.multiply(trainingImages[number],decayVal)
				weights[i,guessVal]= np.subtract(weights[i,guessVal],decayProduct)
				weights[i,int(trainingLabels[number])]=np.add(weights[i,int(trainingLabels[number])],decayProduct)

		print 'Epoch #',i,': Training Accuracy:', numberSuccess/5000.0

#This function evaluates the performance of the classifier by checking its results for all images against the solutions. The percentage of
#correct answers is returned back
def evaluation(testingResults, testLabels):
	success = 0.0
	attempts = 0.0
	for i in range(0, len(testLabels)):
		if testingResults[i] == testLabels[i]:
			success += 1.0
		attempts += 1.0
	print "The overall accuracy for the perceptron classifier is", 100*success/attempts, "%"

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
		digitCorrect.append(success/attempts)
	print "Accuracy by digit:"
	for i in range(0, len(digitCorrect)):
		print i, ": ", 100*digitCorrect[i], "%"

#This function computes the confusion matrix for the Perceptron classifier that gives the classifier's performance for all classes and provides a 
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
	print "Confusion Matrix:"
	for i in range(0,10):
		for j in range(0,10):
			confusionMatrix[i][j] /= digitFreq[i]
		print confusionMatrix[i]

# This function uses the final weights calculated by the perceptron classifier for each class and multiplies each test images by it
# and makes a guess based on which value is highest as a result of the multiplication.
def testingStep(testImages, testLabels, weights):
	prediction=[]
	for numberSample in range(0, len(testLabels)):
		result=[]
		for classVal in range(0, 10):
			product = np.multiply(weights[classVal],testImages[numberSample])
			sumVal = np.sum(product)
			result.append(sumVal)
		prediction.append(result.index(max(result)))
	return prediction

#This is the main function, which calls all functions needed to run the Perceptron classifier in order of initializing data, training the data,
#testing the data, evaluating the data, and generating a confusion matrix based on results
def main(alphaVal,bias,randomWeights,trainingOrder,epochs):
	print "Reading Training Data"
	trainingImages = convertImages(readImages("trainingImages"))
	trainingLabels = readLabels("trainingLabels")
	print "Training Data Reading Complete"

	if bias == True:
		trainingImages = np.insert(trainingImages,0,1,axis=1)

	numDigits = len(trainingImages[0])
	weights = np.zeros((epochs, 10, numDigits))
	if randomWeights == True:
		weights = np.random.rand(epochs, 10, numDigits)

	print "Evaluating Training Data..."
	trainingStep(trainingImages, trainingLabels, alphaVal, trainingOrder, epochs, weights)
	print "Training Data Evaluation Complete"

	print "Reading Testing Data..."
	testImages = convertImages(readImages("testImages"))
	testLabels = readLabels("testLabels")
	print "Test Data Reading Complete"

	if bias == True:
		testImages = np.insert(testImages,0,1,axis=1)

	print "Evaluating Testing Data"
	testingResults = testingStep(testImages, testLabels, weights[-1])
	print "Testing Complete"

	print "Evaluating Results"
	evaluation(testingResults, testLabels)
	digitEvaluation(testingResults, testLabels)
	computeConfusionMatrix(testingResults, testLabels)
	print "Evalution Complete"

# The parameters for the perceptron classifier are input manually
if __name__ == '__main__':
	while 1:
		alphaVal = raw_input("Choose Alpha Value for Learning Rate Decay Function: ")
		try:
	    		float(alphaVal)
	    		alphaVal = float(alphaVal)
	    		break
		except ValueError:
	    		print "Not a float"
# ----------------------------------------------------------------
	while 1:
		bias = raw_input("Input 0 to exclude bias or 1 to include bias: ")
		if bias == '0':
			bias = False
			break
		elif bias == '1':
			bias = True
			break
		print "Not a valid input"
# ----------------------------------------------------------------
	while 1:
		initWeights = raw_input("Input 0 to initialize zero for weights or 1 to randomize weights: ")
		if initWeights == '0':
			initWeights = False
			break
		elif initWeights == '1':
			initWeights = True
			break
		print "Not a valid input"
# ----------------------------------------------------------------
	while 1:
		trainingOrder = raw_input("Input 0 to fix training order example order or 1 to randomize training example order: ")
		if trainingOrder == '0':
			trainingOrder = False
			break
		elif trainingOrder == '1':
			trainingOrder = True
			break
		print "Not a valid input"
# ----------------------------------------------------------------
	while 1:
		epochs = raw_input("Choose number of epochs: ")
		try:
	    		int(epochs)
	    		epochs = int(epochs)
	    		break
		except ValueError:
	    		print "Not an int"

	main(alphaVal,bias,initWeights,trainingOrder,epochs)

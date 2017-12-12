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

#The purpose of this function is to create the training stage of the Bayesian classifier.
def trainingStep(trainingImages, trainingLabels, alphaVal, bias, randomWeights, trainingOrder, epochs):
	trainingImages = np.array(trainingImages)
	trainingLabels = np.array(trainingLabels)

	if bias == True:
		trainingImages = np.insert(trainingImages,0,1,axis=1)

	weights = np.zeros((epochs, 10, 28*28))
	if randomWeights == True:
		weights = np.random.rand(epochs, 10, 28*28)

	success = []
	idx = []
	for i in range(1,epochs):
		weights[i]=weights[i-1]
		Miss=np.ones(5000)
		sequence = range(5000)
		if trainingOrder:
			random.shuffle(sequence)
	
		for number in sequence:
			result=[]
			for cla in range(10):
				result.append(np.sum(np.multiply(weights[i,cla],trainingImages[number])))
		
			prediction=result.index(max(result))
			truth=int(trainingLabels[number])

			if truth==prediction:
				Miss[number]=0
			else:
				decayVal = float(alphaVal) / float(float(alphaVal) + float(i))
				mult= np.multiply(trainingImages[number],alphaVal/(alphaVal + float(i)))
				weights[i,prediction]= np.subtract(weights[i,prediction],mult)
				weights[i,truth]=np.add(weights[i,truth],mult)

		print('ep:',i,' accy: ', 1-np.sum(Miss)/5000)
		success.append(1-np.sum(Miss)/5000)
		idx.append(i)

	return weights[epochs-1]

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
def main(alphaVal,bias,randomWeights,trainingOrder,epochs):
	print "Reading Training Data"
	trainingImages = convertImages(readImages("trainingImages"))
	trainingLabels = readLabels("trainingLabels")
	print "Training Data Reading Complete"

	print "Evaluating Training Data..."
	trainingData = trainingStep(trainingImages, trainingLabels, alphaVal, bias, randomWeights, trainingOrder, epochs)
	print "Training Data Evaluation Complete"

	# print "Reading Training Data..."
	# testImages = readImages("testImages")
	# testLabels = readLabels("testLabels")
	# print "Training Data Reading Complete"
	# print "Evaluating Test Images..."
	# testingResults = testing(testImages, trainingData, trainingClassFrequencies)
	# print "Test Images Evaluated"
	
if __name__ == '__main__':
	main(100, False, False, False, 100)
# 	while 1:
# 		alphaVal = raw_input("Choose Alpha Value for Learning Rate Decay Function: ")
# 		try:
# 	    		int(alphaVal)
# 	    		alphaVal = int(alphaVal)
# 	    		break
# 		except ValueError:
# 	    		print "Not an int"
# # ----------------------------------------------------------------
# 	while 1:
# 		bias = raw_input("Input 0 to exclude bias or 1 to include bias: ")
# 		if bias == '0':
# 			bias = False
# 			break
# 		elif bias == '1':
# 			bias = True
# 			break
# 		print "Not a valid input"
# # ----------------------------------------------------------------
# 	while 1:
# 		initWeights = raw_input("Input 0 to initialize zero for weights or 1 to randomize weights: ")
# 		if initWeights == '0':
# 			initWeights = False
# 			break
# 		elif initWeights == '1':
# 			initWeights = True
# 			break
# 		print "Not a valid input"
# # ----------------------------------------------------------------
# 	while 1:
# 		trainingOrder = raw_input("Input 0 to fix training order example order or 1 to randomize training example order: ")
# 		if trainingOrder == '0':
# 			trainingOrder = False
# 			break
# 		elif trainingOrder == '1':
# 			trainingOrder = True
# 			break
# 		print "Not a valid input"
# # ----------------------------------------------------------------
# 	while 1:
# 		epochs = raw_input("Choose number of epochs: ")
# 		try:
# 	    		int(epochs)
# 	    		epochs = int(epochs)
# 	    		break
# 		except ValueError:
# 	    		print "Not an int"

# 	main(alphaVal,bias,initWeights,trainingOrder,epochs)

import numpy as np
from random import randint as rand
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, fileName, neuronsAmount, parametersAmount, entriesAmount, testingPercentage):
        self.neuronsAmount = neuronsAmount
        self.parametersAmount = parametersAmount
        self.entriesAmount = entriesAmount
        self.testingPercentage = testingPercentage

        self.readInput(fileName)
        self.normalizeInput()
        self.chooseBuildingEntries()
        self.initializeWeightMatrix()
        self.initializeBias()
        self.iterationsError = [] #array with the error of each iteration

    def readInput(self, fileName):
        file = open(fileName, "r")
        self.input = []  #the X matrix
        self.objective = []  #the D matrix

        for line in file.read().splitlines():  #get all lines from the file
            entry = []  #create a list to put all the line's parameters
            for parameter in line.split(','):
                entry.append(float(parameter))  # convert to float
            self.input.append(entry[1:])  # get all the entries

            objective = np.eye(self.neuronsAmount, dtype=int)[int(entry[0] - 1)] #1 0 0, 0 1 0, 0 0 1
            self.objective.append(objective)  # get the first value of the line, the objective value

        self.input = np.array(self.input, float)  # tranform them into an numpy array, for the future operations
        self.objective = np.array(self.objective, float)
        file.close()

    def normalizeInput(self):
        normInput = []
        for i in range(0, self.parametersAmount): #lines
            array = []
            m = max(self.input.T[i])
            for j in range(0, self.entriesAmount): #columns
                array.append((self.input.T[i][j]/m - 0.5)*2)
            normInput.append(array)

        self.input = np.array(normInput).T #transpose again
        return

    def chooseBuildingEntries(self):
        self.choosenIndex = []
        for i in range(0, int(self.entriesAmount * (1 - self.testingPercentage))):
            rnd = rand(0, self.entriesAmount - 1)
            while rnd in self.choosenIndex:
                rnd = rand(0, self.entriesAmount - 1)
            self.choosenIndex.append(rnd)

    def initializeWeightMatrix(self):
        self.weightMatrix = []  #the W matrix
        for n in range(0, self.neuronsAmount):  #iniatilize weight matrix
            array = []  # create an array
            for p in range(0, self.parametersAmount):  #one weight to each parameter
                array.append(rand(0, 10)/1000) #small random weights
            self.weightMatrix.append(array)
        self.weightMatrix = np.array(self.weightMatrix, float)

    def initializeBias(self):
        array = []
        for i in range(0, self.neuronsAmount):
            array.append(rand(0, 10)/1000)
        self.bias = np.array(array, float)[np.newaxis].T  #small random bias (vector 1x1)

    def getOutput(self, value):
        output = []
        for n in range(0, self.neuronsAmount):
            if value[n][0] <= 0:
                output.append(0)
            else:
                output.append(1)
        return np.array(output)[np.newaxis].T

    def perceptron(self, maxIterations, alpha):  #max number of iterations,
        for iteration in range(0, maxIterations):
            iterationError = 0
            for index in self.choosenIndex:
                entry = self.input[index][np.newaxis].T
                objective = self.objective[index][np.newaxis].T #transpose objective vector

                self.output = self.getOutput(self.weightMatrix.dot(entry) + self.bias) #y = f(w.x + b) #transpose output vector
                error = (objective - self.output)  #e = d - y

                self.weightMatrix = self.weightMatrix + alpha*error.dot(entry.T) #w = w + alpha*w*x #[np.newaxis] forces the correct dimension for entry
                self.bias = self.bias + alpha*error #b = b + alpha*e
                iterationError += error.T.dot(error)[0][0] #E = E + e

            if iterationError == 0.0: #tolerance
              break
            self.iterationsError.append(iterationError)

        self.plotError()
        self.test()

    def plotError(self):
        plt.plot(range(0, len(self.iterationsError)), self.iterationsError)
        plt.show()

    def test(self):
        correctOutputs = incorrectOutputs = 0
        for index in range(0, self.entriesAmount):
            if index not in self.choosenIndex:
                entry = self.input[index][np.newaxis].T
                objective = self.objective[index][np.newaxis].T  # transpose objective vector

                self.output = self.getOutput(
                    self.weightMatrix.dot(entry) + self.bias)  # y = f(w.x + b) #transpose output vector
                error = (objective - self.output)  # e = d - y
                if error.T.dot(error)[0][0] == 0:
                    correctOutputs += 1
                else:
                    incorrectOutputs += 1
        print("Correct Outputs: ", correctOutputs, " - Percentage: ", correctOutputs/(self.entriesAmount*self.testingPercentage), "%")
        print("Incorrect Outputs: ", incorrectOutputs, " - Percentage: ", incorrectOutputs/(self.entriesAmount*self.testingPercentage), "%")
        return

myNeuralNetwork = NeuralNetwork("data.txt", 3, 13, 178, 0.33) #file, neurons, parameters, entries, testing percentage
myNeuralNetwork.perceptron(1000, 0.05) #iterations, alpha

from random import randint as rand
import numpy as numpy
import matplotlib.pyplot as plt
import math

MINLIM = -550
MAXLIM = 550


def eggHolder(x1, x2):
    return -(x2 + 47)*math.sin(math.sqrt(abs(x2 + x1/2 + 47))) - x1*math.sin(math.sqrt(abs(x1 - (x2 + 47))))


class Antibody:
    def __init__(self, gene1, gene2):
        if abs(gene1) <= MAXLIM:
            self.gene1 = gene1
        elif gene1 < MINLIM:
            self.gene1 = MINLIM
        else:
            self.gene1 = MAXLIM

        if abs(gene2) <= MAXLIM:
            self.gene2 = gene2
        elif gene1 < MINLIM:
            self.gene2 = MINLIM
        else:
            self.gene2 = MAXLIM

    def evaluate(self):
        self.functionValue = eggHolder(self.gene1, self.gene2)
        self.evaluation = -self.functionValue + 1500

    def show(self):
        print("Genes: ", self.gene1, ",", self.gene2, "Evaluation: ", self.evaluation , "Function Value: ", self.functionValue)


class Population:
    def __init__(self, populationSize):
        self.populationSize = populationSize
        self.antibodies = []
        for i in range(0, self.populationSize):
            antibody = Antibody(rand(MINLIM, MAXLIM), rand(MINLIM, MAXLIM))
            self.antibodies.append(antibody)
        self.progression = []

    def iteract(self, maxIterations, cloneAmount, mutationConst, ro):
        for i in range(0, maxIterations):
            self.clone(cloneAmount)
            self.mutate(cloneAmount, mutationConst, ro)
            self.select(cloneAmount)
        self.showResults()

    def clone(self, cloneAmount):
        newPopulation = []
        for antibody in self.antibodies:
            for i in range(0, cloneAmount):
                newPopulation.append(Antibody(antibody.gene1, antibody.gene2))
        self.antibodies = list(newPopulation)

    def mutate(self, cloneAmount, mutationConst, ro):
        self.evaluate()
        for i in range(0, self.populationSize*cloneAmount):
            alpha = math.exp(-ro*(self.antibodies[i].evaluation/self.maxEvaluation))
            random = rand(0, 100)
            if random < alpha*100:
                if rand(0, 1) == 0:
                    self.antibodies[i].gene1 += alpha*mutationConst
                else:
                    self.antibodies[i].gene1 -= alpha*mutationConst

            random = rand(0, 100)
            if random < alpha*100:
                if rand(0, 1) == 0:
                    self.antibodies[i].gene2 += alpha*mutationConst
                else:
                    self.antibodies[i].gene2 -= alpha*mutationConst

    def evaluate(self):
        self.maxEvaluation = 0
        self.evaluations = []
        for antibody in self.antibodies:
            antibody.evaluate()
            if antibody.evaluation > self.maxEvaluation:
                self.maxEvaluation = antibody.evaluation

    def select(self, cloneAmount): #ranking selection
        self.evaluate()
        selectedChromosomes = []
        for i in range(0, self.populationSize):
            bestEvaluation = 0
            for j in range(0, cloneAmount):
                if self.antibodies[i*cloneAmount+j].evaluation > bestEvaluation:
                    bestEvaluation = self.antibodies[i*cloneAmount+j].evaluation
                    bestClone = self.antibodies[i*cloneAmount+j]
            selectedChromosomes.append(bestClone)
        self.antibodies = list(selectedChromosomes)

    def showPopulation(self):
        print("Population: ")
        for antibody in self.antibodies:
            antibody.show()
        print()

    def showResults(self):
        x1, x2 = numpy.meshgrid(numpy.arange(MINLIM, MAXLIM), numpy.arange(MINLIM, MAXLIM))
        Z = -(x2 + 47)*numpy.sin(numpy.sqrt(numpy.fabs(x2 + x1/2 + 47))) - x1*numpy.sin(numpy.sqrt(numpy.fabs(x1 - (x2 + 47))))
        fig, ax = plt.subplots()
        CS = ax.contour(x1, x2, Z)

        ax.clabel(CS, inline=1, fontsize=10)
        ax.set_title('Resultados Algorítmo Imunológico')

        X1 = []
        X2 = []
        for a in self.antibodies:
            X1.append(a.gene1)
            X2.append(a.gene2)

        plt.scatter(X1, X2, color='red')
        plt.show()


population = Population(100) #populationSize
population.iteract(100, 10, 10, 2) #maxIterations, cloneAmount, mutationConst, ro

from random import randint as rand
import matplotlib.pyplot as plt
import math
MINLIM = -550
MAXLIM = 550


def eggHolder(x1, x2):
    return -(x2 + 47)*math.sin(math.sqrt(abs(x2 + x1/2 + 47))) - x1*math.sin(math.sqrt(abs(x1 - (x2 + 47))))


class Chromosome:
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
        print('Genes: ', self.gene1, ",",  self.gene2, 'Evaluation: ', self.evaluation, "Function Value: ", self.functionValue)


class Population:
    def __init__(self, populationSize):
        self.populationSize = populationSize
        self.chromosomes = []
        for i in range(0, self.populationSize):
            chrome = Chromosome(rand(MINLIM, MAXLIM), rand(MINLIM, MAXLIM))
            self.chromosomes.append(chrome)
        self.progression = []
        self.evaluate()

    def iteract(self, maxIterations, crossRate, mutationRate, mutationConst):
        for i in range(0, maxIterations):	
            self.select()
            self.cross(crossRate)
            self.mutate(mutationRate, mutationConst)
            self.getProgression(i)
        self.showProgression(maxIterations)

    def evaluate(self):
        self.evaluations = []
        for chrome in self.chromosomes: #evaluate all the chromosomes
            chrome.evaluate()
            self.evaluations.append(chrome.evaluation)
        self.evaluations.sort()

    def select(self): #roullete selection
        self.selectedChromosomes = []
        for i in range(0, self.populationSize):
            random = rand(0, int(sum(self.evaluations)))
            position = 0
            for evaluation in self.evaluations:
                position += evaluation
                if random <= position:
                    chrome = self.getChromeByEvaluation(evaluation)
                    self.selectedChromosomes.append(chrome)
                    break
        self.chromosomes = list(self.selectedChromosomes)

    def getChromeByEvaluation(self, evaluation):
        for chrome in self.chromosomes:
            if chrome.evaluation == evaluation:
                return chrome

    def cross(self, crossRate):
        for i in range(0, int((self.populationSize-1)/2)):
            random = rand(0, 100)/100
            if random <= crossRate:
                alpha = rand(0, 100)/100
                gene1 = alpha*self.chromosomes[i*2].gene1 + (1-alpha)*self.chromosomes[i*2+1].gene1
                gene2 = alpha*self.chromosomes[i*2].gene2 + (1-alpha)*self.chromosomes[i*2+1].gene2
                self.chromosomes[i*2] = Chromosome(gene1, gene2)

                gene1 = alpha*self.chromosomes[i*2+1].gene1 + (1-alpha)*self.chromosomes[i*2].gene1
                gene2 = alpha*self.chromosomes[i*2+1].gene2 + (1-alpha)*self.chromosomes[i*2].gene2
                self.chromosomes[i*2+1] = Chromosome(gene1, gene2)

    def mutate(self, mutationRate, mutationConst):
        for i in range(0, self.populationSize-1):
            random = rand(0, 100)/100
            if random <= mutationRate:
                if rand(0, 1) == 0:
                    self.chromosomes[i].gene1 += mutationConst
                else:
                    self.chromosomes[i].gene1 -= mutationConst

            random = rand(0, 100)/100
            if random <= mutationRate:
                if rand(0, 1) == 0:
                    self.chromosomes[i].gene2 += mutationConst
                else:
                    self.chromosomes[i].gene2 -= mutationConst

    def showPopulation(self):			
        print("Population: ")
        for chrome in self.chromosomes:
            chrome.show()
        print()

    def showSelected(self):
        print("Selected Chromosomes: ")
        for chrome in self.selectedChromosomes:
            chrome.show()
        print()

    def getProgression(self, i):
        self.evaluate()        
        bestEvaluation = self.evaluations[len(self.evaluations)-1]
        chrome = self.getChromeByEvaluation(bestEvaluation)
        average = sum(self.evaluations)/len(self.evaluations)
        self.progression.append((chrome.evaluation, chrome.functionValue, average))

    def showProgression(self, maxIterations):
        bests = []
        values = []
        averages = []
        for p in self.progression:
            bests.append(p[0])
            values.append(p[1])
            averages.append(p[2])
            
        plt.title('Evolução da Aptidão')
        plot = plt.plot(range(0, maxIterations), bests)
        plt.setp(plot, color='r', linewidth=2.0)
        plt.show()

        plt.title('Evolução da Função Objetivo')
        plot = plt.plot(range(0, maxIterations), values)
        plt.setp(plot, color='g', linewidth=2.0)
        plt.show()
        
        plt.title('Evolução da Média')
        plot = plt.plot(range(0, maxIterations), averages)
        plt.setp(plot, color='b', linewidth=2.0)
        plt.show()


population = Population(100) #populationSize
population.iteract(100, 0.5, 0.2, 1) #maxIterations, crossRate, mutationRate, mutationConst
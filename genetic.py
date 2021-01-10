from math import ceil
from random import sample
from greedyAlgorithm import GreedyAlgorithm
from random import randint
from time import time
from math import inf


class Genetic:
    def __init__(self,
                 populationSize: int,
                 parentsNumber: int,
                 fileName: str):

        self.fileName: str = fileName

        self.procNumber    : int = 0
        self.taskNumber    : int = 0
        self.optimumValue  : int = 0
        self.parentsNumber : int = parentsNumber  if parentsNumber  >= 2 else 2
        self.populationSize: int = populationSize if populationSize >= 3 else 3

        self.procTimeArr: list = []
        self.population : list = []
        self.bestVector : list = []
        self.parents    : list = []

        self.bestTime   : float = inf
        self.startTime  : float = 0
        self.currentTime: float = 0
        self.stopTime   : float = 120

        self.populationTime : dict = {}  # key = index in self.population list, value = time for greedy algorithm
        self.setOfValues    : dict = {}  # key = task time, value = number of such times in a vector

        self.populationZero()
        self.loop()

    def populationZero(self):
        tempTaskTimeArr: list = []
        try:
            file = open(self.fileName, "r")
            self.procNumber = int(file.readline())
            self.taskNumber = int(file.readline())

            self.procTimeArr = [0] * self.procNumber
            tempTaskTimeArr = [0] * self.taskNumber

            for i in range(self.taskNumber):
                tempTaskTimeArr[i] = int(file.readline())
            file.close()
        except:
            print("File error: cannot open/read")
            exit(0)

        opt = ceil(sum(tempTaskTimeArr) / self.procNumber)
        self.optimumValue = opt if opt >= max(tempTaskTimeArr) else max(tempTaskTimeArr)
        print("Calculated optimum value:", self.optimumValue)

        tempTaskTimeSet = set(tempTaskTimeArr)
        for taskTime in tempTaskTimeSet:
            self.setOfValues[taskTime] = tempTaskTimeArr.count(taskTime)

        self.population = [sorted(tempTaskTimeArr, reverse=True), tempTaskTimeArr]
        while len(self.population) < self.populationSize:
            newChromosome = sample(tempTaskTimeArr, self.taskNumber)
            if newChromosome not in self.population:
                self.population.append(newChromosome)

    def crossover(self):
        index1: int = 0
        index2: int = 0
        while index1 == index2:
            index1 = randint(0, self.parentsNumber - 1)
            index2 = randint(0, self.parentsNumber - 1)
        return self.parents[index1][:int(self.taskNumber / 2) ] + \
               self.parents[index2][ int(self.taskNumber / 2):]

    def newChromosome(self):
        tempChild = self.crossover()
        tempSet = self.setOfValues.copy()
        missingValues: list = []
        for timeIndex in range(len(tempChild)):
            if tempSet[tempChild[timeIndex]] > 0:
                tempSet[tempChild[timeIndex]] -= 1
            else:
                missingValues.append(timeIndex)
        timeIndex = 0
        for key, val in tempSet.items():
            while val > 0:
                tempChild[missingValues[timeIndex]] = key
                val -= 1
                timeIndex += 1
        return tempChild

    def newPopulation(self):
        tempPopulationTime = sorted(self.populationTime.items(), key=lambda item: item[1])
        for vectorIndex in range(self.parentsNumber):
            self.parents.append(self.population[tempPopulationTime[vectorIndex][0]])

        self.population = [self.parents[0], self.parents[1]]
        while len(self.population) < self.populationSize:
            tempChild = self.newChromosome()
            tempChild = self.mutation(tempChild) if randint(0, 1) else tempChild
            if tempChild not in self.population:
                self.population.append(tempChild)
        self.clearArrays()

    def mutation(self, chromosome: list):
        index1: int = 0
        index2: int = 0
        while index1 == index2:
            index1 = randint(0, self.taskNumber - 1)
            index2 = randint(0, self.taskNumber - 1)
        chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
        return chromosome

    def clearArrays(self):
        self.parents.clear()
        self.populationTime.clear()

    def fitness(self):
        for chromosome in self.population:
            resultTime = GreedyAlgorithm(self.procNumber, chromosome).time()
            self.populationTime[self.population.index(chromosome)] = resultTime
            if resultTime < self.bestTime:
                self.bestTime = resultTime
                self.bestVector = chromosome

    def loop(self):
        self.startTime = time()
        while time() - self.startTime < self.stopTime and self.bestTime > self.optimumValue:
            self.fitness()
            self.newPopulation()
        print("Time for the genetic algorithm:", self.bestTime)

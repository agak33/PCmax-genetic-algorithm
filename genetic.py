from math import ceil
from random import sample
from greedyAlgorithm import GreedyAlgorithm
from random import randint
from time import time
from math import inf


class Genetic:
    def __init__(self,
                 populationSize: int,
                 fileName: str):

        self.fileName:       str = fileName

        self.procNumber:     int = 0
        self.taskNumber:     int = 0
        self.optimum:        int = 0
        self.populationSize: int = populationSize
        self.parentsNumber:  int = ceil(self.populationSize / 3)

        self.procTimeArr:    list = []
        self.population:     list = []
        self.bestVector:     list = []
        self.parents:        list = []

        self.bestTime:       float = inf
        self.startTime:      float = 0
        self.currentTime:    float = 0
        self.stopTime:       float = 20

        self.populationTime: dict = {}
        self.setOfValues:    dict = {}

        self.greedy:         object = GreedyAlgorithm(0, [])

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
            print("File error")
            exit(0)

        self.optimum = ceil(sum(tempTaskTimeArr) / self.procNumber)
        tempTimeSet = set(tempTaskTimeArr)
        for taskTime in tempTimeSet:
            self.setOfValues[taskTime] = tempTaskTimeArr.count(taskTime)

        while len(self.population) < self.populationSize:
            newChromosome = sample(tempTaskTimeArr, self.taskNumber)
            if newChromosome not in self.population:
                self.population.append(newChromosome)

    def loop(self):
        self.startTime = time()
        while True:
            self.fitness()
            self.newPopulation()
            if time() - self.startTime >= self.stopTime:
                print("Czas dla algorytmu genetycznego: ", self.bestTime)
                #GreedyAlgorithm(self.procNumber, self.bestVector).draw()
                exit(0)

    def newPopulation(self):
        # sort slownika z czasami dla poszczegolnych wektorow, gdzie
        # klucz = index w self.population, wartosc = czas dla zachlannego
        tempPopulationTime = sorted(self.populationTime.items(), key=lambda item: item[1])

        for vectorIndex in range(self.parentsNumber):                             # dodanie odpowiedniej ilosci rodzicow
            self.parents.append(self.population[tempPopulationTime[vectorIndex][0]])

        self.population = [self.parents[0], self.parents[1]]
        while len(self.population) < self.populationSize:               # tworzenie nowej
            tempSet = self.setOfValues.copy()
            index1: int = 0
            index2: int = 0
            while index1 == index2:                                     # losowanie 2 wektorow rodzicow
                index1 = randint(0, self.parentsNumber - 1)
                index2 = randint(0, self.parentsNumber - 1)
            tempChild = self.parents[index1][:int(self.taskNumber / 2)] + \
                        self.parents[index2][int(self.taskNumber / 2):]         # stworzenie potomka

            tempMissingValues: list = []
            for timeIndex in range(len(tempChild)):                                     # sprawdzenie, które wartości się powtarzają
                if tempSet[tempChild[timeIndex]] > 0:
                    tempSet[tempChild[timeIndex]] -= 1
                else:
                    tempMissingValues.append(timeIndex)     # jezeli w setcie = 0, wartośc na i-tej pozycji jest do wymiany

            timeIndex = 0
            for key, val in tempSet.items():
                while val > 0:
                    tempChild[tempMissingValues[timeIndex]] = key
                    val -= 1
                    timeIndex += 1

            if randint(0, 1):                       # losujemy czy mutujemy czy nie
                tempChild = self.mutation(tempChild)

            if tempChild not in self.population:    # jak nie ma w populacji to mozna dodac
                self.population.append(tempChild)

        self.parents.clear()
        self.populationTime.clear()

    def mutation(self, chromosome: list):
        index1: int = 0
        index2: int = 0
        while index1 == index2:
            index1 = randint(0, self.taskNumber - 1)
            index2 = randint(0, self.taskNumber - 1)
        chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
        return chromosome

    def fitness(self):
        for chromosome in self.population:
            self.greedy = GreedyAlgorithm(self.procNumber, chromosome)
            resultTime = self.greedy.time()
            self.populationTime[self.population.index(chromosome)] = resultTime
            if resultTime < self.bestTime:
                self.bestTime = resultTime
                self.bestVector = chromosome
            if resultTime <= self.optimum or resultTime == max(chromosome):
                print("algorytmem genetycznym:", resultTime)
                #self.greedy.draw()
                exit(0)

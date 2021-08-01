from math import ceil, inf
from random import sample, randint
from greedyAlgorithm import GreedyAlgorithm
from time import time
from typing import Union
from colorama import Fore


class Genetic:
    """
    Class to solve PCmax problem using genetic algorithm.
    """
    def __init__(self,
                 populationSize: int,
                 parentsNumber: int,
                 filePath: str):
        """
        Construct object to solve PCmax problem.
        Parameters:
            :param populationSize: number of chromosomes in population, minimum 3
            :param parentsNumber: number of parents created new population, minimum 2
            :param filePath: path to file with number of processors, tasks and list of their lengths
        '''Proper file format:'''
        Number of processors
        Number of tasks
        Length of the 1st task
        Length of the 2nd task
        ...
        Length of the last task
        """

        if not isinstance(populationSize, int):
            raise TypeError('Population size have to be an integer.')

        if not isinstance(parentsNumber, int):
            raise TypeError('Number of parents have to be an integer.')

        if populationSize < 3:
            raise ValueError('Minimal amount of population size must be at least 3.')

        if parentsNumber < 2:
            raise ValueError('Minimal amount of parents have to be at least 2.')

        if populationSize < parentsNumber:
            raise ValueError('Population size cannot be larger than the parents number.')

        # values given in parameters
        self.__filePath      : str = filePath
        self.__parentsNumber : int = parentsNumber
        self.__populationSize: int = populationSize

        self.__procNumber : int  = 0
        self.__taskNumber : int  = 0
        self.__procTimeArr: list = []
        self.__taskTimeArr: list = []

        # lists with chromosomes (whole population, parents)
        self.__population : list = []
        self.__parents    : list = []

        # attributes to store the best solution value and vector
        self.__bestSolutionValue   : float = inf
        self.__bestSolutionVector  : list = []

        # dictionary to store value for every chromosome
        self.__populationFitness  : dict = {}  # key = index in self.population list, value = time for greedy algorithm
        # dictionary to store information about number of the same lengths (needed for error correction)
        self.__setOfTaskTimes     : dict = {}  # key = task time, value = number of such times in a vector

        self.readFile()

    @property
    def optimum(self):
        """
        Calculate optimum value of given problem.
        :return: Optimum value or none if file was not read
        """
        try:
            opt = ceil(sum(self.__taskTimeArr) / self.__procNumber)
            maxTaskTime = max(self.__taskTimeArr)
            return max(opt, maxTaskTime)
        except ZeroDivisionError:
            return None

    @property
    def solutionValue(self):
        return self.__bestSolutionValue if self.__bestSolutionValue != 0 else None

    @property
    def solutionVector(self):
        return self.__bestSolutionVector if self.__bestSolutionVector != [] else None

    @property
    def procNumber(self):
        return self.__procNumber

    @property
    def taskNumber(self):
        return self.__taskNumber

    @property
    def procTimeArr(self):
        return self.__procTimeArr

    @property
    def taskTimeArr(self):
        return self.__taskTimeArr

    @property
    def filePath(self):
        return self.__filePath

    @property
    def parentsNumber(self):
        return self.__parentsNumber

    @property
    def populationSize(self):
        return self.__populationSize

    @filePath.setter
    def filePath(self, value):
        self.__filePath = value
        self.readFile()

    @parentsNumber.setter
    def parentsNumber(self, value):
        if not isinstance(value, int):
            raise TypeError('Number of parents have to be an integer.')
        if value < 2:
            raise ValueError('Minimal amount of parents have to be at least 2.')
        if self.__populationSize < value:
            raise ValueError('Population size cannot be larger than the parents number.')
        self.__parentsNumber = value

    @populationSize.setter
    def populationSize(self, value):
        if not isinstance(value, int):
            raise TypeError('Population size have to be an integer.')
        if value < 3:
            raise ValueError('Minimal amount of population size must be at least 3.')
        if value < self.__parentsNumber:
            raise ValueError('Population size cannot be larger than the parents number.')
        self.__populationSize = value

    def readFile(self) -> bool:
        """
        Read all data from file (number of processors, number of tasks, list of tasks lengths).
        :return: bool (true if file was read, false otherwise)
        """
        try:
            file = open(self.filePath, "r")
            self.__bestSolutionVector, self.__bestSolutionVector = inf, []
            self.__procNumber = int(file.readline())
            self.__taskNumber = int(file.readline())

            if self.__procNumber <= 0 or self.__taskNumber <= 0:
                raise ValueError('Number of tasks and processors have to be positive.')

            self.__procTimeArr = [0] * self.__procNumber
            self.__taskTimeArr = [int(file.readline()) for _ in range(self.__taskNumber)]

            for task in self.__taskTimeArr:
                if task <= 0:
                    raise ValueError('Length of task have to be positive.')

            file.close()
            return True
        except FileNotFoundError:
            print(f'{Fore.RED}File error: cannot open {self.filePath}.{Fore.RESET}')
        except ValueError as e:
            print(f'{Fore.RED}{str(e)}{Fore.RESET}')
        self.__procNumber, self.__taskNumber = 0, 0
        self.__procTimeArr, self.__taskTimeArr = [], []
        return False

    def __populationZero(self):
        """
        Create first population using vector with tasks lengths read from file.
        :return: None
        """
        for taskTime in self.__taskTimeArr:
            if taskTime in self.__setOfTaskTimes:
                self.__setOfTaskTimes[taskTime] += 1
            else:
                self.__setOfTaskTimes[taskTime] = 1

        self.__population = [sorted(self.__taskTimeArr, reverse=True), self.__taskTimeArr]
        currPopulationSize = 2
        while currPopulationSize < self.__populationSize:
            newChromosome = sample(self.__taskTimeArr, self.__taskNumber)
            if newChromosome not in self.__population:
                self.__population.append(newChromosome)
                currPopulationSize += 1

    def __crossover(self):
        """
        Draw dwo parents and create list consist of half first parent and half second.
        :return: New chromosome with some errors
        """
        index1: int = 0
        index2: int = 0
        while index1 == index2:
            index1 = randint(0, self.__parentsNumber - 1)
            index2 = randint(0, self.__parentsNumber - 1)
        return self.__parents[index1][:int(self.__taskNumber / 2) ] + \
               self.__parents[index2][ int(self.__taskNumber / 2):]

    def __newChromosome(self):
        """
        Generate new chromosome using crossover method, contains error correction
        :return: New chromosome without errors
        """
        tempChild = self.__crossover()
        tempSet =   dict(
                        sample(
                            list(self.__setOfTaskTimes.copy().items()),
                            len(self.__setOfTaskTimes)
                        )
                    )

        # errors correction
        # 1. Find positions with wrong values
        missingValues: list = []
        for taskIndex, taskTime in enumerate(tempChild):
            if tempSet[taskTime] > 0:
                tempSet[taskTime] -= 1
            else:
                missingValues.append(taskIndex)
        # 2. Correct founded positions
        missValueIndex = 0
        for key, val in tempSet.items():
            while val > 0:
                tempChild[missingValues[missValueIndex]] = key
                val -= 1
                missValueIndex += 1

        return tempChild

    def __mutation(self, chromosome: list):
        """
        Draw two positions in chromosome and swap values on them.
        :param chromosome: chromosome from population
        :return: chromosome after mutation
        """
        index1: int = 0
        index2: int = 0
        while index1 == index2:
            index1 = randint(0, self.__taskNumber - 1)
            index2 = randint(0, self.__taskNumber - 1)
        chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
        return chromosome

    def __newPopulation(self):
        """
        Create new population based on current one.
        Drawn parents from population and create new chromosomes. Child has 1/5 chance
        for mutation.
        :return: None
        """
        tempPopulationTime = sorted(self.__populationFitness.items(), key=lambda item: item[1])
        for vectorIndex in range(self.__parentsNumber):
            self.__parents.append(self.__population[tempPopulationTime[vectorIndex][0]])

        self.__population = [self.__parents[0], self.__parents[1]]
        currPopSize = 2
        while currPopSize < self.__populationSize:
            tempChild = self.__newChromosome()
            tempChild = self.__mutation(tempChild) if randint(1, 5) == 1 else tempChild
            if tempChild not in self.__population:
                self.__population.append(tempChild)
                currPopSize += 1
        self.__clearArrays()

    def __clearArrays(self):
        """
        Clear list with parents and dictionary with information about result of every
        chromosome in population
        :return: None
        """
        self.__parents.clear()
        self.__populationFitness.clear()

    def __fitness(self):
        """
        Calculate solution time for every chromosome in population using greedy algorithm.
        :return: None
        """
        for index, chromosome in enumerate(self.__population):
            resultTime = GreedyAlgorithm(self.__procNumber, chromosome).time
            self.__populationFitness[index] = resultTime
            if resultTime < self.__bestSolutionValue:
                self.__bestSolutionValue  = resultTime
                self.__bestSolutionVector = chromosome
                print(f'New solution founded: {self.__bestSolutionValue}')

    def solve(self, maxTime: Union[int, float] = 10):
        """
        Solve PCmax problem using genetic algorithm.
        :param maxTime: maximal time of calculating solution value (in seconds). Default 2 minutes.
        :return: founded value, minimal time required to do all tasks
        """
        optimalValue = self.optimum
        if optimalValue is None:
            print(f'{Fore.RED}It\'s not possible to calculate a solution - file was not read properly.{Fore.RESET}')
            return None
        print(f'Optimal value: {optimalValue}')

        startTime = time()
        self.__populationZero()
        self.__fitness()
        while time() - startTime < maxTime and self.__bestSolutionValue > optimalValue:
            self.__newPopulation()
            self.__fitness()

        print(f'Best solution value founded: {self.__bestSolutionValue}')
        answer = ''
        while answer != 'y' and answer != 'n':
            answer = input(f'Would you like to draw the solution? [y/n]  ')
        if answer == 'y':
            GreedyAlgorithm(self.__procNumber, self.__bestSolutionVector).draw()
        return self.__bestSolutionValue

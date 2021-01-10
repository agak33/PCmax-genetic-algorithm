from genetic import Genetic
from data import Data
from greedyAlgorithm import GreedyAlgorithm


populationSize: int = 15
parentsNumber: int = 6
fileName = "test.txt"

file = Data(1, 100,
            101, 1000,
            1, 100,
            fileName)
file.generateFile()

Genetic(populationSize, parentsNumber, fileName)


f = open(fileName, "r")
procNumber = int(f.readline())
taskNumber = int(f.readline())
procTimeArr = [0] * procNumber
taskTimeArr = [0] * taskNumber

for i in range(taskNumber):
    taskTimeArr[i] = int(f.readline())
f.close()

greedy = GreedyAlgorithm(procNumber, taskTimeArr)
print("Time for the greedy algorithm:", greedy.time())
from genetic import Genetic
from data import Data
from greedyAlgorithm import GreedyAlgorithm

# m10n200.txt
# zachlanny: 11 972
# genetyczny: 11 002

# m25.txt
# zachlanny: 4072
# genetyczny: 3481

# m50.txt
# zachlanny: 200
# genetyczny: 173

# m50n200.txt
# zachlanny: 1222
# genetyczny: 1013

# m50n1000.txt
# zachlanny: 10 313
# genetyczny: 9890

fileName: str = "m50.txt"
populationSize: int = 15

file = Data(20, 25,              # liczba procków (od - do)
            100, 500,            # liczba zadań (od - do)
            1, 100,            # czas zadania (od - do)
            fileName)          # nazwa pliku

#file.generateFile()

f = open(fileName, "r")
procNumber = int(f.readline())
taskNumber = int(f.readline())

procTimeArr = [0] * procNumber
taskTimeArr = [0] * taskNumber

for i in range(taskNumber):
    taskTimeArr[i] = int(f.readline())
f.close()

greedy = GreedyAlgorithm(procNumber, taskTimeArr)
print("algorytmem zachlannym:", greedy.time())

Genetic(populationSize, fileName)

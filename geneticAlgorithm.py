import random

class GeneticAlgorithm:
    def __init__(self,
                 procNum: int,
                 taskArr: list):

        self.procNumber: int = procNum
        self.taskNumber: int = len(taskArr)

        self.procTimeArr: list = [0] * procNum
        self.taskTimeArr: list = taskArr

    def time(self):
        for task in self.taskTimeArr:
            index = self.procTimeArr.index(min(self.procTimeArr))
            self.procTimeArr[index] += task

        return max(self.procTimeArr)
    def losuj(self,nieUzyte):
        losowa = int()
        # nieUzyte = bool([]*self.taskNumber)

        losowa = self.taskTimeArr.index(random.choice(self.taskTimeArr))
        while nieUzyte[losowa]==True:
            losowa = self.taskTimeArr.index(random.choice(self.taskTimeArr))
        nieUzyte[losowa] = True;
        return self.taskTimeArr[losowa]

    def firstPopulation(self):

        temp = self.taskTimeArr
        n = self.procNumber // self.taskNumber
        # population = [self.procNumber][n]
        nieUzyte = [False for i in range(self.taskNumber)]
        population = [[-1 for i in range(n)] for j in range(self.procNumber)]
        for proc in range(self.taskNumber):
            for task in range(n):
                population[proc][task] = self.losuj(nieUzyte)




    def krzyzuj(self):
         return 0

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt


class GreedyAlgorithm:
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

    def draw(self):
        self.procTimeArr = [0] * self.procNumber
        solution = plt.figure()
        ax = solution.add_subplot(111)

        for task in self.taskTimeArr:
            index = self.procTimeArr.index(min(self.procTimeArr))

            rec = Rectangle((self.procTimeArr[index], index), task, 1,
                            facecolor='blue', edgecolor='black')
            ax.add_patch(rec)

            self.procTimeArr[index] += task

        solution_time = max(self.procTimeArr)
        #print("Time: {}".format(solution_time))

        plt.title("Solution")
        plt.xticks([i for i in range(solution_time + 1)])
        plt.xlabel("Time")
        plt.yticks([i for i in range(self.procNumber + 1)])
        plt.ylabel("Processor")
        plt.show()

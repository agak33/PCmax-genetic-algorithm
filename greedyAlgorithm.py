from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from typing import List
from task import Task


class GreedyAlgorithm:
    """
    Class to solve PCmax problem using greedy algorithm.
    """
    def __init__(self,
                 procNum: int,
                 taskArr: List[int]):
        """
        Construct new object to solve PCmax problem.
        Parameters:
            :param procNum: number of processors, positive integer
            :param taskArr: list with lengths of tasks, list of positive integers, can be empty
        """
        if not isinstance(procNum, int) or procNum <= 0:
            raise Exception('Number of processors have to be a positive integer.')

        if not isinstance(taskArr, list):
            raise Exception('Lengths of tasks have to be a list.')

        for task in taskArr:
            if not isinstance(task, int) or task <= 0:
                raise Exception('Lengths of tasks have to be a positive integer.')

        # integers
        self.__procNum: int = procNum
        self.__taskNum: int = len(taskArr)

        # lists
        self.__procTimeArr: list = [0] * procNum
        self.__taskTimeArr: list = taskArr

        # list of rectangles coordinates to draw solution on the plot
        self.__rectCoord: list[Task] = []

    @property
    def procNum(self):
        return self.__procNum

    @property
    def taskNum(self):
        return len(self.__taskTimeArr)

    @property
    def procTimeArr(self):
        return self.__procTimeArr

    @property
    def taskTimeArr(self):
        return self.__taskTimeArr

    @property
    def time(self) -> int:
        """
        Distribute tasks between processors using greedy algorithm.
        :return: minimal time required to do all tasks
        """
        self.__procTimeArr: list = [0] * self.__procNum
        self.__rectCoord  : list[Task] = []
        for task in self.__taskTimeArr:
            index = self.__procTimeArr.index(min(self.__procTimeArr))
            self.__rectCoord.append(Task(self.__procTimeArr[index],
                                         index + 0.5,
                                         task,
                                         1))
            self.__procTimeArr[index] += task

        return max(self.__procTimeArr)

    # setters
    @procNum.setter
    def procNum(self, value):
        if not isinstance(value, int) or value <= 0:
            raise Exception('Number of processors have to be a positive integer.')
        self.__procNum = value
        self.__procTimeArr = [0] * value

    @taskTimeArr.setter
    def taskTimeArr(self, value):
        if not isinstance(value, list):
            raise Exception('Lengths of tasks have to be a list.')
        for task in value:
            if not isinstance(task, int) or task <= 0:
                raise Exception('Lengths of tasks have to be a positive integer.')
        self.__taskTimeArr = value

    def draw(self):
        """
        Draw solution using matplotlib package. All tasks are shown on the plot as blue rectangles.
        :return: nothing
        """
        solution = plt.figure()
        solution_time = self.time

        ax = solution.add_subplot(111)
        for rectCoord in self.__rectCoord:
            rec = Rectangle((rectCoord.x, rectCoord.y),
                             rectCoord.width, rectCoord.height,
                             facecolor='blue', edgecolor='black')
            ax.add_patch(rec)

        plt.title(f'PCmax solution time: {solution_time}')
        plt.xticks([i for i in range(solution_time + 1)])
        plt.xlabel("Time")
        plt.yticks([i for i in range(self.__procNum + 1)])
        plt.ylim((0.5, self.__procNum + 0.5))
        plt.ylabel("Processor")
        plt.show()

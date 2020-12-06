from random import randint


class Data:
    def __init__(self,
                 minProc: int,
                 maxProc: int,
                 minTask: int,
                 maxTask: int,
                 minTaskLength: int,
                 maxTaskLength: int,
                 fileName: str):

        self.MIN_PROC_COUNT: int = minProc
        self.MAX_PROC_COUNT: int = maxProc

        self.MIN_TASK_COUNT: int = minTask
        self.MAX_TASK_COUNT: int = maxTask

        self.MIN_TASK_LENGTH: int = minTaskLength
        self.MAX_TASK_LENGTH: int = maxTaskLength
        self.FILE_NAME: str = fileName

    def generateFile(self):
        file = open(self.FILE_NAME, "w")

        procCount = randint(self.MIN_PROC_COUNT, self.MAX_PROC_COUNT)
        file.write(str(procCount) + "\n")

        taskCount = randint(self.MIN_TASK_COUNT, self.MAX_TASK_COUNT)
        file.write(str(taskCount) + "\n")

        for i in range(taskCount):
            taskLength = randint(self.MIN_TASK_LENGTH, self.MAX_TASK_LENGTH)
            file.write(str(taskLength) + "\n")

        file.close()

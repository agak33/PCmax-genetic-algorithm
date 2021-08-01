from random import randint
from colorama import Fore


class Data:
    """
    Class to generate file with random number of processors, tasks and their lengths, depends
    on parameters given in the constructor.
    """
    def __init__(self,
                 minProcCount: int,
                 maxProcCount: int,
                 minTaskCount: int,
                 maxTaskCount: int,
                 minTaskLength: int,
                 maxTaskLength: int):
        """
        Construct object to generate file.
        Parameters:
            :param minProcCount: minimal number of processors
            :param maxProcCount: maximal number of processors
            :param minTaskCount: minimal number of tasks
            :param maxTaskCount: maximal number of tasks
            :param minTaskLength: minimal length of a single task
            :param maxTaskLength: maximal length of a single task
        All arguments have to be positive integers. Obviously, maximals have to be equal or greater to the minimals.
        """
        if not (
                isinstance(minTaskCount, int) and isinstance(maxTaskCount, int) and
                isinstance(minProcCount, int) and isinstance(maxProcCount, int) and
                isinstance(minTaskLength, int) and isinstance(maxTaskLength, int)
        ):
            raise TypeError('All arguments in constructor have to be integers.')

        if minProcCount > maxProcCount or minProcCount <= 0:
            raise ValueError('Maximal amount of processors needs to be greater or equal to the minimal '
                             'and they must be positive.')

        if minTaskCount > maxTaskCount or minTaskCount <= 0:
            raise ValueError('Maximal amount of tasks needs to be greater or equal to the minimal '
                             'and they must be positive.')

        if minTaskLength > maxTaskLength or minTaskLength <= 0:
            raise ValueError('Maximal length of task needs to be greater or equal to the minimal '
                             'and they must be positive.')

        self.__minProcCount: int = minProcCount
        self.__maxProcCount: int = maxProcCount

        self.__minTaskCount: int = minTaskCount
        self.__maxTaskCount: int = maxTaskCount

        self.__minTaskLength: int = minTaskLength
        self.__maxTaskLength: int = maxTaskLength

        # strings to raise proper exceptions
        self.__miniValException: str = 'Minimum have to be less or equal to the maximum '\
                                       'and it must be positive.'
        self.__maxiValException: str = 'Maximum have to be greater or equal to the minimum '\
                                       'and it must be positive.'
        self.__typeException: str = 'Value given in parameter have to be an integer.'

    # getters
    @property
    def minProcCount(self):
        return self.__minProcCount

    @property
    def maxProcCount(self):
        return self.__maxProcCount

    @property
    def minTaskCount(self):
        return self.__minTaskCount

    @property
    def maxTaskCount(self):
        return self.__maxTaskCount

    @property
    def minTaskLength(self):
        return self.__minTaskLength

    @property
    def maxTaskLength(self):
        return self.__maxTaskLength

    # setters
    @minProcCount.setter
    def minProcCount(self, value):
        if not isinstance(value, int):
            raise TypeError(self.__typeException)
        if value > self.__maxProcCount or value <= 0:
            raise ValueError(self.__miniValException)
        self.__minProcCount = value

    @maxProcCount.setter
    def maxProcCount(self, value):
        if not isinstance(value, int):
            raise TypeError(self.__typeException)
        if value < self.__minProcCount or value <= 0:
            raise ValueError(self.__maxiValException)
        self.__maxProcCount = value

    @minTaskCount.setter
    def minTaskCount(self, value):
        if not isinstance(value, int):
            raise TypeError(self.__typeException)
        if value > self.__maxTaskCount or value <= 0:
            raise ValueError(self.__miniValException)
        self.__minTaskCount = value

    @maxTaskCount.setter
    def maxTaskCount(self, value):
        if not isinstance(value, int):
            raise TypeError(self.__typeException)
        if value < self.__minTaskCount or value <= 0:
            raise ValueError(self.__maxiValException)
        self.__maxTaskCount = value

    @minTaskLength.setter
    def minTaskLength(self, value):
        if not isinstance(value, int):
            raise TypeError(self.__typeException)
        if value > self.__maxTaskLength or value <= 0:
            raise ValueError(self.__miniValException)
        self.__minTaskLength = value

    @maxTaskLength.setter
    def maxTaskLength(self, value):
        if not isinstance(value, int):
            raise TypeError(self.__typeException)
        if value < self.__minTaskLength or value <= 0:
            raise ValueError(self.__maxiValException)
        self.__maxTaskLength = value

    def generateFile(self,
                     filePath: str) -> bool:
        """
        Generate file with random number of processors, tasks and list of tasks lengths.
        Numbers are drawn based on attributes values.
            :param filePath: path to the file, where all data will be written. If it doesn't exists, it will be created.
                             (only file, not the whole path)
            :return: bool (true if file was created, false otherwise)
        """
        try:
            file = open(filePath, 'w')

            procCount = randint(self.__minProcCount, self.__maxProcCount)
            file.write(str(procCount) + '\n')

            taskCount = randint(self.__minTaskCount, self.__maxTaskCount)
            file.write(str(taskCount) + '\n')

            for _ in range(taskCount):
                taskLength = randint(self.__minTaskLength, self.__maxTaskLength)
                file.write(str(taskLength) + '\n')

            file.close()
            print(f'{filePath} created')
            return True
        except FileNotFoundError:
            print(f'{Fore.RED}{filePath}: directory not found{Fore.RESET}')
            return False

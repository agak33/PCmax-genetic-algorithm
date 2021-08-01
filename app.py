from genetic import Genetic
from data import Data
from colorama import Fore


class App:
    def __init__(self):
        """
        Start the app.
        """
        print('{:-^100}'.format(' PCmax solver '))
        self.state = -1
        self.mainMenu()

    def mainMenu(self) -> None:
        """
        Menu with choices for user.
        :return: None
        """
        while self.state != 0:
            print('Choose one option from all given below (type a number):')
            print('1 - generate file with random amount of processors, and tasks')
            print('2 - solve PCmax problem using genetic algorithm')
            print('0 - exit')
            self.state = -1
            while self.state not in ['0', '1', '2']:
                self.state = input('Your choice: ')
            getattr(self, f'state_{self.state}')()

    def state_0(self) -> None:
        """
        Changes state attribute to zero to exit the program.
        :return: None
        """
        self.state = 0

    def state_1(self) -> None:
        """
        Menu for generating input file.
        :return: None
        """
        print('{:-^100}'.format(' File generator '))
        minProc, maxProc = self.get2int('Give minimal and maximal amount of processors '
                                        '(2 integers separate with space): ')
        minTask, maxTask = self.get2int('Give minimal and maximal amount of tasks '
                                        '(2 integers separate with space): ')
        minTime, maxTime = self.get2int('Give minimal and maximal time of a single task '
                                        '(2 integers separate with space): ')
        path = ''
        while not path:
            path = input('Give path to file (0 - come back to main menu): ')
        if path != '0':
            try:
                Data(minProc, maxProc,
                     minTask, maxTask,
                     minTime, maxTime).generateFile(path)
            except ValueError as e:
                print(f'{Fore.RED}Failed to create a file: {str(e)}{Fore.RESET}')
        print('-' * 100)

    def state_2(self) -> None:
        """
        Menu for genetic algorithm.
        :return: None
        """
        print('{:-^100}'.format(' Genetic solver '))
        population, parents = self.get2int('Give population size and amount od parents '
                                           '(2 integers separated with space): ')

        path = ''
        while not path:
            path = input('Give path to input file (0 - come back to main menu): ')
        if path != '0':
            try:
                Genetic(population, parents, path).solve()
            except ValueError as e:
                print(f'{Fore.RED}Failed to create an object: {str(e)}{Fore.RESET}')
        print('-' * 100)

    @staticmethod
    def get2int(message) -> [int, int]:
        """
        Takes two integers from the user.
        :param message: Message displays to user during taking values
        :return: two integers, in order given by the user
        """
        int1, int2 = None, None
        while int1 is None and int2 is None:
            try:
                int1, int2 = [int(x) for x in input(message).split()]
            except ValueError or TypeError:
                print(f'{Fore.RED}Wrong values. Try again.{Fore.RESET}')
        return int1, int2

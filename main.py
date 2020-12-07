from data import Data
from geneticAlgorithm import GeneticAlgorithm
fileName: str = "test.txt"

file = Data(10, 10,            # liczba procków (od - do)
            20, 20,            # liczba zadań (od - do)
            1, 20,             # czas zadania (od - do)
            fileName)          # nazwa pliku

file.generateFile()

genAlg = GeneticAlgorithm(3,[1,2,4])
genAlg.firstPopulation()

# tutaj wywolanie genetycznego jeszcze bedzie

# Genetic algorithm to solve PCmax problem

## Main files
* data.py: to generate an input file for the PCmax problem
* greedyAlgorithm.py: to solve PCmax problem using a greedy algorithm
* genetic.py: to solve PCmax problem using genetic algorithm
* app.py: creates console menu for the user

More information about all classes and methods is written in files.

## General info
A single chromosome is represented by a vector of all tasks lengths 
given in the input file. The population is a collection of such 
vectors, and each individual has a different tasks order.

Population zero included input vector and sorted one in 
descending order. Rest vectors are created by combining values 
from the original vector in random order.

During the crossing, two chromosomes from the set of "parents" are 
drawn. Then, there's creating a new vector, which contains half of 
the elements from the first chromosome (values are taken from 
parent's indexes from 0 to ceil(task_number / 2) - 1) and a half 
from the second one (values are taken from parent's indexes from 
ceil(task_number / 2) to task_number - 1). This method produces 
some errors in the new vector - some values are missing, some are 
too many. It needs a correction, so redundant values are replaced 
by the missing ones.

The chance to occur a mutation is 1:5. It was implemented by 
swapping two values on random positions in a chromosome.

The fitness of the chromosome is calculated based on the difference 
between the optimum and time using a greedy algorithm. The less 
this value is, the higher fitness it has.

The new generation included one vector with the best fitness. 
Rest are created by crossing and mutating.

Recommended population size is 15 - 20 with 5 - 10 parents.

## Restrictions

Minimal population size is 3, amount of parents is 2. Minimal 
number of tasks is 3. The set of parents cannot be bigger 
than the whole population.

In the file generator, given minimal values have to be less 
or equal to the maximums.

In this project, there's no implemented method to check if 
they're enough different values in chromosomes or the number 
of parents to create a population in a given size.

## Input file format
All values in a file have to be integers.
```angular2html
amount_of_processors
amount_of_tasks
length_of_the_1st_task
length_of_the_2nd_task
...
length_of_the_last_task
```

In the ```files``` folder there're some exemplary txt files.

## Installation
```angular2html
git clone https://https://github.com/agak33/PCmax-genetic-algorithm
```
## Running the app
If you don't want to use the app menu, you can command it (in ```main.py```):
```angular2html
App()
```
To create an object to solve a genetic problem:
```angular2html
obj = Genetic(population_size, parents_number, path_to_input_file)
```
To solve the problem, there's a need to call solve() method:
```angular2html
obj.solve(solving_time)
```
solving_time is a maximal time of calculation (in seconds). 
When it passes, the best founded value is printed (and also returned). 
This parameter is set to 120 seconds as a default.

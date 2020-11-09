from random import randint

# parameters
MIN_PROC_COUNT: int = 5
MAX_PROC_COUNT: int = 15

MIN_TASK_COUNT: int = 15
MAX_TASK_COUNT: int = 25

MIN_TASK_LENGTH: int = 1
MAX_TASK_LENGTH: int = 8
FILE_NAME: str = "test.txt"  # (or full path)


# generate file
file = open(FILE_NAME, "w")

proc_count = randint(MIN_PROC_COUNT, MAX_PROC_COUNT)
file.write(str(proc_count) + "\n")

task_count = randint(MIN_TASK_COUNT, MAX_TASK_COUNT)
file.write(str(task_count) + "\n")

for i in range(task_count):
    task_length = randint(MIN_TASK_LENGTH, MAX_TASK_LENGTH)
    file.write(str(task_length) + "\n")

file.close()

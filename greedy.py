from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

choice = 0
ProcCount, TaskCount = 0, 0


def find_solution(task_time, proc_time):
    solution = plt.figure()
    ax = solution.add_subplot(111)

    for task in task_time:
        index = proc_time.index(min(proc_time))

        rec = Rectangle((proc_time[index], index), task, 1,
                        facecolor='blue', edgecolor='black')
        ax.add_patch(rec)

        proc_time[index] += task

    solution_time = max(proc_time)
    print("Time: {}".format(solution_time))

    plt.title("Solution")
    plt.xticks([i for i in range(solution_time + 1)])
    plt.xlabel("Time")
    plt.yticks([i for i in range(ProcCount + 1)])
    plt.ylabel("Processor")
    plt.show()


while choice > 3 or choice < 1:
    try:
        choice = int(input("Please enter one of these values:\n"
                           "1 - input from file\n"
                           "2 - input from keyboard\n"
                           "3 - exit\n"))
    except:
        continue

if choice == 1:
    file_name = str(input("Please enter the name of the file (or full path): "))
    try:
        file = open(file_name, "r")
        ProcCount = int(file.readline())
        TaskCount = int(file.readline())

        proc_time = [0] * ProcCount
        task_time = [0] * TaskCount

        for i in range(TaskCount):
            task_time[i] = int(file.readline())

        file.close()
        find_solution(task_time, proc_time)
    except:
        print("File error")

elif choice == 2:
    while ProcCount < 1:
        try:
            ProcCount = int(input("Please enter the number of processors (integer): "))
        except:
            continue
    while TaskCount < 1:
        try:
            TaskCount = int(input("Please enter the number of tasks (integer): "))
        except:
            continue

    proc_time = [0] * ProcCount
    task_time = [0] * TaskCount

    for i in range(TaskCount):
        while task_time[i] < 1:
            try:
                task_time[i] = int(input("Please enter the length of task number {} (integer): ".format(i + 1)))
            except:
                continue
    find_solution(task_time, proc_time)

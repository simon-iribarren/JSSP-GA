from utils import readFilePairs
from jspGA import genetic

target = None

population_size=int(input('Please input the size of population (default: 30): ') or 30)
mutation_rate=float(input('Please input the size of Mutation Rate (default 0.2): ') or 0.2)
iterations=int(input('Please input number of iteration (default 2000): ') or 2000)

#target=int(input('Please input a target for the makespan result (default None): ') or None)

times, machines, n = readFilePairs("cases/15_15_1")
genetic(times, machines, n, population_size, iterations, mutation_rate, target)



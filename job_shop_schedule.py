import random
import copy
from utils import readFilePairs
from calculateMakespan import calculateMakespan
from GAOperations import checkDiversity, generate_population, getFitness, evolve

def genetic(times, machines, n, population_number, iterations, rate):
    machine_number = len(machines[0])
     
    def sortAndGetBestIndividual(population):
        best_individual = None
        best_result = None
        for individual in population:
            result = None
            if not individual[1]: 
                result, table = calculateMakespan(times, machines, individual[0], n)
                individual[1] = result
            else: 
                result = individual[1]

            if not best_result or result < best_result:
                best_result = result
                best_individual = individual

        population.sort(key=lambda x: x[1])
        return best_individual, best_result

    population = generate_population(population_number, n, machine_number)
    global_best_ind, global_best = sortAndGetBestIndividual(population)

    for i in range(iterations):
        population = evolve(population, rate)
        best_ind, best_result = sortAndGetBestIndividual(population)
        total_fitness, diffPercentage = getFitness(population)

        if(not global_best or best_result < global_best):
            print("iteration %s result %s" %(i, best_result))
            global_best = best_result
            global_best_ind = copy.deepcopy(best_ind)

        checkDiversity(population, diffPercentage, n, machine_number)

    
    best_result, best_table = calculateMakespan(times, machines, global_best_ind[0], n)           
    print("OVERALL RESULT")
    print("TABLE:")
    i = 1
    for row in best_table:
        print("M%s: %s" %(i, row))
        i += 1
    print("RESULT: %s" %best_result)                 
    print("ORDER: %s" %best_ind[0])
    
times, machines, n = readFilePairs("cases/15_15_1")
genetic(times, machines, n, 40, 50000, 0.1)



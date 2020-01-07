import copy
import time
import sys
from calculateMakespan import calculateMakespan
from GAOperations import checkDiversity, generate_population, getFitness, evolve
from plotResult import plotResult
from utils import fromPermutation



def printProgress(bestValue, iterations, timeElapsed):
    sys.stdout.write("\rIterations: {0} | Best result found {1} | Time elapsed: {2}s".format(iterations, bestValue, int(timeElapsed)))
    sys.stdout.flush()

def genetic(times, machines, n, population_number, iterations, rate, target):
    machine_number = len(machines[0])
    start_time = time.time()

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
    
    ##if we don't define a target we set the number of iterations we want 
    if not target:
        for i in range(iterations):
            population = evolve(population, rate)
            best_ind, best_result = sortAndGetBestIndividual(population)
            total_fitness, diffPercentage = getFitness(population)

            if(not global_best or best_result < global_best):
                global_best = best_result
                global_best_ind = copy.deepcopy(best_ind)

            printProgress(best_result, i, time.time() - start_time)
            checkDiversity(population, diffPercentage, n, machine_number)
    else:
        #If we define a target we iterate until the best result reach that target
        i = 0
        while(target < global_best):
            i += 1
            #in every iteration: 
            #We evolve the population
            population = evolve(population, rate)
            #We find the best individual 
            best_ind, best_result = sortAndGetBestIndividual(population)
            #We calculate the diversity % between the population and the total_fitness(sum of all the results)
            total_fitness, diffPercentage = getFitness(population)

            #if the result found is better than the global found we update the global
            if(not global_best or best_result < global_best):
                global_best = best_result
                global_best_ind = copy.deepcopy(best_ind)
            #We print the progress so far and the time elapsed
            printProgress(best_result, i, time.time() - start_time)
            #We check the diversity, in case the diversity percentage is very low we delete a number of the population and we add randome members
            checkDiversity(population, diffPercentage, n, machine_number)

    
    best_result, best_table = calculateMakespan(times, machines, global_best_ind[0], n)           
    print("\nOVERALL RESULT")
    print("RESULT: %s" %best_result)                 
    print('the elapsed time:%ss'% (int(time.time() - start_time)))
    print("Permutation: ")
    print(fromPermutation(global_best_ind[0], n))
    plotResult(best_table, best_result)
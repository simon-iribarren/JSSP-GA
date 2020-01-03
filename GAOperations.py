import random
from utils import swap_rnd

def removeFromList(parent, list):
    seen = set()
    seen_add = seen.add
    return [x for x in parent if not (x in list or seen_add(x))]


def replaceWithRandomPopulation(population, q, n, mn):
    for i in range(q):
        population.pop()
    for i in range(q):
        addRandomIndividual(population, n, mn)

def checkDiversity(population, diff, n, mn):
    if diff < 0.03:
        replaceWithRandomPopulation(population, int(n/3), n, mn)
    if diff < 0.05:
        replaceWithRandomPopulation(population, int(n/5), n, mn)
    elif diff < 0.1:
        replaceWithRandomPopulation(population, int(n/10), n, mn)

def getFitness(population):
    prev = population[0][1]
    total = 0
    diffPercentage = 0.0
    for ind in population:
        curr = ind[1]
        total += curr
        diffPercentage += (curr/float(prev)) - 1
        prev = curr

    return total, diffPercentage

#Each individual is compose by a permutation(list from 0 to the job_number*machine_number)
#And a second parameter that is filled with the result of the makespan for the permutation
#We keep track of the result to not calculate multiple times the same result unnecesarily
#Is important to remove that number every time the permutation change
def addRandomIndividual(population, n, mn):
    ind = list(range(n*mn))
    random.shuffle(ind)
    population.append([ind, None])


#We generate the number of population
def generate_population(number, n, mn):
        population = []
        for i in range(number):
            addRandomIndividual(population, n, mn)
        return population

#During the crossover we select gens from the father from the start to the end index defined, we remove those from the mother
#Then we add them to the resultant in the same order that it was in the father origininally
def crossover(father, mother, start_index, end_index):
    father_gen = father[0][start_index:end_index]
    fetus = removeFromList(mother[0], father_gen)
    result = []
    result.extend(fetus[:start_index])
    result.extend(father_gen)
    result.extend(fetus[start_index:])
    return [result, None]



#mutate one member of the poupulation randomly excluding the first one(best individual)
#We just change the order of the permutation by one
def mutation(population, mutation_rate):
    if(random.random() > mutation_rate):
        candidate = random.choice(population[1:])
        swap_rnd(candidate[0])
        candidate[1] = None

def evolve(population, mutation_rate):
    #Important: the population should be sorted before evolve

    #We delete the worst individual of the population
    population.pop()

    #we choose a mother and father for the new individual
    father = random.choice(population)
    mother = random.choice(population)
    while(mother == father):
        mother = random.choice(population)
    
    indexes = range(len(father[0]))

    #we select wich part of the father will go to the mother
    start_index = random.choice(indexes)
    end_index = random.choice(indexes[start_index:])

    #we generate the baby with the crossover
    baby = crossover(father, mother, start_index, end_index)

    #we add the new member to the population
    population.append(baby)

    #we trigger the mutation for one of the population, depending on the mutation rate
    mutation(population, mutation_rate)
    return population
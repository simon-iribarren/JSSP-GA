import random
from utils import swap_rnd

def removeFromList(parent, list):
    seen = set()
    seen_add = seen.add
    return [x for x in parent if not (x in list or seen_add(x))]

def generate_population(number, n, mn):
        population = []
        for i in range(number):
            addRandomInd(population, n, mn)
        return population

def crossover(father, mother, start_index, end_index):
    sperm = father[0][start_index:end_index]
    fetus = removeFromList(mother[0], sperm)
    result = []
    result.extend(fetus[:start_index])
    result.extend(sperm)
    result.extend(fetus[start_index:])
    return [result, None]

def single_mutation(population, mutation_rate):
    if(random.random() > mutation_rate):
        candidate = random.choice(population[1:])
        swap_rnd(candidate[0])
        candidate[1] = None
        
def mutation(population, mutation_rate):
    new_population = []
    for individual in population:
        if(random.random() > mutation_rate):
            new_individual = [swap_rnd(individual[0]), None]
            new_population.append(individual)
        else:
            new_population.append(individual)
    return new_population


def addRandomInd(population, n, mn):
    ind = range(n*mn)
    random.shuffle(ind)
    population.append([ind, None])


def addRandomPopulation(population, q, n, mn):
    for i in range(q):
        population.pop()
    for i in range(q):
        addRandomInd(population, n, mn)

def checkDiversity(population, diff, n, mn):
    if diff < 0.03:
        addRandomPopulation(population, n/3, n, mn)
    if diff < 0.05:
        addRandomPopulation(population, n/5, n, mn)
    elif diff < 0.1:
        addRandomPopulation(population, n/10, n, mn)

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

def evolve(population, mutation_rate):
    population.pop()

    father = random.choice(population)
    mother = random.choice(population)
    while(mother == father):
        mother = random.choice(population)
    
    indexes = range(len(father[0]))

    start_index = random.choice(indexes)
    end_index = random.choice(indexes[start_index:])

    baby = crossover(father, mother, start_index, end_index)

    population.append(baby)

    single_mutation(population, mutation_rate)
    return population
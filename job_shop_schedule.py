import random
import copy

def readFile(filepath):
    times_done = False
    times = []
    machines = []

    with open(filepath) as fp:
        line = fp.readline()
        while line:
            raw_line = line.strip().split(' ')
            curr = []
            for char in raw_line:
                if len(char) > 0:
                    curr.append(int(char))

            if len(curr) == 0:
                times_done = True
            else:
                if times_done:
                    machines.append(curr)
                else: 
                    times.append(curr)

            line = fp.readline()
    return times, machines, len(times)


def calculate_time(times, machines, config, n):
    time_table = []
    machine_number = len(machines[0])
    for i in range(machine_number):
        time_table.append([])

    current_times = [0]*n
    job_progress = [0]*n
    total_time = 0

    for j in config:
        job = j%n
        current_machine = machines[job][job_progress[job]] - 1 
        current_time = current_times[job]
        machine_usage = time_table[current_machine]
        usage_time = times[job][job_progress[job]]

        current_time, total_time = fillTimeSlot(machine_usage, current_time, usage_time, job, total_time)

        job_progress[job] += 1
        current_times[job] = current_time

    return total_time, time_table


def fillTimeSlot(machine_usage, current_time, usage_time, job, total_time):
    if len(machine_usage) > 0:
        prev = 0
        slot = None
        for used_slots in machine_usage:
            start = used_slots[0]
            end = used_slots[1]

            if start < current_time and current_time < end:
                current_time = end

            if prev == 0 and start > current_time + usage_time:
                slot = [current_time, usage_time + current_time, job]
                break
            elif start - prev >= usage_time and current_time <= prev:
                slot = [current_time, current_time + usage_time, job]
                break

            prev = end
            if end > current_time:
                current_time = end

        if slot == None:
            slot = [current_time, current_time + usage_time, job]

        current_time = slot[1]
        machine_usage.append(slot)
        machine_usage.sort(key=lambda x: x[1])

        if slot[1] > total_time:
            total_time = slot[1]

    else: 
        machine_usage.append([current_time, usage_time + current_time, job])
        current_time += usage_time;

    return current_time, total_time
        


def get_neightbor(config):
    list_cp = copy.copy(config)
    id1 = random.choice(range(len(config)))
    id2 = random.choice(range(len(config)))
    tmp = config[id1]
    list_cp[id1] = list_cp[id2]
    list_cp[id2] = tmp
    return list_cp

def swap_rnd(config):
    id1 = random.choice(range(len(config)))
    id2 = random.choice(range(len(config)))
    tmp = config[id1]
    config[id1] = config[id2]
    config[id2] = tmp
    return config


def removeFromList(parent, list):
    seen = set()
    seen_add = seen.add
    return [x for x in parent if not (x in list or seen_add(x))]

def generate_population(number, n, mn):
        population = []
        for i in range(number):
            ind = range(n*mn)
            random.shuffle(ind)
            population.append([ind, None])

        population.append(range(n*mn))
        return population

def crossover(father, mother, start_index, end_index):
    sperm = father[0][start_index:end_index]
    fetus = removeFromList(mother[0], sperm)
    result = [];
    result.extend(fetus[:start_index])
    result.extend(sperm)
    result.extend(fetus[start_index:])
    return [result, None]

def mutation(population, mutation_rate):
    new_population = []
    for individual in population:
        if(random.random() > mutation_rate):
            new_individual = [swap_rnd(individual[0]), None]
            new_population.append(individual)
        else:
            new_population.append(individual)
    return new_population

def genetic(times, machines, n, population_number, generations, rate):
    machine_number = len(machines[0])
    base_arr = range(n*machine_number)

    def bestIndividual(population, gen):
        best_individual = None
        best_result = None
        for individual in population:
            result = None
            if not individual[1]: 
                result, table = calculate_time(times, machines, individual, n)
                individual[1] = result
            else: 
                result = individual[1]

            if not best_result or result < best_result:
                best_result = result
                best_individual = individual

        population.sort(key=lambda x: x[1])
        return best_individual, best_result

    def evolve(population, mutation_rate, generation):
        new_population = []
        best_ind, best_result = bestIndividual(population, generation)

        for i, ind in enumerate(population):
            if(i == len(population) - 1):
                break
            start_index = random.choice(base_arr)
            end_index = random.choice(base_arr[start_index:])
            baby = crossover(ind, population[i+1], start_index, end_index)
            new_population.append(baby)

        new_population = mutation(new_population, mutation_rate)
        new_population.append(best_ind)
        return new_population

    population = generate_population(population_number, n, mn)
    result = None
    result_ind = None

    for i in range(generations):
        population = evolve(population, rate, i)
        best_ind, best_result = bestIndividual(population, i)
        if(not result or best_result < result):
            print("generation %s result %s" %(i, best_result))
            result = best_result
            result_ind = best_ind
    
    best_result, best_table = calculate_time(times, machines, best_ind, n)

    print("OVERALL RESULT")
    print("TABLE:")
    i = 1
    for row in best_table:
        print("M%s: %s" %(i, row))
        i += 1
    print("RESULT: %s" %best_result)        
    print("ORDER: %s" %result_ind) 
        


times, machines, n = readFile("15_15_0")

genetic(times, machines, n, 50, 5000, 0.2)



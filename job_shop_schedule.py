import random
import copy


def readFilePairs(filepath):
    times_done = False
    times = []
    machines = []

    with open(filepath) as fp:
        line = fp.readline()
        n, mn = line.strip().split(' ')
        line = fp.readline()

        while line:
            parse_line = ' '.join(line.split())
            raw_line = parse_line.strip().split(' ')
            curr = []
            i = 0
            machine = []
            time = []
            while i < len(raw_line):
                m, t = raw_line[i], raw_line[i + 1]
                machine.append(int(m))
                time.append(int(t))
                i += 2

            times.append(time)
            machines.append(machine)
            line = fp.readline()

    return times, machines, int(n)


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

def addRandomInd(population, n, mn):
    ind = range(n*mn)
    random.shuffle(ind)
    population.append([ind, None])

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

def genetic(times, machines, n, population_number, generations, rate):
    machine_number = len(machines[0])
    base_arr = range(n*machine_number)
    print(machines)
    print(times)

    def bestIndividual(population):
        best_individual = None
        best_result = None
        for individual in population:
            result = None
            if not individual[1]: 
                result, table = calculate_time(times, machines, individual[0], n)
                individual[1] = result
            else: 
                result = individual[1]

            if not best_result or result < best_result:
                best_result = result
                best_individual = individual

        population.sort(key=lambda x: x[1])
        return best_individual, best_result

    def evolve(population, mutation_rate):
        new_population = []
        result = bestIndividual(population)
        best_ind, best_result = result[0], result[1]

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

    def single_evolve(population, mutation_rate):
        result = bestIndividual(population)
        best_ind = result[0]
        population.pop()
        father = random.choice(population)
        mother = random.choice(population)
        start_index = random.choice(base_arr)
        end_index = random.choice(base_arr[start_index:])
        baby = crossover(father, mother, start_index, end_index)
        population.append(baby)
        single_mutation(population, mutation_rate)
        return population

    def getFitness(population):
        prev = population[0][1]
        total = 0
        diff = 0.0
        for ind in population:
            curr = ind[1]
            total += curr
            diff += (curr/float(prev)) - 1
            prev = curr

        return total, diff

    def addRandomPopulation(population, q):
        for i in range(q):
            population.pop()
        for i in range(q):
            addRandomInd(population, n, machine_number)
    
    def checkDiff(population, diff):
        total_fitness, diff = getFitness(population)
        if diff < 0.03:
            addRandomPopulation(population, n/3)
        if diff < 0.05:
            addRandomPopulation(population, n/5)
        elif diff < 0.1:
            addRandomPopulation(population, n/10)

    def find_best_local(population, generation, generation_diff, target):
        g = generation
        best_fitness = None
        best_result = None
        best_individual = None
        last_improve = g

        while(not best_result or best_result > 665 and g - last_improve < generation_diff):
            population = single_evolve(population, rate)
            r = bestIndividual(population)
            best_ind, resul_score = r[0], r[1]
            total_fitness, diff = getFitness(population)
            g += 1

            if(not best_result or best_result > resul_score):
                best_result = resul_score
                best_individual = copy.copy(best_ind)
                last_improve = g
                print("generation %s local result %s" %(g, best_result))


            if(not best_fitness or best_fitness > total_fitness):
                percentage = diff*100
                best_fitness = total_fitness
                #print("fitness: %s, diff: %s" %(best_fitness, percentage))
                last_improve = g
                
            checkDiff(population, diff)

        return best_result, best_individual, g

    def permutationToJobs(permutation):
        return map(lambda x: x%n, permutation[0])

    def tournament(target):
        best_found = None
        best_ind = None
        winners = [
            [[154, 256, 250, 51, 48, 276, 69, 31, 142, 173, 138, 81, 295, 63, 253, 191, 124, 222, 86, 184, 90, 181, 102, 214, 232, 223, 130, 264, 169, 144, 221, 219, 135, 248, 289, 178, 122, 174, 53, 67, 204, 74, 109, 238, 116, 263, 58, 43, 203, 266, 193, 114, 61, 228, 132, 141, 140, 286, 42, 60, 292, 188, 196, 246, 293, 161, 241, 104, 296, 244, 14, 32, 50, 30, 190, 56, 78, 158, 128, 195, 202, 4, 275, 66, 254, 201, 180, 99, 18, 168, 9, 76, 106, 52, 7, 247, 137, 108, 179, 294, 22, 40, 197, 261, 260, 194, 208, 107, 207, 231, 79, 187, 110, 209, 284, 6, 126, 83, 279, 118, 267, 150, 251, 1, 159, 133, 49, 176, 119, 20, 237, 82, 34, 143, 216, 28, 94, 139, 35, 131, 105, 288, 280, 54, 87, 162, 59, 257, 269, 84, 77, 113, 274, 186, 225, 220, 189, 23, 177, 217, 235, 239, 41, 215, 227, 287, 8, 262, 175, 285, 10, 100, 149, 62, 153, 234, 277, 166, 164, 75, 70, 243, 252, 147, 3, 19, 268, 297, 270, 265, 157, 73, 245, 171, 12, 111, 230, 299, 127, 226, 5, 47, 156, 212, 15, 71, 258, 185, 129, 192, 200, 183, 25, 255, 96, 27, 0, 242, 64, 146, 93, 281, 29, 199, 206, 88, 103, 24, 198, 72, 68, 213, 37, 65, 57, 163, 2, 46, 44, 172, 80, 148, 98, 283, 273, 182, 85, 170, 229, 165, 271, 152, 89, 136, 11, 155, 33, 36, 290, 125, 272, 134, 97, 278, 39, 95, 298, 211, 233, 218, 259, 38, 17, 167, 240, 45, 236, 101, 282, 117, 224, 160, 16, 26, 112, 151, 145, 205, 121, 249, 120, 21, 210, 115, 13, 291, 91, 55, 123, 92], 740]
        ]
        generations = 0
        rounds = 0
        while(not best_found or best_found >= target):
            rounds += 1
            print("ROUND: %s" %(rounds))
            if(len(winners) > 2):
                print("BEST CANDIDATES")
                pop = generate_population(population_number - len(winners), n, machine_number)
                pop.extend(winners)
                tr = find_best_local(pop, generations, 20000, target)
                br_local = tr[0]
                bi_local = tr[1]
                generations = tr[2]
                winners.sort(key=lambda x: x[1])
                winners = [bi_local]

                if not best_found or best_found > br_local:
                    best_found = br_local
                    best_ind = bi_local
                    print("BEST GLOBAL FOUND: %s - GENERATION: %s" %(br_local, generations))
                    print(permutationToJobs(bi_local))

                else:
                    print("BEST FOUND: %s - GENERATION: %s" %(br_local, generations))
                    print(permutationToJobs(bi_local))
            else: 
                random_population = generate_population(population_number, n, machine_number)
                tr = find_best_local(random_population, generations, 1500, target)
                br_local = tr[0]
                bi_local = tr[1]
                generations = tr[2]
                print("ROUND BEST: ", br_local)
                winners.append(bi_local)

                if not best_found or best_found > br_local:
                    best_found = br_local
                    best_ind = bi_local
                    print("BEST GLOBAL FOUND: %s - GENERATION: %s" %(br_local, generations))
                    print(permutationToJobs(bi_local))
                else:
                    print("BEST FOUND: %s - GENERATION: %s" %(br_local, generations))
                    print(permutationToJobs(bi_local))

        best_result, best_table = calculate_time(times, machines, best_ind[0], n)           
        print("OVERALL RESULT")
        print("TABLE:")
        i = 1
        for row in best_table:
            print("M%s: %s" %(i, row))
            i += 1
        print("RESULT: %s" %best_result)        
        print("ORDER: %s" %best_ind[0])

    tournament(665)
    """ population = generate_population(population_number, n, machine_number)
    generation = 0
    best_fitness = None

    global_best = None
    global_best_ind = None

    while(not global_best or global_best > 665):
        population = single_evolve(population, rate)
        r = bestIndividual(population)
        best_ind, best_result = r[0], r[1]
        total_fitness, diff = getFitness(population)
        generation += 1

        if(not global_best or best_result < global_best):
            print("generation %s global result %s" %(generation, best_result))
            global_best = best_result
            global_best_ind = copy.copy(best_ind)

        if(not best_fitness or best_fitness > total_fitness):
            percentage = diff*100
            best_fitness = total_fitness
            
        checkDiff(population, diff)

    for i in range(generations):
        population = single_evolve(population, rate)
        r = bestIndividual(population)
        best_ind, best_result = r[0], r[1]
        if(not global_best or best_result < global_best):
            print("generation %s result %s" %(generation, best_result))
            global_best = best_result
            global_best_ind = best_ind
    
    best_result, best_table = calculate_time(times, machines, best_ind[0], n)           
    print("OVERALL RESULT")
    print("TABLE:")
    i = 1
    for row in best_table:
        print("M%s: %s" %(i, row))
        i += 1
    print("RESULT: %s" %best_result)                 
    print("ORDER: %s" %best_ind[0]) """
times, machines, n = readFilePairs("test5")
genetic(times, machines, n, 30, 50000, 0.15)



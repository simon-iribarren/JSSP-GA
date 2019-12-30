import random
import copy


def readFileDiff(filepath):
    times_done = False
    times = []
    machines = []

    with open(filepath) as fp:
        line = fp.readline()
        while line:
            raw_line = line.strip().split('  ')
            curr_time = []
            curr_machine = []
            time = False
            for pair in raw_line:
                machine, time = pair.split(' ')
                curr_time.append(int(time))
                curr_machine.append(int(machine))
    
            times.append(curr_time)
            machines.append(curr_machine)

            line = fp.readline()
    return times, machines, len(times)

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

def calculate_total_time(times, machines, config, n):
    USED = []
    for i in range(len(machines[0])):
        USED.append([])
    
    total_time = 0
    for i in range(n):
        job = config[i]
        job_times = times[job]
        job_machines = machines[job]
        current_time = 0
        for j in range(len(job_machines)):
            current_machine = job_machines[j] - 1
            usage_time = job_times[j]
            machine_usage = USED[current_machine]
            current_time, total_time = fillTimeSlot(machine_usage, current_time, usage_time, job, total_time)

    return total_time, USED

def calculate_time(times, machines, config, n):
    time_table = []
    for i in range(len(machines[0])):
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

from itertools import permutations 

def brute_force(times, machines, n):
    configuration = [10, 13, 12, 11, 11, 9, 8, 7, 7, 5, 4, 3, 2, 1, 0, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 13, 12, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 14, 13, 12, 11, 14, 9, 8, 7, 6, 5, 4, 3, 11, 1, 0, 14, 13, 12, 11, 10, 9, 8, 7, 6, 10, 4, 3, 2, 9, 0, 14, 13, 12, 11, 10, 9, 8, 6, 5, 5, 4, 3, 12, 5, 0, 3, 13, 12, 11, 10, 9, 8, 7, 1, 5, 4, 3, 0, 8, 0, 14, 13, 12, 11, 10, 9, 8, 7, 5, 6, 4, 3, 2, 1, 2, 6, 13, 1, 5, 10, 9, 1, 3, 6, 5, 4, 3, 2, 12, 0, 14, 13, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 14, 13, 12, 11, 10, 1, 8, 7, 6, 5, 4, 3, 2, 1, 0, 14, 13, 12, 11, 10, 9, 8, 14, 7, 1, 4, 14, 2, 6, 0, 14, 14, 2, 11, 10, 9, 8, 7, 6, 4, 4, 7, 2, 1, 0, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 6, 3, 2, 1, 0, 14, 13, 12, 2, 10, 9, 8, 7, 6, 4, 5, 3, 2, 1, 0]
    best_result, best_table = calculate_total_time(times, machines, configuration, n)

    for cfg in permutations(configuration, len(configuration)):
        result, table = calculate_time(times, machines, cfg, n)
        if result < best_result: 
            best_result = result
            best_table = table
            best_config = copy.copy(configuration)
            print(best_result)
    
    print("TABLE:")
    i = 1
    for row in best_table:
        print("M%s: %s" %(i, row))
        i += 1

    print("RESULT: %s" %best_result)
    print("ORDER: %s" %best_config)     
      


def local_search(times, machines, n):
    configuration = range(n*n)
    best_result, best_table = calculate_total_time(times, machines, configuration, n)
    best_config = copy.copy(configuration)
    
    print("####Init sequencial config ####" )  

    for i in range(100000):
        cfg = get_neightbor(configuration)
        result, table = calculate_time(times, machines, cfg, n)
        if result < best_result: 
            configuration = cfg
            best_result = result
            best_table = table
            best_config = copy.copy(configuration)
            print(best_result)

    print("SEQUENTIAL BEST: %s" %best_result)        

    configuration = range(n)*n
    configuration = configuration[::-1]
    print("####Init reverse config ####" )
    reverse_best = 1000000
    cfg = configuration
    for i in range(100000):
        result, table = calculate_time(times, machines, cfg, n)
        if result < reverse_best: 
            configuration = cfg
            reverse_best = result
            if reverse_best < best_result:
                best_result = reverse_best
                best_table = table
                best_config = copy.copy(configuration)
                print(best_result)
        cfg = get_neightbor(configuration)

    print("REVERSE BEST: %s" %reverse_best)        

    
    random.shuffle(configuration)
    
    best_random = 1000000
    cfg = configuration

    print("####Init random config ####" )
    for i in range(10000):
        result, table = calculate_time(times, machines, cfg, n)
        if(result < best_random):
            configuration = cfg
            best_random = result
            if best_random < best_result:
                best_result = best_random
                best_table = table
                best_config = copy.copy(configuration)
                print(best_result)
        cfg = get_neightbor(configuration)

    print("RANDOM BEST: %s" %best_random)        

    print("OVERALL RESULT")
    print("TABLE:")
    i = 1
    for row in best_table:
        print("M%s: %s" %(i, row))
        i += 1

    print("RESULT: %s" %best_result)        
    print("ORDER: %s" %best_config)     
   
times, machines, n = readFile("test")
brute_force(times, machines, n)
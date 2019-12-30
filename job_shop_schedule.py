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

            if len(machine_usage) > 0:
                prev = 0
                slot = None
                for start, end in machine_usage:
                    if start < current_time and current_time < end:
                        current_time = end

                    if prev == 0 and start > current_time + usage_time:
                        slot = [current_time, usage_time + current_time]
                        break
                    elif start - prev >= usage_time and current_time <= prev:
                        slot = [current_time, current_time + usage_time]
                        break

                    prev = end
                    if end > current_time:
                        current_time = end

                if slot == None:
                    slot = [current_time, current_time + usage_time]

                current_time = slot[1]
                machine_usage.append(slot)
                machine_usage.sort(key=lambda x: x[1])

                if slot[1] > total_time:
                    total_time = slot[1]
            else: 
                machine_usage.append([current_time, usage_time + current_time])
                current_time += usage_time;
    return total_time, USED

def get_neightbor(config):
    list_cp = copy.copy(config)
    id1 = random.choice(range(len(config)))
    id2 = random.choice(range(len(config)))
    tmp = config[id1]
    list_cp[id1] = list_cp[id2]
    list_cp[id2] = tmp
    return list_cp


def local_search(times, machines, n):
    configuration = range(n)
    best_result, best_table = calculate_total_time(times, machines, configuration, n)
    best_config = copy.copy(configuration)
    
    for i in range(10000):
        cfg = get_neightbor(configuration)
        result, table = calculate_total_time(times, machines, cfg, n)
        if result < best_result: 
            configuration = cfg
            best_result = result
            best_table = table
            best_config = copy.copy(configuration)
            print(best_result)

    configuration = configuration[::-1]

    for i in range(10000):
        cfg = get_neightbor(configuration)
        result, table = calculate_total_time(times, machines, cfg, n)
        if result < best_result: 
            configuration = cfg
            best_result = result
            best_table = table
            best_config = copy.copy(configuration)
            print(best_result)

    for i in range(10000):
        random.shuffle(configuration)
        result, table = calculate_total_time(times, machines, configuration, n)
        if result < best_result: 
            best_result = result
            best_table = table
            best_config = copy.copy(configuration)
            print(best_result)

    print("RESULT: %s" %best_result)        
    print("ORDER: %s" %best_config)     
   
times, machines, n = readFileDiff("test")
local_search(times, machines, n)
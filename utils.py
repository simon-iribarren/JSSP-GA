
import random
from calculateMakespan import calculateMakespan

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

def readSolution(filepath):
    machines = []

    with open(filepath) as fp:

        line = fp.readline()
        while line:
            raw_line = line.strip().split(' ')
            curr = []
            for char in raw_line:
                if len(char) > 0:
                    curr.append(int(char))
            machines.append(curr)
            line = fp.readline()
    sequence = []
    for i in range(len(machines[0])):
        for j in range(len(machines)):
            sequence.append(machines[j][i])
    return sequence

def swap_rnd(config):
    id1 = random.choice(range(len(config)))
    id2 = random.choice(range(len(config)))
    tmp = config[id1]
    config[id1] = config[id2]
    config[id2] = tmp
    return config

def fromPermutation(permutation, n):
    return list(map(lambda  x: x%n, permutation))
    

def testPermutation(permutation, times, machines, n):
    best_result, table = calculateMakespan(times, machines, permutation, n)
    print("SEQUENCE")
    print(permutation)
    print("RESULT:")
    print(best_result)
    job_sequence = []
    print("TABLE:")
    i = 1
    for row in table:
        print("M%s: %s" %(i, row))
        for slot in row:
            job_sequence.append(slot[2])
        i += 1
    print(job_sequence)

def printTable(table):
    i = 1
    print("TABLE: ")
    for row in table:
        print("M%s: %s" %(i, row))
        i += 1
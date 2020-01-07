import copy
import random

def calculateMakespan(times, machines, config, n):
    time_table = []
    times = copy.deepcopy(times)
    machines = copy.deepcopy(machines)
    mn = len(machines[0])
    for i in range(mn):
        time_table.append([])

    current_times = [0]*n
    total_time = 0
    for j in config:
        job = j%n
        current_machine = machines[job].pop(0)
        current_time = current_times[job]
        machine_usage = time_table[current_machine]
        usage_time = times[job].pop(0)
        current_time, total_time = fillTimeSlot(machine_usage, current_time, usage_time, job, total_time)

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
        current_time += usage_time

    return current_time, total_time
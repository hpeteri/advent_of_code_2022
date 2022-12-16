# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("input.txt", "r") as f:
    lines = f.read().splitlines()
    f.close()

class Valve:
    def __init__(this, name, flow_rate):
        this.name        = name
        this.flow_rate   = int(flow_rate)
        this.connections = []
        this.distance_to = {}
    def __str__(this):
        return f"valve: '{this.name}' | {this.flow_rate} -> {this.connections}"
        
valves = {}
for line in lines:
    l = line.split(";")
    valve_name = l[0].split(" ")[1]
    flow_rate = l[0].split("=")[1]

    connections = l[1].split(" ")[5:]
    valve = Valve(valve_name, flow_rate)

    for connection in connections:
        valve.connections.append(connection[:2])

    valves[valve_name] = valve


def calculate_shortest_distance(path, to):
    valve = valves[path[-1]]
    
    if valve.name == to:
        return len(path) - 1

    shortest_distance = len(valves)
    for connection in valve.connections:
        try:
            path.index(connection)
        except:
            p = path[:]
            p.append(connection)
            distance = calculate_shortest_distance(p, to)
            shortest_distance = min(distance, shortest_distance)

    return shortest_distance

working_valves = []
for key in valves:
    valve = valves[key]
    if valve.flow_rate != 0:
        working_valves.append(key)
    
    for k in valves:
        d = calculate_shortest_distance([key], k)
        valve.distance_to[k] = d


def check_paths(at, score, path, working_valves, time_left):
    valve = valves[at]
    if time_left <= 0:
        return [score, path]

    if len(working_valves) == 0:
        return [score, path]
    
    best_score = 0
    best_path = []
    for idx, other in enumerate(working_valves):
        valve_0 = valves[other]
        d = valve.distance_to[other]

        other_score = score
        other_time_left = time_left - (d + 1)
        
        if other_time_left > 0:
            other_score += other_time_left * valve_0.flow_rate
            
        new_working_valves = working_valves[:idx]
        new_working_valves.extend(working_valves[idx + 1:])

        other_path = path[:]
        other_path.append(other)
        
        sp = check_paths(other, other_score, other_path, new_working_valves, other_time_left)

        if sp[0] > best_score:
            
            best_score = sp[0]
            best_path  = sp[1][:]

    return [best_score, best_path]
        
        

# part 1
best_score_path = check_paths("AA", 0, [], working_valves[:], 30)
best_score = best_score_path[0]
best_path = best_score_path[1]
print(f"best score: {best_score}")
print(best_path)


def get_permutations(src_set, dst_set, wanted_len, res):
    if len(dst_set) == wanted_len:
        res.append([dst_set[:]])
        return res
    
    for i in range(len(src_set)):

        d = dst_set[:]
        d.append(src_set[i])
        
        s = src_set[i + 1:]

        res = get_permutations(s, d, wanted_len, res)

    return res

# part 2
best_total_score = 0
best_paths = []
print(f"tasks : {len(working_valves)}")
for split_idx in range(int(len(working_valves) / 2) + 1):

    elf_task_count = len(working_valves) - split_idx
    elephant_task_count = split_idx
    
    elf_tasks      = get_permutations(working_valves[:], [], elf_task_count, [])
    elephant_tasks = []

    for perms in elf_tasks:

        e_perms = []
        for vs in perms:
            e_tasks = working_valves[:]
            for v in vs:
                try:
                    e_tasks.remove(v)
                except e:
                    print(e)
                
            e_perms.append(e_tasks)

        elephant_tasks.append(e_perms)


    for i in range(len(elf_tasks)):
        elf_score  = check_paths("AA", 0, [], elf_tasks[i][0], 26)
        elephant_score = check_paths("AA", 0, [], elephant_tasks[i][0], 26)
        
        total = elf_score[0] + elephant_score[0]
        if total > best_total_score:
            best_total_score = total
            best_paths = [elf_score[1], elephant_score[1]]

print(f"best total: {best_total_score}")
print(best_paths[0])
print(best_paths[1])

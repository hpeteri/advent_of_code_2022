# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

import sys

from copy import copy
from math import ceil

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if len(sys.argv) < 2:
    print("pass file name as argument")
    sys.exit()

    
with open(sys.argv[1], "r") as f:
    lines_0 = f.read().replace("\n", " ")
    lines_1 = lines_0.split(".")
    lines = []
    for line in lines_1:
        lines.extend(line.split(":"))

for idx, line in enumerate(lines):
    lines[idx] = line.strip()

class SimulationContext:
    def __init__(this, costs):
        this.resources  = [0,0,0,0]
        this.robots     = [1,0,0,0]
        this.minute     = 0
        #this.target     = 24
        this.target     = 32
        this.costs      = costs
        this.max_robots = [0,0,0,99]
        for robot_cost in costs:
            for ci, cost in enumerate(robot_cost):
                this.max_robots[ci] = max(this.max_robots[ci], cost)
    def create_copy(this):
        cp =  SimulationContext(this.costs)

        cp.resources = this.resources[:]
        cp.robots    = this.robots[:]
        cp.minute    = this.minute
        return cp
    
    def __str__(this):
        s = ""

        return s
    
    def time_for_robot(this, robot_idx):
        costs = this.costs[robot_idx]
        for ci, cost in enumerate(costs):
            if not cost:
                continue
            
            if this.robots[ci] == 0:
                return -1

        if this.robots[robot_idx] == this.max_robots[robot_idx]:
            return -1
        
        max_time = 0
        for ci, cost in enumerate(costs):
            if cost:
                if cost <= this.resources[ci]:
                    pass
                else:
                    max_time = max(max_time, ceil((cost - this.resources[ci]) / (this.robots[ci])))

        return max_time

    def make_robot(this, robot_idx):        
        for ci, cost in enumerate(this.costs[robot_idx]):
            this.resources[ci] -= cost
                
    def simulate_for(this, minutes):
        result = True
        
        if this.minute + minutes > this.target - 1:
            minutes  = this.target - 1 - this.minute
            result   = False
        
        this.minute += minutes

        
        for idx, robot in enumerate(this.robots):
            this.resources[idx] += robot * minutes

        return result

def factorial(x):
    result = 0
    while x >= 0:
        result += x
        x -= 1

    return result

def simulate(sim, simulations_to_do, best_result):
    if sim.minute == sim.target - 1:
        for i, robot in enumerate(sim.robots):
            sim.resources[i] += robot
        
        return
    if sim.minute > sim.target - 1:
        print("this should not happen")
        print(sim.minute)
        return
    
    for i in range(4):
        time_for_n_robot = sim.time_for_robot(i)
        if time_for_n_robot >= 0:
            sim_0 = sim.create_copy()
                        
            if time_for_n_robot == 0:
                sim_0.make_robot(i)
                sim_0.simulate_for(1)
                sim_0.robots[i] += 1
                
            else:
                sim_0.simulate_for(time_for_n_robot)
                
            if best_result:
                
                time_left = sim.target - sim_0.minute

                g0 = factorial(sim_0.robots[3])
                g1 = factorial(time_left)

                if sim_0.resources[3] + g0 + g1 < best_result.resources[3]:
                    return
                                
            simulations_to_do.append(sim_0)
            
        
blueprint = None
line_idx = 0
blueprint_results = []
for line in lines:    
    if line[0: 9] == "Blueprint" or len(line) == 0:
        if blueprint != None:
            print("do blueprint: ", blueprint)
            simulations_to_do = [SimulationContext(blueprint)]
            tries = 0

            best_score = 0
            blueprint_results.append(None)
            while len(simulations_to_do):
                
                tries += 1
                sim = simulations_to_do.pop()
                simulate(sim, simulations_to_do, blueprint_results[-1])
                if sim.resources[3] > best_score:
                    best_score = sim.resources[3]
                    blueprint_results[-1] = sim
                    print(f"new best: {best_score} (with {tries} tries)")

            print(f"did {tries} simulations")
            
        blueprint = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        line_idx  = 0

        if len(blueprint_results) == 3:
            break
        
        continue

    if line_idx == 0:
        cost            = int(line.split(" ")[4])
        blueprint[0][0] = cost
        
    elif line_idx == 1:
        cost            = int(line.split(" ")[4])
        blueprint[1][0] = cost
        
    elif line_idx == 2:
        ore_cost                = int(line.split(" ")[4])
        clay_cost               = int(line.split(" ")[7])
        blueprint[2][0] = ore_cost
        blueprint[2][1] = clay_cost
        
    elif line_idx == 3:
        ore_cost             = int(line.split(" ")[4])
        obsidian_cost        = int(line.split(" ")[7])
        blueprint[3][0] = ore_cost
        blueprint[3][2] = obsidian_cost
            
    line_idx += 1

score = 0
for idx, result in enumerate(blueprint_results):
    if result:
        print(result.resources[3])
        score += (idx + 1) * result.resources[3]

print(f"score: {score}")

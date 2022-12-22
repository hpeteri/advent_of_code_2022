# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

import sys
from copy import copy

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


class Blueprint:
    def __init__(this):
        this.ore_cost      = 0
        this.clay_cost     = 0
        this.obsidian_cost = []
        this.geode_cost    = []

    def __str__(this):
        return f"\nore: {this.ore_cost}\nclay: {this.clay_cost}\nobsidian: {this.obsidian_cost}\ngeode: {this.geode_cost}"


class SimulationContext:
    def __init__(this, blueprint):
        this.ore_bot_count                  = 1
        this.clay_bot_count                 = 0
        this.obsidian_bot_count             = 0
        this.geode_bot_count                = 0
        this.constructed_ore_bot_count      = 0
        this.constructed_clay_bot_count     = 0
        this.constructed_obsidian_bot_count = 0
        this.constructed_geode_bot_count    = 0
        this.ore_count                      = 0
        this.clay_count                     = 0
        this.obsidian_count                 = 0
        this.geode_count                    = 0
        this.rnd                            = 0
        this.max_ore_bot_count              = max(blueprint.ore_cost, max(blueprint.clay_cost, max(blueprint.obsidian_cost[0] ,blueprint.geode_cost[0])))
        this.max_clay_bot_count             = blueprint.obsidian_cost[1]
        this.max_obsidian_bot_count         = blueprint.geode_cost[1]
        #this.history                        = ""
                
    def print_history(this):
        pass
        #print("HISTORY")
        #print(this.history)
        
    def update(this):
        this.ore_count      += this.ore_bot_count
        this.clay_count     += this.clay_bot_count
        this.obsidian_count += this.obsidian_bot_count
        this.geode_count    += this.geode_bot_count
        #this.history        += this.get_status()
  

    def next_round(this):
        this.rnd += 1
        
        this.ore_bot_count      += this.constructed_ore_bot_count;
        this.clay_bot_count     += this.constructed_clay_bot_count;
        this.obsidian_bot_count += this.constructed_obsidian_bot_count;
        this.geode_bot_count    += this.constructed_geode_bot_count;

        this.constructed_ore_bot_count      = 0;        
        this.constructed_clay_bot_count     = 0;       
        this.constructed_obsidian_bot_count = 0;   
        this.constructed_geode_bot_count    = 0;
        
        #this.history += f"\n=== minute {this.rnd} ===\n"
        
    def get_status(this):
        
        s  = f"{this.ore_bot_count} / {this.max_ore_bot_count} ore robots collects ore. you now have {this.ore_count} ore.\n"
        s += f"{this.clay_bot_count} / {this.max_clay_bot_count} clay robots collects clay. you now have {this.clay_count} clay.\n"
        s += f"{this.obsidian_bot_count} / {this.max_obsidian_bot_count}  obsidian robots collects obsidian. you now have {this.obsidian_count} obsidian.\n"
        s += f"{this.geode_bot_count} geode robots collects geodes. you now have {this.geode_count} geodes.\n"

        return s
        
    def make_ore_robot(this, blueprint):
        if this.ore_count < blueprint.ore_cost:
            return 0

        if this.ore_bot_count >= this.max_ore_bot_count:
            return 2
        
        this.ore_count     -= blueprint.ore_cost
        this.constructed_ore_bot_count = 1
        #this.history += "make ore bot\n"
        return 1
    
    def make_clay_robot(this, blueprint):
        if this.ore_count < blueprint.clay_cost:
            return 0

        if this.clay_bot_count >= this.max_clay_bot_count:
            return 2
        
        this.ore_count -= blueprint.clay_cost
        this.constructed_clay_bot_count = 1
        #this.history += "make clay bot\n"
        return 1

    def make_obsidian_robot(this, blueprint):
        if this.ore_count < blueprint.obsidian_cost[0]:
            return 0

        if this.clay_count < blueprint.obsidian_cost[1]:
            return 0

        if this.obsidian_bot_count >= this.max_obsidian_bot_count:
            return 2
        
        this.ore_count -= blueprint.obsidian_cost[0]
        this.clay_count -= blueprint.obsidian_cost[1]
        this.constructed_obsidian_bot_count = 1
        #this.history += "make obsidian bot\n"
        return 1

    
    def make_geode_robot(this, blueprint):
        if this.ore_count < blueprint.geode_cost[0]:
            return 0
        if this.obsidian_count < blueprint.geode_cost[1]:
            return 0

        this.ore_count      -= blueprint.geode_cost[0]
        this.obsidian_count -= blueprint.geode_cost[1]
        this.constructed_geode_bot_count = 1
        #this.history += "make geode bot\n"
        return 1
        
max_geodes_opened = 0
def sim_blueprint(blueprint, sim, simulations_to_do):
    target_rnd = 24
    while sim.rnd < target_rnd:
        sim.next_round()
        
        #ore
        sim_0 = copy(sim)
        a = sim_0.make_ore_robot(blueprint)
        if a == 1:
            sim_0.update()
            simulations_to_do.append(sim_0)

        #clay
        sim_1 = copy(sim)
        b = sim_1.make_clay_robot(blueprint)
        if b == 1:
            sim_1.update()
            simulations_to_do.append(sim_1)

        #obisian
        sim_2 = copy(sim)
        c = sim_2.make_obsidian_robot(blueprint)
        if c == 1:
            sim_2.update()
            simulations_to_do.append(sim_2)

        #geode
        sim_3 = copy(sim)
        d = sim_3.make_geode_robot(blueprint)
        if d == 1:
            sim_3.update()
            simulations_to_do.append(sim_3)

        sim.update()

        # if we can do all options, no point of waiting a round...
        if (a == 1) and (b == 1) and (c == 1) and (d == 1):
            break

        # case when we dont construct new robots and instead wait for resources
        
        if b and (sim.clay_bot_count == 0):
            break

        if c and (sim.obsidian_bot_count == 0):
            break
        
        if d and (sim.geode_bot_count == 0):
            break
        
    if not sim.rnd < target_rnd:
        global max_geodes_opened
        if sim.geode_count > max_geodes_opened.geode_count:
            max_geodes_opened = sim
            print(sim.geode_count)
                
blueprint = None
line_idx = 0
geode_count = []
for line in lines:
    if line[0: 9] == "Blueprint" or len(line) == 0:
        if blueprint != None:
            print()
            print("do blueprint: ", blueprint)
            simulations_to_do = [SimulationContext(blueprint)]
            tries = 0
            max_geodes_opened = SimulationContext(blueprint)
            while len(simulations_to_do):
                tries += 1
                sim = simulations_to_do.pop()
                sim_blueprint(blueprint, sim, simulations_to_do)

            print(f"did {tries} simulations")
            max_geodes_opened.print_history()
            geode_count.append(max_geodes_opened)
                            
        blueprint = Blueprint()
        line_idx = 0
        continue

    print(line)
    if line_idx == 0:
        cost               = int(line.split(" ")[4])
        blueprint.ore_cost = cost
        
    elif line_idx == 1:
        cost                = int(line.split(" ")[4])
        blueprint.clay_cost = cost
        
    elif line_idx == 2:
        ore_cost                = int(line.split(" ")[4])
        clay_cost               = int(line.split(" ")[7])
        blueprint.obsidian_cost = [ore_cost, clay_cost]
        
    elif line_idx == 3:
        ore_cost             = int(line.split(" ")[4])
        obsidian_cost        = int(line.split(" ")[7])
        blueprint.geode_cost = [ore_cost, obsidian_cost]
    else:
        print(f"???: {line_idx}")
    
    line_idx += 1


total = 0
for idx, a in enumerate(geode_count):
    print(a.geode_count)
    total += (idx + 1) * a.geode_count

print(f"score: {total}")

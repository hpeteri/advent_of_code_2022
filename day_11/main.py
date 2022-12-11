# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

f = open("input.txt", "r")
lines = f.read().splitlines()
f.close()

import operator

monkeys = []

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

for line in lines:
    line = line.lstrip().split(' ')
    if len(line) == 1:
        continue
    
    if line[0] == "Monkey":
        monkey = {}
        
        monkey["items"]      = []
        monkey["test_value"] = -1
        monkey["op_code"]    = ["", None, ""] 
        
        monkey["test_true"]  = None
        monkey["test_false"] = None
        monkey["inspection_count"] = 0
        
        monkeys.append(monkey)

    elif line[0] == "Starting":
        for i in range(2, len(line)):
            monkeys[-1]["items"].append(int(line[i].strip(',')))

    elif line[0] == "Operation:":
        monkeys[-1]["op_code"][0] = line[3]
        monkeys[-1]["op_code"][1] = line[4]
        monkeys[-1]["op_code"][2] = line[5]
        
    elif line[0] == "If" and line[1] == "true:":
        monkeys[-1]["test_true"] = int(line[5])

    elif line[0] == "If" and line[1] == "false:":
        monkeys[-1]["test_false"] = int(line[5])
    elif line[0] == "Test:":
        monkeys[-1]["test_value"] = int(line[3])

rnd = 1;

common_denom = 1
for monkey in monkeys:
    common_denom *= monkey["test_value"]

for i in range(10000):
    for (monkey_idx, monkey) in enumerate(monkeys):
        
        divider = monkey["test_value"]
        op = monkey["op_code"][1]
        for item in monkey["items"]:
            monkey["inspection_count"] += 1
            old = item
            new = eval("".join(monkey["op_code"]))

            new = new % common_denom
            
            if (new % divider) == 0:
                #t = monkeys[monkey["test_true"]]["test_value"]
                #new = (divider * t) + (new % t)
                
                monkeys[monkey["test_true"]]["items"].append(new)

            else:
                #t = monkeys[monkey["test_false"]]["test_value"]
                #new = (t + (new % t)) * (divider + (new % divider))
                
                monkeys[monkey["test_false"]]["items"].append(new)
                
        monkey["items"] = []

    rnd += 1

inspections = []

for monkey in monkeys:
    inspections.append(monkey["inspection_count"])

inspections.sort(reverse=True)

monkey_business = inspections[0] * inspections[1]
print("monkey business: ", monkey_business)

# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

import sys

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if len(sys.argv) < 2:
    print("pass filename as argument")
    sys.exit()

# read lines
try:
    with open(sys.argv[1], "r") as f:
        lines = f.read().splitlines()
        f.close()
except:
    print(f"failed to open file: '{sys.argv[1]}'")
    sys.exit()


grid = []
grid_is_ready = False

instructions = []

grid_width = 0
grid_height = 0
for line in lines:
    if not grid_is_ready:
        a = [c for c in line]
        grid_width = max(grid_width, len(line))
        
        if len(a) == 0:
            print(f"grid is ready '{line}'")
            grid_is_ready = True
            continue
                    
        grid.append(a)
        
    else:
        
        is_digit = line[0].isdigit()
        instruction = line[0]
        for idx, c in enumerate(line[1:]):
            if is_digit:
                if c.isdigit():
                    instruction += c
                else:
                    instructions.append(instruction)
                    is_digit = False
                    instruction = ""
                    instructions.append(c)
            else:
                if not c.isdigit():
                    instructions.append(instruction)
                    instruction = ""
                    instructions.append(c)
                else:
                    is_digit = True
                    instruction = c

        instructions.append(instruction)

grid_height = len(grid)
for idx, row in enumerate(grid):
    while len(row) < grid_width:
        row.append(" ")
        
        
p0_xy = [grid[0].index('.'), 0]

facing_idx = 0
facings = [[1, 0], [0, 1], [-1, 0], [0, -1]]


print(p0_xy)

for instruction in instructions:
    facing_xy = facings[facing_idx]
    print(f"facing is now: {facing_xy}")
    if instruction.isdigit():
        print(f"go forward {instruction}")

        for i in range(int(instruction)):
            n = p0_xy
            while 1:
                n = [(n[0] + facing_xy[0]) % grid_width, (n[1] + facing_xy[1]) % grid_height]
                s = grid[n[1]][n[0]]
                if s == ' ':
                    continue
                
                break
            s = grid[n[1]][n[0]]
            
            if s == '#':
                break
            elif s == ".":
                p0_xy = n
                print(n)
            else:
                print(f"symbol is '{s}'")
                sys.exit()
                            
        print(f"at: {p0_xy}")
            

    else:
        print(instruction)
        if instruction == 'R':
            facing_idx = (facing_idx + 1) % 4
        else:
            facing_idx = (facing_idx + 3) % 4

print(f"pos xy: {p0_xy}")
print(f"facing: {facing_idx}")
print(f"score: {(1000 * (p0_xy[1] + 1)) + (4 * (p0_xy[0] + 1)) + (facing_idx)}")

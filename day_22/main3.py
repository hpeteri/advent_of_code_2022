# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

import sys

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# read lines
try:
    with open("input.txt", "r") as f:
        lines = f.read().splitlines()
        f.close()
except:
    print(f"failed to open file: 'input.txt")
    sys.exit()

cube_diameter = 50    
grid = []
grid_is_ready = False

instructions = []

for line in lines:
    if not grid_is_ready:
        a = [c for c in line]
                
        if len(a) == 0:
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

        

cube_map = [[], [], [], [], [], []]

print(cube_diameter)

for i in range(cube_diameter):

    # 0
    cube_map[0].append(grid[i][cube_diameter: cube_diameter * 2])
    # 1
    cube_map[1].append(grid[i][cube_diameter * 2: cube_diameter * 3])

    
    # 2
    cube_map[2].append(grid[cube_diameter + i][cube_diameter: cube_diameter * 2])

    
    # 3
    cube_map[3].append(grid[cube_diameter * 2 + i][:cube_diameter])
    # 4
    cube_map[4].append(grid[cube_diameter * 2 + i][cube_diameter: cube_diameter * 2])    

    
    # 5
    cube_map[5].append(grid[cube_diameter * 3 + i][:cube_diameter])    

for i in range(6):
    print()
    print(f"=== side: {i} ===")
    print()
    for row in cube_map[i]:
        print("".join(row))

facings = [[1, 0], [0, 1], [-1, 0], [0, -1]]

# side, facing, x, y
p0_sfxy = [0, 0, 0, 0]

for instruction in instructions:
    
    #print()
    #print(f"facing is now: {facing_xy}")

    if instruction.isdigit():
        #print(f"go forward {instruction}")
        for i in range(int(instruction)):
            x          = p0_sfxy[2]
            y          = p0_sfxy[3]
            side_idx   = p0_sfxy[0]
            facing_idx = p0_sfxy[1]

            side      = cube_map[p0_sfxy[0]]
            facing_xy = facings[p0_sfxy[1]]
    
            while 1:
                x = (x + facing_xy[0])
                y = (y + facing_xy[1])

                if x  == cube_diameter:
                    if side_idx == 0:
                        side_idx   = 1
                        x          = 0
                    elif side_idx == 1:
                        side_idx   = 4
                        facing_idx = 2
                        x          = cube_diameter -1
                        y          = cube_diameter - y - 1
                    elif side_idx == 2:
                        side_idx   = 1
                        facing_idx = 3
                        x          = y
                        y          = cube_diameter - 1
                    elif side_idx == 3:
                        side_idx   = 4
                        x          = 0                        
                    elif side_idx == 4:
                        side_idx   = 1
                        facing_idx = 2
                        x          = cube_diameter -1
                        y          = cube_diameter - y - 1
                    elif side_idx == 5:
                        side_idx   = 4
                        facing_idx = 3
                        x          = y
                        y          = cube_diameter - 1
                elif x < 0:
                    if side_idx == 0:
                        side_idx   = 3
                        facing_idx = 0
                        x          = 0
                        y          = cube_diameter - y - 1
                    elif side_idx == 1:
                        side_idx   = 0
                        x          = cube_diameter - 1
                    elif side_idx == 2:
                        side_idx   = 3
                        facing_idx = 1
                        x          = y
                        y          = 0                        
                    elif side_idx == 3:
                        side_idx   = 0
                        facing_idx = 0
                        x          = 0
                        y          = cube_diameter - y - 1
                    elif side_idx == 4:
                        side_idx   = 3
                        x          = cube_diameter - 1
                    elif side_idx == 5:
                        side_idx   = 0
                        facing_idx = 1
                        x          = y
                        y          = 0

                if y < 0:
                    if side_idx == 0:
                        side_idx   = 5
                        facing_idx = 0
                        y          = x
                        x          = 0
                    elif side_idx == 1:
                        side_idx   = 5
                        y          = cube_diameter - 1
                    elif side_idx == 2:
                        side_idx   = 0
                        y          = cube_diameter - 1
                    elif side_idx == 3:
                        side_idx   = 2
                        facing_idx = 0
                        y          = x
                        x          = 0
                    elif side_idx == 4:
                        side_idx   = 2
                        y          = cube_diameter - 1
                    elif side_idx == 5:
                        side_idx   = 3
                        y          = cube_diameter - 1                    
                elif y == cube_diameter:
                    if side_idx == 0:
                        side_idx   = 2
                        y          = 0
                    elif side_idx == 1:
                        side_idx   = 2
                        facing_idx = 2
                        y          = x
                        x          = cube_diameter - 1
                    elif side_idx == 2:
                        side_idx   = 4
                        y          = 0
                    elif side_idx == 3:
                        side_idx   = 5
                        y          = 0
                    elif side_idx == 4:
                        side_idx   = 5
                        facing_idx = 2
                        y          = x
                        x          = cube_diameter - 1
                    elif side_idx == 5:
                        side_idx   = 1
                        y          = 0
                side = cube_map[side_idx]
                sym  = side[y][x]

                if sym == ' ':
                    print(f"cube side has space: {x} {y} at side: {side_idx}")
                    sys.exit()                
                break

            sym = side[y][x]
            
            if sym == '#':
                break
            elif sym == ".":
                p0_sfxy[0] = side_idx
                p0_sfxy[1] = facing_idx
                p0_sfxy[2] = x
                p0_sfxy[3] = y
                #print(f"MOVE: {p0_sfxy}")
            else:
                print(f"wrong symbol: '{sym}'")
                sys.exit()

        #print(f"DONE: at: {p0_sfxy}")
        
    else:
        if instruction == 'R':
            p0_sfxy[1] = (p0_sfxy[1] + 1) % 4
        else:
            p0_sfxy[1] = (p0_sfxy[1] + 3) % 4    

        
        #print(f"after {instruction}. at: {p0_sfxy}")

# indexing starts at 0

if p0_sfxy[0] == 0:
    p0_sfxy[2] += cube_diameter  + 1
    p0_sfxy[3] += 1
    
elif p0_sfxy[0] == 1:
    p0_sfxy[2] += cube_diameter * 2  + 1
    p0_sfxy[3] += 1
    
elif p0_sfxy[0] == 2:
    p0_sfxy[2] += cube_diameter + 1
    p0_sfxy[3] += cube_diameter + 1
    
elif p0_sfxy[0] == 3:
    p0_sfxy[2] += 1
    p0_sfxy[3] += cube_diameter * 2+ 1
    
elif p0_sfxy[0] == 4:
    p0_sfxy[2] += cube_diameter + 1
    p0_sfxy[3] += cube_diameter * 2 + 1
    
elif p0_sfxy[0] == 5:
    p0_sfxy[2] += 1
    p0_sfxy[3] += cube_diameter * 3 + 1

print()
print(f"score: {p0_sfxy[3] * 1000 + p0_sfxy[2] * 4 + p0_sfxy[1]}")

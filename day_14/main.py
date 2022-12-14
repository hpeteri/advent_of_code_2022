# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("input.txt", "r") as f:
    lines = f.read().splitlines()
    f.close()

min_x = 100000;
min_y = 0

max_x = -1;
max_y = -1;

instructions = []
for line in lines:
    path = []
    
    for p in line.split("->"):
        xy = p.split(",")
        x = int(xy[0])
        y = int(xy[1])
        path.append([x, y])
        
        min_x = min(min_x, x)
        max_x = max(max_x, x)

        max_y = max(max_y, y)
        
    instructions.append(path)

#part 2
min_x -= (max_x - min_x) * 2
max_x += (max_x - min_x) * 2
max_y += 2


grid = [["." for x in range(max_x - min_x + 1)] for y in range(max_y - min_y + 1)]

for x in range(max_x - min_x + 1):
    grid[-1][x] = "#"

for inst in instructions:

    prev = inst[0]
    prev[0] -= min_x
    prev[1] -= min_y
    
    for p in inst[1:]:
        p[0] -= min_x
        p[1] -= min_y
        
        start_x = min(prev[0], p[0])
        end_x   = max(prev[0], p[0])

        start_y = min(prev[1], p[1])
        end_y   = max(prev[1], p[1])
        
        for x in range(end_x - start_x + 1):
            grid[p[1]][start_x + x] = "#"

        for y in range(end_y - start_y + 1):
            grid[start_y + y][p[0]] = "#"
            
        prev = p
        

round_idx = 0

def print_grid():
    print()
    print(round_idx)
    for row in grid:
        print("".join(row))
        
is_raining_sand = True
while is_raining_sand:
    sand_x = 500 - min_x
    sand_y = 0

    while(1):
        try:
            down = grid[sand_y + 1][sand_x]
            left = grid[sand_y + 1][sand_x - 1]
            right = grid[sand_y + 1][sand_x + 1]
        except:
            is_raining_sand = False
            round_idx -= 1
            break
                    
        if down != ".": # if beneath is not empty
            if left == '.': 
                sand_x -= 1
                sand_y += 1
            elif right == '.':
                sand_x += 1
                sand_y += 1
            else:
                if sand_x > max_x - min_x or sand_x < 0:
                    is_raining_sand = False
                    break
                if sand_y > max_y - min_y or sand_y < 0:
                    is_raining_sand = False
                    break
                
                grid[sand_y][sand_x] = "o"
                #print_grid()
                if sand_y == 0 and sand_x == 500 - min_x:
                    round_idx += 1
                    is_raining_sand = False
                    break
                

                break
        else:
            sand_y += 1
            
    round_idx += 1
    

print_grid()
print(f"units dropped: {round_idx - 1}")
    
    




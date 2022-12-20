# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

import sys
# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if len(sys.argv) < 2:
    print("pass file name as argument")
    sys.exit()

    
with open(sys.argv[1], "r") as f:
    lines = f.read().splitlines()
    f.close()

min_x = 9999
min_y = 9999
min_z = 9999

max_x = -9999
max_y = -9999
max_z = -9999

for line in lines:
    if len(line) == 0:
        break
    
    pos = line.split(",")
    min_x = min(int(pos[0]), min_x)
    min_y = min(int(pos[1]), min_y)
    min_z = min(int(pos[2]), min_z)

    max_x = max(int(pos[0]), max_x)
    max_y = max(int(pos[1]), max_y)
    max_z = max(int(pos[2]), max_z)


grid = [[[0 for x in range(max_x - min_x + 3)] for y in range(max_y - min_y + 3)] for z in range(max_z - min_z + 3)]


side_count = 0

def add_surrounding_count(x0, y0, z0, grid):
    offsets = [[0,0,1], [0,0,-1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0]]
    for offset in offsets:
        x1 = x0 + offset[0]
        y1 = y0 + offset[1]
        z1 = z0 + offset[2]
        
        if z1 < 0 or z1 >= len(grid):
            continue
                    
        if y1 < 0 or y1 >= len(grid[z1]):
            continue
            
        if x1 < 0 or x1 >= len(grid[0][0]):
            continue
    
        if grid[z1][y1][x1] != -1:
            grid[z1][y1][x1] += 1

surface_area = 0
for line in lines:
    if len(line) == 0:
        break
    
    pos = line.split(",")
    x = int(pos[0]) - min_x + 1
    y = int(pos[1]) - min_y + 1
    z = int(pos[2]) - min_z + 1

    add_surrounding_count(x, y, z, grid)
    grid[z][y][x] = -1
    
# floodfill
grid2 = [[[0 for x in range(max_x - min_x + 3)] for y in range(max_y - min_y + 3)] for z in range(max_z - min_z + 3)]

to_check = [[0,0,0]]

def flood_fill(x0, y0, z0, to_check):
    offsets = [[0,0,1], [0,0,-1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0]]
    for offset in offsets:
        x1 = x0 + offset[0]
        y1 = y0 + offset[1]
        z1 = z0 + offset[2]
        
        if z1 < 0 or z1 >= len(grid):
            continue
                    
        if y1 < 0 or y1 >= len(grid[z1]):
            continue
            
        if x1 < 0 or x1 >= len(grid[0][0]):
            continue

        is_checked = grid2[z1][y1][x1]
        p0         = grid[z1][y1][x1]
        
        if is_checked != 1 and p0 >= 0:
            to_check.append([x1,y1,z1])

while len(to_check):
    p = to_check.pop()

    x = p[0]
    y = p[1]
    z = p[2]

    if grid2[z][y][x] != 1:
        surface_area += grid[z][y][x]
        
    grid2[z][y][x] = 1

    
    flood_fill(x, y, z, to_check)

print(f"surface area: {surface_area}")
    

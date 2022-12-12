# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("input.txt", "r") as f:
    lines = f.read().splitlines()
    f.close()

grid = [[0 for c in range(len(lines[0]))] for c in range(len(lines))]

from enum import Enum
class Directions(Enum):
    up    = 1
    down  = 2
    left  = 4
    right = 8

paths_to_check = []

for y in range(len(grid)):
    for x in range(len(grid[0])):
        up   = y - 1
        down = y + 1
        left   = x - 1
        right  = x + 1

        current = lines[y][x]
        if current == 'S':
            current = 'a'

        if current == 'a':
            paths_to_check.append([x, y, 0, []])
            
        # up
        if up >= 0:
            adjacent = lines[up][x]
            if adjacent == 'E':
                adjacent = 'z'
                
            diff = ord(adjacent) - ord(current)
            if diff <= 1:
                grid[y][x] |= Directions.up.value    

        # down
        try:
            adjacent = lines[down][x]
            if adjacent == 'E':
                adjacent = 'z'

            diff = ord(adjacent) - ord(current)
            if diff <= 1:
                grid[y][x] |= Directions.down.value
                
        except:
            pass
        
        if left >= 0:
            adjacent = lines[y][left]
            if adjacent == 'E':
                adjacent = 'z'
            
            diff = ord(adjacent) - ord(current)
            if diff <= 1:
                grid[y][x] |= Directions.left.value
            
        # right
        try:
            adjacent = lines[y][right]
            if adjacent == 'E':
                adjacent = 'z'
            
            diff = ord(adjacent) - ord(current)
            if diff <= 1:
                grid[y][x] |= Directions.right.value
                
        except:
            pass

solutions = []

checked = [[-1 for c in range(len(lines[0]))] for c in range(len(lines))]

def check_path(x, y, path_length, path):
    if not checked[y][x] == -1 and checked[y][x] <= path_length:
        return

    if lines[y][x] == 'E':
        solutions.append([path_length, path])
        return

    dirs = grid[y][x]

    checked[y][x] = path_length
    path.append([y, x])                     
                         
    if dirs & Directions.up.value:
        paths_to_check.append([x, y - 1, path_length + 1, path[:]])
        

    if dirs & Directions.down.value:
        paths_to_check.append([x, y + 1, path_length + 1, path[:]])

    if dirs & Directions.left.value:
        paths_to_check.append([x - 1, y, path_length + 1, path[:]])

    if dirs & Directions.right.value:
        paths_to_check.append([x + 1, y, path_length + 1, path[:]])


while len(paths_to_check):
    path = paths_to_check.pop()
    check_path(path[0], path[1], path[2], path[3])
    

solutions.sort()
solutions = solutions[:1]
print()
for sol in solutions:
    print(f"{sol[0]} : {len(sol[1])}")
    
    p = [['[_]' for c in range(len(lines[0]))] for c in range(len(lines))]
    for (idx, point) in enumerate(sol[1]):
        
        p[point[0]][point[1]] = '[#]'

    for l in p:
          print("".join(l))
    
    
    

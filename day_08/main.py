#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os
# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))

f_handle = open("input.txt", "r")
lines = f_handle.read().splitlines()
f_handle.close()


width = len(lines[0])
height = len(lines)

print(width, height)

grid = [0 for c in range(width * height)]

# look from left
for y in range(height):
    max_height = 0;
    for x in range(width):
        tree_height = int(lines[y][x]);
        if tree_height > max_height or x == 0:
            grid[y * width + x] = 1
            max_height = tree_height

# look from right
for y in range(height):
   max_height = 0;
   for x in range(width):
       x = width - 1 - x
       tree_height = int(lines[y][x])
       if tree_height > max_height or x == width - 1:
           grid[y * width + x] = 1
           max_height = tree_height
           


# look from left
for x in range(width):
    max_height = 0;
    for y in range(height):
        tree_height = int(lines[y][x]);
        if tree_height > max_height or y == 0:
            grid[y * width + x] = 1
            max_height = tree_height

# look from right
for x in range(width):
    max_height = 0;
    for y in range(height):
        y = height - 1 - y
        tree_height = int(lines[y][x])
        if tree_height > max_height or y == height - 1:
            grid[y * width + x] = 1
            max_height = tree_height
           


            


grid.sort()

nums = []
for c in grid:
    if c == 1:
        nums.append(1)

print("count: ", len(nums))

def calculate_scenic_score(x_0, y_0, lines):
    score_left  = 0
    score_right = 0
    score_up    = 0
    score_down  = 0

    tree_height = int(lines[y_0][x_0]);
    
    # look left
    for x in reversed(range(x_0)):
        h = int(lines[y_0][x]);
        score_left += 1
        if h >= tree_height:
            break

    # look right
    for x in range(x_0 + 1, width):
        h = int(lines[y_0][x]);
        score_right += 1
        if h >= tree_height:
            break

    # look up
    for y in reversed(range(y_0)):
        h = int(lines[y][x_0]);
        score_up += 1
        if h >= tree_height:
            break
        
    # look down
    for y in range(y_0 + 1, height):
        h = int(lines[y][x_0]);
        score_down += 1
        if h >= tree_height:
            break    
    
    return score_left * score_right * score_up * score_down

scenic_score = 0;
for y in range(height):
    for x in range(width):
        scenic_score = max(scenic_score, calculate_scenic_score(x, y, lines))

print("scenic score: ", scenic_score)

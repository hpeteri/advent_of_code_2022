# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

import sys
# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("test_input.txt", "r") as f:
    lines = f.read().splitlines()
    f.close()

grid = [['.' for x in range(7)] for y in range(10)]
highest_points = [0 for x in range(7)]

rocks = []

rocks.append([["#","#","#","#"]])
rocks.append([[".","#","."], ["#","#","#"], [".","#",","]])
rocks.append([["#","#","#"], [".",".","#"], [".",".","#"]])
rocks.append([["#"], ["#"], ["#"], ["#"]])
rocks.append([["#", "#"], ["#", "#"]])

def print_grid():
    print()
    print(len(grid))
    for row in grid[::-1]:
        print(row)

    print(f"highest_points: {highest_points}")
    print(f"highest point: {max(highest_points)}")

print_grid()

rock_idx     = -1
rock_points  = []
rock_count   = 0
rock_symbols = ["#", "$", "@", "X", "O", "+"]

def drop_rock():
    global rocks
    global rock_idx
    global rock_points
    
    
    rock_idx = (rock_idx + 1) % len(rocks)
    rock = rocks[rock_idx]
    
    rock_points = []
    y_offset = max(highest_points) + 3
    
    for y_idx, y in enumerate(rock):
        for x_idx, x in enumerate(y):
            if x == "#":                
                rock_points.append([x_idx + 2, y_offset + y_idx])
                #print()            
                #print("drop rock")
                #for row in rock:
                #    print(row)
                #print(rock_points)
instructions = []
for line in lines:
    for instruction in line:
        instructions.append(instruction)

print(f"instruction count: {len(instructions)}")

i = -1

snapshots = []
test = [[1,2,3],[4,5,6],[7,8,9]]
snapshot_found = False
while True:
    i = (i + 1) % len(instructions)
    instruction = instructions[i]
    if len(rock_points) == 0:
        if rock_idx == 0:
            arr = grid[-40:-5]
            s = ""
            for r in arr:
                rs = "".join(r)
                s = f"{s}{rs}\n"

            found = False
            for snapshot_idx, snapshot in enumerate(snapshots):
                if s == snapshot[0]:
                    
                    print("MATCHING:")
                    print(f"rocks: {rock_count + 1}")
                    print(f"instruction idx: {i}")
                    print(max(highest_points))
                    print(s)
                    print()
                    #print(f"rocks: {snapshot[3]}")
                    #print(f"instruction idx: {snapshot[2]}")
                    #print(snapshot[1])
                    #print(snapshot[0])
                    #print()
                    if not snapshot_found:
                        snapshots = [snapshot, [max(highest_points), i, rock_count + 1]]
                        
                    snapshot_found = True
                    
            if not found and not snapshot_found:
                snapshots.append([s, max(highest_points), i, rock_count + 1])
                
        drop_rock()
        rock_count += 1
        
        # part 1
        #if rock_count >= 2023:
        #    print_grid()
        #    sys.exit()
        # part 2


        #MATCHING:
        #rocks: 2362
        #instruction idx: 3778
        #3691

        #MATCHING:
        #rocks: 4067
        #instruction idx: 3778
        #6340

        
        # repeating pattern arises:
        # rocks | instruction idx | height
        # 2362  | 3778            | 3691
        # 4067  | 3778            | 6340

        # rock_delta   = 1705
        # height_delta = 2649

        # excess rocks = 1000000000000 % rock_delta = 1585
        # repetitions  = int(1000000000000 / rock_delta) = 586510263

        # height_0 = repetitions * height_delta = 1553665686687
        # rocks to drop = 1585 + 1 -> highest point 2468
        # total height  = 1553665686687 + 2468 = 1553665689159 too hight
                
        if rock_count >= 1585 + 1
            print_grid()
            sys.exit()
        
    
    x_delta = -1
    y_delta = 1
    
    if instruction == ">":
        x_delta = 1

    if instruction == "<":
        x_delta = -1

    # check x delta
    if x_delta == -1:
        for point in rock_points:
            if point[0] == 0:
                x_delta = 0

    elif x_delta == 1:
        for point in rock_points:
            if point[0] == len(grid[0]) - 1:
                x_delta = 0
        
    if x_delta != 0:
        for point in rock_points:
            x_0 = point[0] + x_delta
            y_0 = point[1]

            try:
                if grid[y_0][x_0] != '.':
                    x_delta = 0
                    break
            except:
                pass
        
    # move in x
    for point in rock_points:
        point[0] += x_delta
        if point[0] >= 7:
            print("over 7 x")
            sys.exit()
        if point[0] < 0:
            print("under 0 x")
            sys.exit()
        
        

    # check y delta
    for point in rock_points:
        x_0 = point[0]
        y_0 = point[1] - 1
        
        # y_1 = highest_points[x_0]
        # if y_0  == y_1:
        #     y_delta = 0

        if y_0 < 0:
            y_delta = 0
        else:
            if grid[y_0][x_0] != '.':
                y_delta = 0
                
        
    # rock stopped
    if y_delta == 0:

        for point in rock_points:
            x_0 = point[0]
            y_0 = point[1]

            h = max(highest_points)
            while h + 6 >= len(grid):
                grid.append(['.' for x in range(7)])
                
            grid[y_0][x_0] = rock_symbols[rock_idx]
            highest_points[x_0] = max(highest_points[x_0], y_0 + 1)
                    

        rock_points = []
                
    else:
        # move in y
        for point in rock_points:
            point[1] -= y_delta
        
            if point[1] < 0:
                print_grid()
                print(rock_points)
                print("abort")
                sys.exit()

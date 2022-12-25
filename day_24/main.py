# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.


import sys
from copy import deepcopy

from collections import deque

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

fastest_path = None
    
class State:
    def __init__(self, walls, xy, target, turn, blizzards):
        self.walls     = walls
        self.positions = [xy]
        self.turn      = turn
        self.target    = target
        self.blizzards = deepcopy(blizzards)
        
    def move_blizzards(self):
        updated_blizzards = {}
        for xy in self.blizzards:
            
            x = int(xy.split(",")[0])
            y = int(xy.split(",")[1])

            for direction in self.blizzards[f"{x},{y}"]:
                
                x_0 = x
                y_0 = y
                
                while True:
                    if direction == "<":
                        x_0 -= 1
                    elif direction == ">":
                        x_0 += 1
                    elif direction == "^":
                        y_0 -= 1
                    elif direction == "v":
                        y_0 += 1
                    else:
                        print(f" ?? {direction} ??")
                        
                    x_0 = x_0 % len(self.walls[0])
                    y_0 = y_0 % len(self.walls)

                    if self.walls[y_0][x_0] == "#":
                        continue
                    break
                
                try:
                    it = updated_blizzards[f"{x_0},{y_0}"]
                except:
                    updated_blizzards[f"{x_0},{y_0}"] = []

                updated_blizzards[f"{x_0},{y_0}"].append(direction)
                                
        self.blizzards = updated_blizzards
        self.turn += 1

    def get_moves(self):
        
        
        grid = deepcopy(self.walls)
        for xy in self.blizzards:
            x = int(xy.split(",")[0])
            y = int(xy.split(",")[1])

            grid[y][x] = "#"

        moves = []
        for xy in self.positions:
            if grid[xy[1]][xy[0]] != "#":
                moves.append(xy)

            # left
            left_x = xy[0] - 1
            left_y = xy[1]
            if left_x >= 0  and grid[left_y][left_x] != "#":
                moves.append([left_x, left_y])

            # right
            right_x = xy[0] + 1
            right_y = xy[1]
            if right_x < len(self.walls[0]) and grid[right_y][right_x] != "#":
                moves.append([right_x, right_y])

            # down
            down_x = xy[0]
            down_y = xy[1] + 1
            if down_y < len(self.walls) and grid[down_y][down_x] != "#":
                moves.append([down_x, down_y])

            # up
            up_x = xy[0]
            up_y = xy[1] - 1
            if up_y >= 0 and grid[up_y][up_x] != "#":
                moves.append([up_x, up_y])


        grid = deepcopy(self.walls)
        self.positions = []
        for move in moves:
            if grid[move[1]][move[0]] != "#":
                self.positions.append(move)
            
            grid[move[1]][move[0]] = "#"
        

    def is_winner(self):
        for xy in self.positions:
            if(xy[1] == self.target[1] and xy[0] == self.target[0]):
                self.positions = [xy]
                return True

        return False

    def move_to_target(self):
        while True:
            if self.is_winner():
                break

            self.move_blizzards()
            self.get_moves()

walls = []
blizzards = {}
for y, line in enumerate(lines):
    walls.append([])
    for x, c in enumerate(line):
        if c == "#":
            walls[-1].append('#')
        else:
            walls[-1].append(' ')
            if c != '.':
                # blizzard
                blizzards[f"{x},{y}"] = [c]

state = State(walls, (1, 0), (len(walls[-1]) - 2, len(walls) - 1), 0, blizzards)
state.move_to_target()
# part 1
print(f"1 score: {state.turn}")

# part 2
state.target = (1, 0)
state.move_to_target()

state.target = (len(walls[-1]) - 2, len(walls) - 1)
state.move_to_target()


print(f"2 score: {state.turn}")

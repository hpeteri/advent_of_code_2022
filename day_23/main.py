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

elves = {}
directions = [[0, 1], [0, -1], [1, 1], [1, 0], [1, -1], [-1, 1], [-1, 0], [-1, -1]]

def get_loc_string(xy):
    return f"{xy[0]}, {xy[1]}"

def debug_print_elves(rnd):
    
    # debug print    
    min_x = 9999
    min_y = 9999
    max_x = -9999
    max_y = -9999
    
    for i, xy in enumerate(elves):
        x = int(xy.split(",")[0])
        y = int(xy.split(",")[1])

        min_x = min(min_x, x)
        min_y = min(min_y, y)

        max_x = max(max_x, x)
        max_y = max(max_y, y)

    
    min_x -= 1
    min_y -= 1

    max_x += 1 
    max_y += 1
    
    
    grid = [["." for x in range(max_x - min_x + 1)] for y in range(max_y - min_y + 1)]
    for xy in elves:
        x = int(xy.split(",")[0]) - min_x
        y = int(xy.split(",")[1]) - min_y

        grid[y][x] = '#'


    print()
    print(f"=== round {rnd} ===")
    print(f"elves: {len(elves)}")
    print(f"score: {(max_x - min_x - 1) * (max_y - min_y - 1) - len(elves)}")
    #for row in grid:
    #   print("".join(row))

    

class Elf:
    def __init__(this, xy):
        this.moves = []
        this.xy    = xy
        # N
        # o o o
        # - x -
        # - - -
        
        this.moves.append([[1,-1], [0, -1], [-1,-1]])

        # S
        # - - -
        # - x -
        # o o o        
        this.moves.append([[-1,1], [0, 1], [1,1]])

        # E
        # - - o
        # - x o
        # - - o
        this.moves.append([[-1,-1], [-1, 0], [-1,1]])

        # W
        # o - -
        # o x -
        # o - -
        this.moves.append([[1,-1], [1, 0], [1,1]])
                
    def get_move_transaction(this, elves):
        for move_idx, move in enumerate(this.moves):
            is_empty = True
            for d in move:
                
                xy_0     = this.xy[:]
                xy_0[0] += d[0]
                xy_0[1] += d[1]
                
                try:
                    it = elves[get_loc_string(xy_0)]
                    is_empty = False
                except:
                    pass

            if is_empty:
                x = 0
                y = 0
                for d in move:
                    x += d[0]
                    y += d[1]

                x /= len(move)
                y /= len(move)

                x += this.xy[0]
                y += this.xy[1]
                return [int(x), int(y)]
            else:
                pass
            
        return this.xy

    def move_to(this, x, y):
        this.xy = [x, y]

    def update_moves(this):
        first = this.moves[0]
        this.moves = this.moves[1:]
        this.moves.append(first)
        
        
for y, line in enumerate(lines):
    for x, sym in enumerate(line):
        if sym == '#':
            xy = [x, y]
            
            elves[get_loc_string(xy)] = Elf(xy)
        

debug_print_elves("start")
rnd = -1
while True:
    rnd += 1
    
    # half 1
    move_transactions = {}

    move_count = 0
    for elf in elves:
        elf = elves[elf]
        xy = elf.xy
        
        has_adjacent_elf = False
        for direction in directions:
            xy_1 = [xy[0] + direction[0], xy[1] + direction[1]]

            try:
                it = elves[get_loc_string(xy_1)]
                has_adjacent_elf = True
                move_count += 1
            except:
                pass
            
        if not has_adjacent_elf:
            try:
                it = move_transactions[get_loc_string(xy)]
            except:
                move_transactions[get_loc_string(xy)] = []
                
            move_transactions[get_loc_string(xy)].append(elf)
            #print(f"stay in place {xy}")
        else:
            xy_1 = elf.get_move_transaction(elves)

            try:
                it = move_transactions[get_loc_string(xy_1)]
            except:
                move_transactions[get_loc_string(xy_1)] = []
                
            move_transactions[get_loc_string(xy_1)].append(elf)
            #print(f"move from {xy} to {xy_1}")
            
    # half 2
    elves = {}
    for move in move_transactions:
        
        elves_to_move = move_transactions[move]
        if len(elves_to_move) == 1:
            elf = elves_to_move[0]
            x = int(move.split(",")[0])
            y = int(move.split(",")[1])

            elf.move_to(x, y)
            elves[get_loc_string([x, y])] = elf
        else:
            for elf in elves_to_move:
                move_count -= 1
                x = elf.xy[0]
                y = elf.xy[1]
                    
                elves[get_loc_string([x, y])] = elf
                    

    # end of round
    for xy in elves:
        elves[xy].update_moves()
    
    if move_count == 0:
        break
    #debug_print_elves(rnd)
    
debug_print_elves(rnd + 1)    

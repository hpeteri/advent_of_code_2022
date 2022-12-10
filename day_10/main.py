# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

# set working dir to file location

import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

f = open("input.txt", "r")
lines = f.read().splitlines()
f.close()


cycle_count        = 1
register_X         = 1
register_X_updates = []
update_cycles      = []
signal_strengths   = []

crt = [['.' for c in range(40)] for i in range(6)]

def crt_display():
    print()
    for scan_line in crt:
        ln = "".join(scan_line)
        print(ln)
    print()


for line in lines:
    line = line.split(' ')

    instruction = line[0]
    if instruction == "noop":
        cycle_count += 1

    elif instruction == "addx":
        register_X_updates.append(int(line[1]))
        update_cycles.append(cycle_count + 2)
        cycle_count += 2
    
    
cycle_count = 1;
while len(update_cycles):
    
    cycle_count += 1
    
    if len(update_cycles):
        wanted_cycles = update_cycles[0];
        if wanted_cycles == cycle_count:
            register_X += register_X_updates[0]
            update_cycles = update_cycles[1:]
            register_X_updates = register_X_updates[1:]
    
    if ((cycle_count + 20) % 40 == 0):
        signal_strengths.append([cycle_count, cycle_count * register_X])


    # draw_sprite
    cycle_count -= 1
    y_pos = int((cycle_count) / 40)
    x_pos = (cycle_count - y_pos * 40)
    
    char = '.'
    if register_X - 1 <= x_pos  <= register_X + 1:
        char = '#'
    
    crt[y_pos][x_pos] = char


    cycle_count += 1


signal_sum = 0;
for i in signal_strengths:
    signal_sum += i[1]

print("signal_sum: ", signal_sum)

crt_display()

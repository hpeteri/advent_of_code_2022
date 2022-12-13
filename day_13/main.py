# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("input.txt", "r") as f:
    lines = f.read().splitlines()
    f.close()

pairs = [[]]

for line in lines:
    if len(line) == 0:
        pairs.append([])
    else:
        line = line[1: -1]
        tokens = line.split(",")
        values = []

        depth     = 0
        new_depth = 0
        for token in tokens:
            for c in token:
                if c == "[":
                    it = values
                    for i in range(depth):
                        it = it[-1]
                    it.append([])
                    
                    depth += 1
                    new_depth = depth
                    
                if c == "]":
                    new_depth -= 1
                    
            token = token.strip("[]")
            if depth == 0:
                try:
                    values.append(int(token))
                except:
                    pass
                    #values.append(token)
            else:
                it = values
                for i in range(depth):
                    it = it[-1]
                try:
                    it.append(int(token))
                except:
                    pass
                    #it.append(token)
            
            depth = new_depth
        pairs[-1].append(values)
        
def compare_lists(left_lst, right_lst, depth):
    
    indent = ' ' * depth
    for i in range(min(len(left_lst), len(right_lst))):
        left = left_lst[i]
        right = right_lst[i]
        if type(left) == type(1) and type(right) == type(1):
            if left < right:
                return 1
            elif left == right:
                continue;
            else:
                return 0

        if type(left) == type(right) == type([]):
            result = compare_lists(left, right, depth + 2)
            if result != -1:
                return result
            
        else:
            if type(right) == type([]):
                left = [left]
                                               
            elif type(left) == type([]):
                right = [right]
            else:
                if type(right) == type([]):
                    return 1                
                elif type(left) == type([]):
                    return 0
                else:
                    return 0
            result = compare_lists(left, right, depth)
            if result != -1:
                return result

    if len(left_lst) < len(right_lst):
        return 1
    elif len(left_lst) == len(right_lst):
        return -1
    else:
        return 0

right_order = []
for (i, pair) in enumerate(pairs):
    if compare_lists(pair[0], pair[1], 1) == 1:
        right_order.append(i + 1)

print("right order indices sum: ", sum(right_order))


packets = []
pairs.append([[[2]], [[6]]])
for pair in pairs:
    packets.extend(pair)

sorted_packets = []
tries = 0
while(len(packets)):
    
    packet_0 = packets[0]
    packets = packets[1:]
        
    is_sorted = 1
    for packet_1 in packets:
        result = compare_lists(packet_0, packet_1, 1)
        if result == 0:
            is_sorted = 0

    if is_sorted:
        sorted_packets.append(packet_0)
        tries = 0
    else:
        packets.append(packet_0)


idx_0 = sorted_packets.index([[2]]) + 1
idx_1 = sorted_packets.index([[6]]) + 1

print(f"indices: {idx_0} & {idx_1}, result: {idx_0 * idx_1}")

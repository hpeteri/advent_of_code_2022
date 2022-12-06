#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os

def print_stacks(stacks):    
    for stack in stacks:
        print(stack)
    print()

def print_stack_tops(stacks):
    for stack in stacks:
        if(len(stack)):
            print(stack.pop())
    print()    

    
# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))
cwd = os.getcwd()

f = open("input.txt", "r")
lines = f.read().splitlines()
f.close()

stacks = [[], [], [], [], [], [], [], [], []]

for (idx, line) in enumerate(lines):
    if len(line) == 0:
        lines = lines[idx + 1::]
        print("done");
        break

    
    for i in range(9):
        if(i * 4 + 1 > len(line)):
           break
           
        it = line[i * 4 + 1];
        if(it != ' '):
            stacks[i].append(it)
   
   

for (idx, stack) in enumerate(stacks):
    if(len(stack)):
        stack.pop()
    stack = stack[::-1]
    stacks[idx] = stack

print_stacks(stacks)       
for line in lines:
    line  = line.split(' ')
    
    count = int(line[1])
    src   = int(line[3]) - 1 
    dst   = int(line[5]) - 1

    tmp = []
    for i in range(count):
        if len(stacks[src]) == 0:
            break
        
        item = stacks[src].pop()
        tmp.append(item)

    tmp = tmp[::-1]
    stacks[dst].extend(tmp)
            
print_stacks(stacks)       
print_stack_tops(stacks)        


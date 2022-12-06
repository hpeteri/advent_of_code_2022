#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os

# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))
cwd = os.getcwd()

f = open("input.txt", "rb")

current_calories = 0
all_calories = []

while(1):
    data = f.readline()
    try:
        current_calories += int(data)
    except:
        all_calories.append(current_calories);
        current_calories = 0
        
    if(len(data) == 0):
        break

f.close()

all_calories.sort(reverse=True);
print("[0]:   ", all_calories[0]);
print("[1]:   ", all_calories[1]);
print("[2]:   ", all_calories[2]);
print("total: ", all_calories[2] + all_calories[1] + all_calories[0]);

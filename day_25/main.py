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


total = 0
def snafu_to_base10(line) -> int:
    result = 0
    
    for idx, c in enumerate(line):
        dec = 5 ** (len(line) - idx -1)

        if c == '=':
            result -= dec * 2
        elif c == '-':
            result -= dec
        else:
            result += dec * int(c)

    return result
    
for line in lines:
    result = snafu_to_base10(line)    
    total += result

print(f"total: {total}")

def base10_to_snafu(num):
    snafu = ""
    while num != 0:
        num, mod = divmod(num, 5)

        if mod >= 3:
            num += 1
            mod -= 5
        snafu += "=-012"[mod + 2]
    return snafu[::-1]            

bts = base10_to_snafu(total)
print(f"'{total}' -> '{bts}' -> '{snafu_to_base10(bts)}'")


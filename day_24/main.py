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


for line in lines:
    print(line)

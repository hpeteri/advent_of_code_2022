#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os

def is_start_of_packet(tokens):
    tokens = [ c for c in tokens ]
    
    tokens.sort()
    prev = tokens[0];
    for i in range(1, len(tokens)):
        if(tokens[i] == prev):
            return False

        prev = tokens[i]
        
    return True
    
# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))
cwd = os.getcwd()

f_handle = open("input.txt", "r")
f = f_handle.read()
f_handle.close()


idx = 0
packet_len = 14
for i in range(len(f) - packet_len):
    tokens = f[i:i + packet_len];
    if(is_start_of_packet(tokens)):
       idx = i + packet_len
       break
    

print("start of packet ended: {}".format(idx))

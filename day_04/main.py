#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os


# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))
cwd = os.getcwd()

f = open("input.txt", "r")

lst = f.read().split('\n')
lst.pop()

fully_contained_count = 0
partial_count = 0

for item in lst:
    ranges = item.split(',');
    
    ranges[0] = ranges[0].split('-')
    ranges[1] = ranges[1].split('-')
    
    ranges[0][0] = int(ranges[0][0])
    ranges[0][1] = int(ranges[0][1])
    ranges[1][0] = int(ranges[1][0])
    ranges[1][1] = int(ranges[1][1])
    
    # min start should be at index 0
    # if start is same for both, index 0 should range with largest end
    if(ranges[0][0] > ranges[1][0] or
       ((ranges[0][0] == ranges[1][0] and ranges[0][1] <= ranges[1][1]))):
        tmp = ranges[0]
        ranges[0] = ranges[1]
        ranges[1] = tmp
        
    if(ranges[0][1] >= ranges[1][1]):
        fully_contained_count += 1

    if(ranges[1][0] <= ranges[0][1]):
        partial_count += 1
        
print("fully contained: {}".format(fully_contained_count))
print("partially contained: {}".format(partial_count))

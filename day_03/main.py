#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os

def get_score_for_token(token):
    if 'a' <= token <= 'z':
        return ord(token) - ord('a') + 1

    if 'A' <= token <= 'Z':
        return ord(token) - ord('A') + 27    
    return 0


# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))
cwd = os.getcwd()

f = open("input.txt", "r")

lst = f.read().split('\n')
lst.pop()

score = 0
for item in lst:
    split_at = int(len(item) / 2)
    # lst[idx] = [i[:split_at], i[split_at:]]
    compartment_0 = item[:split_at]
    compartment_1 = item[split_at:]
    for i in range(split_at):
        token_0 = compartment_0[i]
        token_1 = compartment_1.find(token_0)

        # not found in both compartments
        if(token_1 == -1):
            continue

        score += get_score_for_token(token_0)
        break
        
print("score: {}".format(score))

score = 0
for idx in range(int(len(lst) / 3)):
    cmp_0 = lst[idx * 3]
    cmp_1 = lst[idx * 3 + 1]
    cmp_2 = lst[idx * 3 + 2]

    for i in range(len(cmp_0)):
        token_0 = cmp_0[i]
        
        token_1 = cmp_1.find(token_0)
        if(token_1 == -1):
            continue

        token_2 = cmp_2.find(token_0)
        if(token_2 == -1):
            continue

        score += get_score_for_token(token_0)
        break
    
print("group score: {}".format(score))

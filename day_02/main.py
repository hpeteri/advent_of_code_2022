#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os

def get_win_score(a, b):
    # (0 if you lost, 3 if the round was a draw, and 6 if you won)
    
    #     X   Y   Z
    # A |   | x |   |
    # B |   |   | x |
    # C | x |   |   |
        
    # win
    if(b == 'X' and a == 'C'):
        return 6

    if(b == 'Y' and a == 'A'):
        return 6

    if(b == 'Z' and a == 'B'):
        return 6

    # draw
    if(b == 'X' and a == 'A'):
        return 3

    if(b == 'Y' and a == 'B'):
        return 3

    if(b == 'Z' and a == 'C'):
        return 3

    # lose
    return 0

def get_action_score(b):
    # The score for a single round is the score for the shape you selected
    # (1 for Rock, 2 for Paper, and 3 for Scissors)
    if(b == 'X'):
        return 1

    if(b == 'Y'):
        return 2
    
    return 3

def get_win_score_2(a, b):
    # (0 if you lost, 3 if the round was a draw, and 6 if you won)
    # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.

    if(b == 'X'):
        return 0

    if(b == 'Y'):
        return 3

    return 6

def get_action_score_2(a, b):
    # (1 for Rock, 2 for Paper, and 3 for Scissors)

    #     X   Y   Z
    # A | Y | Z | X |
    # B | X | Y | Z |
    # C | Z | X | Y |
        
    if(b == 'X'):
        if(a == 'A'):
            return 3        
        if(a == 'B'):
            return 1
        if(a == 'C'):
            return 2
        
    if(b == 'Y'):
        if(a == 'A'):
            return 1        
        if(a == 'B'):
            return 2
        if(a == 'C'):
            return 3
        
    #if(b == 'Z'):
    if(a == 'A'):
        return 2     
    if(a == 'B'):
        return 3
    if(a == 'C'):
        return 1
        
# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))
cwd = os.getcwd()

f = open("input.txt", "r")

actions = f.read().split('\n')

for (idx, i) in enumerate(actions):
    actions[idx] = i.split(' ')

actions.pop()

score = 0

for action in actions:
    a = action[0]
    b = action[1]

    score += get_win_score(a, b)
    score += get_action_score(b)

print("score: {}".format(score))

score = 0
for action in actions:
    a = action[0]
    b = action[1]

    score += get_win_score_2(a, b)
    score += get_action_score_2(a, b)

print("score: {}".format(score))

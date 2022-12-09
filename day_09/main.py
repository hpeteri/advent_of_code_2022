#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.


# set working dir to file location
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

f = open("input.txt", "r")
lines = f.read().splitlines()
f.close()


knots = [ [0, 0] for c in range(10)]

for knot in knots:
    print(knot)

visited = {}
visited["0, 0"] = 1

for line in lines:
    line = line.split(' ')
    
    dr = line[0]
    d  = int(line[1])

    print(line)

    for i in range(d):
        
        if dr == 'R':
            knots[0][0] += 1
        elif dr == 'L':
            knots[0][0] -= 1
            
        elif dr == 'U':
            knots[0][1] += 1
                        
        elif dr == 'D':
            knots[0][1] -= 1
                    
        for idx in range(len(knots) - 1):
            knot_0 = knots[idx];
            knot_1 = knots[idx + 1];

            delta_x = abs(knot_0[0] - knot_1[0]);
            delta_y = abs(knot_0[1] - knot_1[1]);
            if delta_x > 1 and delta_y > 1:
                if delta_x == delta_y:
                    # x
                    sign = 0
                    if knot_0[0] > knot_1[0]:
                        sign = 1
                    else:
                        sign = -1
                        
                    knot_1[0] += sign

                    # y
                    sign = 0
                    if knot_0[1] > knot_1[1]:
                        sign = 1
                    else:
                        sign = -1
                        
                    knot_1[1] += sign

                    
                    delta_x = 0
                    delta_y = 0
                    
                elif delta_x > delta_y:
                    delta_x = 0
                else:
                    delta_y = 0
                
            # if we move horizontally, clamp y value to head
            if delta_x > 1:
                sign = 0
                if knot_0[0] > knot_1[0]:
                    sign = 1
                else:
                    sign = -1
                    
                knot_1[0] += sign
                knot_1[1] = knot_0[1]
                move_vertical = 1
            
            # if we move vertically, clamp x value to head
            if delta_y > 1:
                sign = 0
                if knot_0[1] > knot_1[1]:
                    sign = 1
                else:
                    sign = -1
            
                knot_1[0] = knot_0[0]
                knot_1[1] += sign
             
                                
        visited["{}, {}".format(knots[len(knots) - 1][0], knots[len(knots) - 1][1])] = 1

print("visited: ", len(visited))

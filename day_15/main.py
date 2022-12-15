# Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri)
# All rights reserved.

# set working directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

import sys

def manhattan_distance(xy_0, xy_1):
    return abs(xy_0[0] - xy_1[0]) + abs(xy_0[1] - xy_1[1])


with open("input.txt", "r") as f:
    lines = f.read().splitlines()
    f.close()


sensor_beacon_pairs = []

min_x = 9999
min_y = 9999
max_x = -9999
max_y = -9999

for line in lines:
    line = line.split(":")

    sensor = line[0][10:]
    beacon = line[1][22:]
    for c in "xy=":
        sensor = sensor.replace(c, "")
        beacon = beacon.replace(c, "")
        
    sensor = [int(num) for num in sensor.split(",")]
    beacon = [int(num) for num in beacon.split(",")]

    distance = manhattan_distance(sensor, beacon)
    min_x = min(min_x, sensor[0] - distance)
    min_y = min(min_y, sensor[1] - distance)
    max_x = max(max_x, sensor[0] + distance)
    max_y = max(max_y, sensor[1] + distance)

    min_x = min(min_x, beacon[0])
    min_y = min(min_y, beacon[1])
    max_x = max(max_x, beacon[0])
    max_y = max(max_y, beacon[1])
    
    sensor_beacon_pairs.append([sensor, beacon])


def manhattan_distance(xy_0, xy_1):
    return abs(xy_0[0] - xy_1[0]) + abs(xy_0[1] - xy_1[1])

# part 1
"""
wanted_y = 2000000
row = ['.' for c in range(max_x - min_x + 1)]
for sb in sensor_beacon_pairs:    
    sb[0][0] -= min_x
    sb[1][0] -= min_x

for sb in sensor_beacon_pairs:
    sensor = sb[0]
    beacon = sb[1]
    
    distance = manhattan_distance(sensor, beacon)
    
    y = wanted_y
    if sensor[1] == y:
        row[sensor[0]] = "S"
    
    if beacon[1] == y:
        row[beacon[0]] = "B"
    
    for x in range(sensor[0] - distance, sensor[0] + distance):
        
        if x >= len(row):
            continue
        if x < 0:
            continue
        
        if manhattan_distance(sensor, [x, y]) <= distance and row[x] == '.':
            row[x] = "#"
    	
l = "".join(row).replace(".","").replace("B","").replace("S","")
print(f"row: {wanted_y} -> {len(l)}")
"""

# part 2
start = 0
end = 4000000
#end = 20

if max_x - min_x < (end - start):
    print("not large enough")
    max_x = min_x + (end - start)

class XRange:
    start = 0
    end = 0
    def __init__(this, x0, x1):
        this.start = x0
        this.end = x1

    def __str__(this):
        return f"range: {this.start}, {this.end}"

    def __lt__(this, other):
        if this.start == other.start:
            return this.end < other.end
        return this.start < other.start
    
for y in range(end - start):
    ranges = []
    for sb in sensor_beacon_pairs:
        
        sensor = sb[0]
        beacon = sb[1]
	
        distance = manhattan_distance(sensor, beacon)
        if manhattan_distance(sensor, [sensor[0], y]) > distance:
            continue;
        
        y_diff = abs(y - sensor[1])

        p0 = max(sensor[0] - (distance - y_diff), start)
        p1 = min(sensor[0] + (distance - y_diff), end + 1)

        ranges.append(XRange(p0, p1))

    

    
    if len(ranges) == 0:
        continue

    ranges.sort()
    reduced = []

    for r_0 in ranges:
        is_encapsulated = False
        for r_1 in ranges:
            if r_0 == r_1:
                continue

            if r_0.start > r_1.start and r_0.end <= r_1.end:
                is_encapsulated = True
                break

            if r_0.start > r_1.start and r_0.start <= r_1.end:
                r_0.start = r_1.start
                r_0.end = max(r_0.end, r_1.end)
                            
        if is_encapsulated:
            continue

        reduced.append(r_0)

    ranges = reduced
    ranges.sort()

    ranges.append(XRange(end, end))
    for idx, r_0 in enumerate(ranges):
        try:
            r_1 = ranges[idx + 1]
        except:
            break
        
        for other in ranges:
            if other.start > r_0.end and other.start < r_1.start:
                r_1 = other
            
        for x in range(r_0.end + 1, r_1.start):
            print(f"x: {x}, y: {y} -> {x * 4000000 + y}")
            sys.exit()

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

encrypted_nums  = []
decrypted_nums = []

for idx, line in enumerate(lines):
    try:
        num = int(line) * 811589153
        
        encrypted_nums.append([num, idx])
        decrypted_nums.append([num, idx])
    except:
        pass

count = len(decrypted_nums)
print(f"got {count} nums")

for i in range(10):
	for n_idx, n in enumerate(encrypted_nums):
	    
	    steps = n[0]
	    idx_0 = n[1]
	
	    steps = steps % (count - 1)
	
	    if steps < 0:
	        print(n[0])
	        print("mitä vittua")
	        sys.exit()
	        
	    #print(f"move {n[0]}[{idx_0}] -> {steps} ->")
	    
	    for i in range(steps):
	        idx_0 = (idx_0 + 1) % count
	        """
	        if idx_0 == 0:
	            for nn in decrypted_nums[1:-1]: 
	                encrypted_nums[nn[1]][1] += 1
	
	            new_decrypted_nums = []
	            new_decrypted_nums.append(decrypted_nums[0])
	            new_decrypted_nums.append([n[0], n_idx])
	            new_decrypted_nums.extend(decrypted_nums[1:-1])
	            
	            decrypted_nums = new_decrypted_nums
	            encrypted_nums[n_1[1]][1] = 1
	            idx_0 = 1
	            
	        else:
	        """ 
	        n_1 = decrypted_nums[idx_0]
	        encrypted_nums[n_1[1]][1] = (idx_0 + count - 1) % count
	
	        decrypted_nums[(idx_0 + count - 1) % count] = n_1
	        decrypted_nums[idx_0] = [n[0], n_idx]
	        encrypted_nums[n_idx][1] = idx_0
	
	            
	    #arrangement = []
	    #for nn in decrypted_nums:
	    #    arrangement.append(nn[0])
	    #print(arrangement)
        
            
arrangement = []
for nn in decrypted_nums:
    arrangement.append(nn[0])
    
zero_idx = arrangement.index(0)

result = []
result.append(arrangement[(zero_idx + 1000) % count])
result.append(arrangement[(zero_idx + 2000) % count])
result.append(arrangement[(zero_idx + 3000) % count])

print(f"1000th element: {arrangement[(zero_idx + 1000) % count]}")
print(f"2000th element: {arrangement[(zero_idx + 2000) % count]}")
print(f"3000th element: {arrangement[(zero_idx + 3000) % count]}")
print(f"result: {sum(result)}")



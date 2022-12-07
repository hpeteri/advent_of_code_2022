#  Copyright (c) 2022 Henrik Peteri (www.github.com/hpeteri).
#  All rights reserved.

import os
# set working dir to file location
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# globals
dirs = {}
cwd = []

class Directory:
    name = ""
    size = 0
    files = None
    def __init__(self, name):
        self.name = name
        self.files = {}
        
    def __str__(self):
        s = "dir: {}, size: {}, files: {}".format(self.name, self.size, len(self.files))
        s += "\n"
        for f in self.files:
            s += "file: '{} : {}'\n".format(f, self.files[f])
        return s

    def __lt__(self, other):
        return self.size < other.size

def print_dirs():
    print("dirs:")
    for d in dirs:
        print("'{}' : '{}'".format(d, dirs[d]))
    print()

def get_cwd():
    path = "/".join(cwd)
    return path

def get_dir(path):
    if dirs.get(path) == None:
        dirs[path] = Directory(path)

    return dirs.get(path)

def get_dir_size(path):
    d = get_dir(path)
    size = 0
    
    for f in d.files:
        file_size = d.files[f]

        if file_size == -1:
            file_size = get_dir_size(path + "/" + f)
            
            
        size += file_size

    return size


f_handle = open("input.txt", "r")
lines = f_handle.read().splitlines()
f_handle.close()


print_dirs()

def is_command(line):
    return line[0] == '$';

is_ls_output = False

for line in lines:
    if is_command(line):
        is_ls_output = False
        prompt = line.split(' ')
        
        if prompt[1] == "cd":
            # update cwd
            if prompt[2] == '..':
                cwd.pop()
            else:
                cwd.append(prompt[2])

            # create new dir record if not found

            path = get_cwd()
            get_dir(path)
            
        elif prompt[1] == "ls":
            is_ls_output = True
        
    else:
        if is_ls_output:
            prompt = line.split(' ')
            curr_dir = get_dir(get_cwd())
            if prompt[0] == "dir":
                
                cwd.append(prompt[1])
                dr = get_dir(get_cwd())
                cwd.pop()
                
                curr_dir.files[prompt[1]] = -1
            
            else:
                if curr_dir.files.get(prompt[1]) == None:
                    curr_dir.files[prompt[1]] = int(prompt[0])
                    
print_dirs()

by_size = []
for d in dirs:
    dirs[d].size = get_dir_size(d)
    by_size.append(dirs[d])

by_size.sort(reverse=False)

total_size = 0
max_size = 100000

for d in by_size:
    if(d.size > max_size):
        break
    
    total_size += d.size
    
    print("{} -> {}".format(d.name, d.size))
        
    
print("total: ", total_size)

# part 2

disk_space     = 70000000
required_space = 30000000
free_space     = disk_space - dirs["/"].size
to_free        = required_space - free_space

print("disk_space: ", disk_space)
print("required_space: ", required_space)
print("free_space: ", free_space)
print("to_free: ", to_free)

for d in by_size:
    if(d.size > to_free):
        print("dir to free: '{}' with size of '{}'".format(d.name, d.size))
        break
    

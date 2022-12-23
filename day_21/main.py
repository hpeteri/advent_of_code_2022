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

# main
monkeys = {}

class ConstantMonkey:
    def __init__(this, i):
        this.result = i

    def __str__(this):
        return f"{this.result}"

    def try_evaluate(this):
        return True

    def is_evaluated(this):
        if this.result == "x":
            return 2
        return 1

    def evaluate(this):
        return f"{this.result}"

    def get_ast(this):
        return this.result

    def get_ast_text(this):
        return f"{this.result}"

class ExpressionMonkey:

    def __init__(this, a, op, b):
        this.a         = a
        this.b         = b
        this.op        = op
        this.evaluated = 0
        this.result    = None

    def __str__(this):
        return f"{this.a} {this.op} {this.b} -> {this.result}"
    
    def is_evaluated(this):
        return this.evaluated
    
    def evaluate(this):
        return this.result
        
    def try_evaluate(this):
        global monkeys
        
        if not monkeys[this.a].is_evaluated():
            return False

        if not monkeys[this.b].is_evaluated():
            return False

        
        s = f"({monkeys[this.a].evaluate()}{this.op}{monkeys[this.b].evaluate()})"

        try:
            this.result = f"{eval(s)}"
            this.evaluated = 1
        except:
            this.result = s
            this.evaluated = -1
            
        return True

    def get_ast(this):
        global monkeys
        return [monkeys[this.a].get_ast(), this.op, monkeys[this.b].get_ast()]
    
    def get_ast_text(this):
        global monkeys
        if this.is_evaluated() == 1:
            return this.evaluate()
                    
        return f"({monkeys[this.a].get_ast_text()} {this.op} {monkeys[this.b].get_ast_text()})"
    
for line in lines:
    line = line.split(":")
    monkey = line[0]
    op = line[1].strip()

    try:
        i = int(op)
        if monkey != "humn":
            monkeys[monkey] = ConstantMonkey(i)
        else:
            #monkeys[monkey] = ConstantMonkey(3910938071092.0)
            monkeys[monkey] = ConstantMonkey("x")
    except:
        abc = op.split(" ")
        if monkey != "root":
            monkeys[monkey] = ExpressionMonkey(abc[0], abc[1], abc[2])
        else:
            monkeys[monkey] = ExpressionMonkey(abc[0], "==", abc[2])
    
to_evaluate = []
for m in monkeys:
    to_evaluate.append(m)

while len(to_evaluate):
    m = to_evaluate.pop()
    monkey = monkeys[m]
    if not monkey.try_evaluate():
        to_evaluate.insert(0, m)
    

root_monkey = monkeys['root']
print(root_monkey.get_ast_text())

ast_0 = root_monkey.get_ast_text()
ast_1 = root_monkey.get_ast()

if root_monkey.is_evaluated() == 1:
    sys.exit()

simplified = ""
other = ""
at = root_monkey
def get_inverse_op(op):
    if op == "==":
        return None

    if op == "+":
        return "-"

    if op == "-":
        return "+"

    if op == "*":
        return "/"
    
    if op == "/":
        return "*"

    print("???")
    sys.exit()

while 1:
    try:
        a = monkeys[at.a]
        b = monkeys[at.b]
    except:
        break
        
    if a.is_evaluated() == 1:
        ast = a.get_ast_text()
        inverse_op = get_inverse_op(at.op)
        if not inverse_op:
            simplified = f"{a.get_ast_text()}"
            other =  f"{b.get_ast_text()}"
        else:
            if inverse_op == "*":
                other      = f"({a.get_ast_text()} / {simplified})"
                simplified = f"({a.get_ast_text()} / {simplified})"
            elif inverse_op == "+":
                other      = f"- ({simplified}  - {a.get_ast_text()})"
                simplified = f"- (({simplified} - {a.get_ast_text()}))"
            else:
                other      = f"{simplified} {inverse_op} {a.get_ast_text()}"
                simplified = f"({simplified} {inverse_op} {a.get_ast_text()})"

        at = b
        
    elif b.is_evaluated() == 1:
        ast = a.get_ast_text()
        inverse_op = get_inverse_op(at.op)
        # here we can use the inverse op
        if not inverse_op:
            simplified = f"{b.get_ast_text()}"
            other =  f"{a.get_ast_text()}"
        else:
            other = f"{simplified} {inverse_op} {b.get_ast_text()}"
            simplified = f"({simplified} {inverse_op} {b.get_ast_text()})"
            
        at = a
            
    try:
        simplified = eval(simplified)
        print(f"{other} == {simplified}")
    except Exception as e:
        print()
        print(f"{other} == {simplified}")
        sys.exit()
    
print(simplified)

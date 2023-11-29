import argparse
from time import time
import json
import math
import re

DAY = 5

PUZZLE_TEXT = '''
--- Day 5: Supply Stacks ---
--- Part One ---

The expedition can depart as soon as the final supplies have been unloaded from the 
ships. Supplies are stored in stacks of marked crates, but because the needed 
supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure 
none of the crates get crushed or fall over, the crane operator will rearrange them 
in a series of carefully-planned steps. After the crates are rearranged, the desired 
crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, 
but they forgot to ask her which crate will end up where, and they want to be ready 
to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the 
rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. 
Stack 1 contains two crates: 
crate Z is on the bottom, and crate N is on top. 
Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. 
Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a 
quantity of crates is moved from one stack to a different stack. In the first step 
of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, 
resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved 
one at a time, so the first crate to be moved (D) ends up below the second and third 
crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved 
one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this 
example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you 
should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
'''

SAMPLE_INPUT = '''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''

PUZZLE_INPUT = '''
                [B]     [L]     [S]
        [Q] [J] [C]     [W]     [F]
    [F] [T] [B] [D]     [P]     [P]
    [S] [J] [Z] [T]     [B] [C] [H]
    [L] [H] [H] [Z] [G] [Z] [G] [R]
[R] [H] [D] [R] [F] [C] [V] [Q] [T]
[C] [J] [M] [G] [P] [H] [N] [J] [D]
[H] [B] [R] [S] [R] [T] [S] [R] [L]
 1   2   3   4   5   6   7   8   9 

move 8 from 7 to 1
move 9 from 1 to 9
move 4 from 5 to 4
move 4 from 6 to 1
move 3 from 8 to 5
move 6 from 5 to 9
move 1 from 5 to 1
move 4 from 4 to 9
move 7 from 3 to 7
move 6 from 7 to 3
move 1 from 8 to 7
move 2 from 7 to 6
move 1 from 8 to 9
move 1 from 6 to 3
move 4 from 3 to 5
move 5 from 1 to 3
move 1 from 1 to 8
move 2 from 3 to 4
move 1 from 4 to 1
move 7 from 9 to 2
move 1 from 6 to 3
move 2 from 1 to 9
move 20 from 9 to 7
move 6 from 4 to 9
move 1 from 2 to 9
move 6 from 9 to 4
move 1 from 4 to 6
move 1 from 8 to 6
move 1 from 4 to 7
move 5 from 2 to 3
move 2 from 6 to 4
move 3 from 9 to 5
move 5 from 3 to 5
move 3 from 3 to 8
move 3 from 5 to 6
move 1 from 9 to 8
move 5 from 4 to 5
move 3 from 4 to 9
move 1 from 8 to 2
move 2 from 8 to 2
move 11 from 5 to 6
move 16 from 7 to 1
move 2 from 1 to 7
move 14 from 6 to 1
move 11 from 1 to 6
move 2 from 1 to 4
move 4 from 3 to 4
move 9 from 2 to 4
move 2 from 4 to 8
move 2 from 5 to 3
move 9 from 4 to 7
move 2 from 3 to 2
move 1 from 2 to 7
move 1 from 8 to 4
move 4 from 1 to 4
move 1 from 9 to 1
move 7 from 4 to 7
move 2 from 6 to 5
move 1 from 8 to 6
move 1 from 4 to 2
move 10 from 1 to 6
move 5 from 7 to 3
move 1 from 4 to 7
move 2 from 1 to 2
move 2 from 2 to 4
move 4 from 3 to 4
move 18 from 7 to 6
move 6 from 6 to 4
move 1 from 7 to 4
move 1 from 7 to 6
move 11 from 4 to 5
move 14 from 5 to 9
move 1 from 8 to 7
move 8 from 6 to 2
move 2 from 4 to 5
move 7 from 9 to 1
move 6 from 9 to 7
move 5 from 1 to 8
move 1 from 3 to 6
move 10 from 6 to 3
move 1 from 9 to 6
move 1 from 5 to 4
move 4 from 3 to 8
move 1 from 5 to 9
move 9 from 2 to 3
move 1 from 9 to 5
move 4 from 8 to 4
move 1 from 5 to 3
move 5 from 8 to 7
move 5 from 7 to 2
move 3 from 4 to 1
move 8 from 6 to 5
move 1 from 7 to 9
move 4 from 1 to 3
move 2 from 4 to 6
move 5 from 5 to 2
move 4 from 6 to 9
move 1 from 1 to 2
move 1 from 5 to 6
move 7 from 2 to 8
move 5 from 6 to 8
move 4 from 7 to 9
move 15 from 3 to 9
move 1 from 7 to 3
move 1 from 5 to 3
move 6 from 2 to 6
move 1 from 5 to 2
move 2 from 3 to 9
move 1 from 6 to 8
move 5 from 8 to 9
move 2 from 3 to 8
move 3 from 3 to 6
move 11 from 9 to 4
move 1 from 2 to 1
move 2 from 8 to 4
move 1 from 1 to 4
move 7 from 4 to 7
move 9 from 6 to 3
move 4 from 7 to 8
move 4 from 7 to 6
move 19 from 9 to 4
move 7 from 8 to 5
move 5 from 3 to 6
move 6 from 6 to 9
move 3 from 3 to 5
move 1 from 3 to 9
move 8 from 4 to 5
move 2 from 9 to 6
move 3 from 8 to 2
move 1 from 8 to 4
move 1 from 2 to 5
move 19 from 4 to 1
move 2 from 5 to 7
move 2 from 2 to 4
move 13 from 5 to 2
move 1 from 5 to 1
move 2 from 6 to 9
move 1 from 8 to 7
move 9 from 9 to 3
move 2 from 3 to 8
move 1 from 4 to 2
move 5 from 6 to 7
move 1 from 4 to 6
move 2 from 8 to 7
move 7 from 1 to 5
move 1 from 6 to 7
move 10 from 1 to 8
move 1 from 1 to 3
move 1 from 1 to 2
move 6 from 5 to 3
move 4 from 5 to 3
move 5 from 7 to 1
move 3 from 1 to 2
move 4 from 7 to 5
move 8 from 3 to 6
move 2 from 1 to 7
move 4 from 5 to 8
move 7 from 3 to 5
move 3 from 7 to 2
move 1 from 7 to 3
move 12 from 2 to 8
move 23 from 8 to 2
move 16 from 2 to 6
move 1 from 9 to 6
move 7 from 5 to 7
move 7 from 2 to 4
move 2 from 3 to 8
move 1 from 1 to 9
move 5 from 8 to 1
move 2 from 3 to 9
move 2 from 7 to 1
move 4 from 1 to 3
move 4 from 7 to 2
move 2 from 1 to 4
move 11 from 2 to 9
move 3 from 3 to 4
move 1 from 9 to 1
move 2 from 2 to 7
move 4 from 4 to 8
move 2 from 9 to 5
move 2 from 5 to 7
move 4 from 4 to 6
move 1 from 3 to 8
move 1 from 9 to 8
move 4 from 4 to 2
move 2 from 1 to 3
move 1 from 8 to 4
move 2 from 3 to 5
move 3 from 9 to 7
move 2 from 8 to 9
move 1 from 9 to 6
move 2 from 7 to 3
move 2 from 8 to 1
move 1 from 4 to 9
move 18 from 6 to 2
move 1 from 6 to 5
move 1 from 5 to 9
move 18 from 2 to 3
move 1 from 8 to 7
move 2 from 5 to 9
move 1 from 1 to 4
move 3 from 2 to 1
move 9 from 9 to 4
move 7 from 4 to 6
move 2 from 7 to 3
move 2 from 4 to 9
move 7 from 6 to 7
move 3 from 7 to 2
move 7 from 6 to 3
move 2 from 6 to 9
move 24 from 3 to 9
move 2 from 6 to 8
move 1 from 4 to 2
move 2 from 8 to 5
move 31 from 9 to 3
move 6 from 7 to 4
move 35 from 3 to 7
move 1 from 1 to 8
move 1 from 5 to 7
move 1 from 5 to 4
move 1 from 3 to 9
move 1 from 8 to 2
move 3 from 1 to 7
move 7 from 4 to 5
move 1 from 9 to 8
move 4 from 5 to 6
move 2 from 5 to 2
move 6 from 2 to 5
move 2 from 5 to 7
move 2 from 2 to 1
move 2 from 5 to 4
move 1 from 8 to 4
move 3 from 4 to 6
move 4 from 6 to 7
move 1 from 5 to 2
move 2 from 6 to 9
move 1 from 6 to 4
move 1 from 4 to 8
move 2 from 9 to 6
move 1 from 8 to 9
move 34 from 7 to 9
move 6 from 7 to 3
move 1 from 7 to 2
move 1 from 5 to 8
move 1 from 8 to 6
move 6 from 7 to 4
move 1 from 7 to 3
move 7 from 3 to 5
move 6 from 4 to 6
move 31 from 9 to 1
move 3 from 5 to 7
move 24 from 1 to 3
move 1 from 2 to 4
move 3 from 9 to 1
move 14 from 3 to 5
move 1 from 4 to 3
move 1 from 9 to 7
move 8 from 3 to 7
move 1 from 2 to 9
move 7 from 1 to 5
move 3 from 6 to 8
move 3 from 6 to 1
move 1 from 1 to 3
move 4 from 3 to 2
move 4 from 2 to 3
move 2 from 5 to 1
move 9 from 7 to 4
move 1 from 6 to 5
move 1 from 1 to 7
move 3 from 8 to 9
move 5 from 4 to 2
move 3 from 2 to 3
move 1 from 2 to 3
move 2 from 4 to 1
move 2 from 9 to 4
move 1 from 9 to 3
move 1 from 6 to 1
move 1 from 9 to 6
move 25 from 5 to 4
move 4 from 1 to 9
move 2 from 3 to 7
move 2 from 6 to 9
move 2 from 9 to 5
move 6 from 7 to 1
move 5 from 3 to 6
move 10 from 4 to 3
move 10 from 4 to 8
move 2 from 4 to 2
move 5 from 1 to 9
move 2 from 6 to 4
move 6 from 9 to 6
move 7 from 6 to 4
move 3 from 9 to 4
move 3 from 2 to 4
move 4 from 3 to 8
move 2 from 5 to 3
move 10 from 4 to 9
move 4 from 9 to 7
move 5 from 9 to 5
move 4 from 5 to 1
move 9 from 4 to 6
move 10 from 1 to 3
move 1 from 5 to 4
move 3 from 4 to 5
move 2 from 5 to 7
move 1 from 7 to 3
move 1 from 6 to 9
move 11 from 8 to 6
move 14 from 6 to 5
move 1 from 4 to 7
move 7 from 5 to 3
move 3 from 5 to 4
move 2 from 9 to 5
move 2 from 4 to 3
move 2 from 7 to 4
move 11 from 3 to 9
move 2 from 8 to 2
move 2 from 2 to 3
move 1 from 8 to 2
move 1 from 2 to 9
move 3 from 4 to 5
move 2 from 6 to 9
move 1 from 1 to 8
move 10 from 9 to 7
move 2 from 9 to 3
move 23 from 3 to 9
move 4 from 6 to 4
move 9 from 5 to 6
move 1 from 5 to 3
move 5 from 6 to 7
move 1 from 1 to 7
move 1 from 3 to 9
move 4 from 6 to 7
move 1 from 8 to 7
move 1 from 7 to 5
move 1 from 5 to 1
move 12 from 7 to 6
move 9 from 9 to 3
move 6 from 6 to 4
move 8 from 7 to 3
move 3 from 7 to 4
move 6 from 3 to 1
move 10 from 4 to 8
move 10 from 8 to 7
move 2 from 3 to 7
move 9 from 3 to 8
move 2 from 6 to 3
move 10 from 7 to 1
move 3 from 4 to 6
move 5 from 8 to 5
move 3 from 5 to 7
move 1 from 3 to 2
move 1 from 2 to 6
move 6 from 9 to 1
move 12 from 1 to 3
move 3 from 6 to 9
move 3 from 1 to 7
move 1 from 3 to 2
move 7 from 1 to 7
move 1 from 2 to 7
move 2 from 6 to 4
move 1 from 4 to 5
move 3 from 8 to 7
move 2 from 6 to 3
move 2 from 6 to 1
move 1 from 3 to 8
move 5 from 3 to 4
move 2 from 8 to 5
move 14 from 7 to 4
move 1 from 3 to 2
move 1 from 3 to 7
move 7 from 7 to 4
move 2 from 5 to 3
move 2 from 1 to 4
move 9 from 4 to 6
move 1 from 1 to 2
move 4 from 9 to 4
move 8 from 9 to 3
move 2 from 2 to 7
move 13 from 4 to 8
move 4 from 4 to 1
move 2 from 7 to 6
move 12 from 3 to 2
move 11 from 2 to 9
move 6 from 4 to 9
move 18 from 9 to 4
move 2 from 1 to 6
move 6 from 8 to 1
move 13 from 6 to 5
move 8 from 4 to 5
move 1 from 2 to 9
move 8 from 1 to 4
move 7 from 4 to 8
move 4 from 3 to 5
move 10 from 8 to 5
move 13 from 5 to 8
move 12 from 4 to 5
move 2 from 9 to 8
move 29 from 5 to 9
move 24 from 9 to 2
move 23 from 2 to 4
move 5 from 9 to 2
move 7 from 5 to 7
move 1 from 5 to 1
move 7 from 4 to 8
move 14 from 8 to 1
move 5 from 2 to 6
move 16 from 4 to 7
move 8 from 1 to 6
move 1 from 2 to 8
move 20 from 7 to 6
move 11 from 6 to 4
move 3 from 1 to 5
move 3 from 4 to 3
move 8 from 4 to 9
move 8 from 6 to 1
move 2 from 1 to 4
move 3 from 5 to 2
move 12 from 8 to 2
move 1 from 7 to 1
move 1 from 3 to 5
move 1 from 7 to 8
move 1 from 7 to 3
move 12 from 2 to 8
move 13 from 6 to 4
move 2 from 1 to 9
move 3 from 2 to 6
move 3 from 9 to 7
move 5 from 9 to 1
move 4 from 6 to 4
move 2 from 3 to 6
move 1 from 5 to 9
move 1 from 6 to 7
move 9 from 1 to 5
move 11 from 8 to 3
move 1 from 6 to 8
move 3 from 7 to 1
move 1 from 8 to 7
move 2 from 8 to 9
move 7 from 1 to 2
move 17 from 4 to 7
move 1 from 8 to 6
move 4 from 7 to 2
move 4 from 9 to 7
move 4 from 2 to 3
move 1 from 1 to 4
move 2 from 4 to 3
move 9 from 5 to 4
move 1 from 6 to 8
move 6 from 2 to 1
move 5 from 1 to 9
move 9 from 4 to 3
move 1 from 4 to 6
move 2 from 9 to 7
move 1 from 1 to 5
move 1 from 2 to 7
move 1 from 8 to 9
move 1 from 6 to 8
move 1 from 5 to 4
move 1 from 8 to 7
move 23 from 3 to 7
move 36 from 7 to 6
move 33 from 6 to 1
move 1 from 4 to 8
move 7 from 1 to 5
move 1 from 8 to 1
move 3 from 7 to 2
move 24 from 1 to 3
move 7 from 7 to 3
move 3 from 5 to 1
move 4 from 5 to 3
move 1 from 9 to 8
move 2 from 9 to 6
move 1 from 8 to 5
move 3 from 2 to 5
move 30 from 3 to 5
move 1 from 6 to 7
move 6 from 1 to 8
move 7 from 3 to 2
move 1 from 7 to 5
move 2 from 3 to 2
move 2 from 6 to 8
move 1 from 6 to 1
move 7 from 5 to 8
move 8 from 8 to 7
move 20 from 5 to 8
move 2 from 9 to 7
move 8 from 2 to 1
move 7 from 7 to 3
move 1 from 2 to 1
move 3 from 7 to 9
move 4 from 8 to 3
move 5 from 5 to 6
move 1 from 5 to 9
move 4 from 9 to 4
move 1 from 5 to 9
move 2 from 3 to 6
move 1 from 5 to 8
move 7 from 6 to 3
move 1 from 4 to 1
move 7 from 3 to 2
move 3 from 3 to 5
move 2 from 4 to 7
'''

P1_SAMPLE_SOLUTION = 'CMZ'

P2_SAMPLE_SOLUTION = 'MCD'

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def part_one(input_text=SAMPLE_INPUT):
    input_list = input_text.split('\n')
    moves = list()
    clean_crates = list()
    stacks = [ None ]
    for item in input_list:
        if 'move' in item:
            moves.append(item)
        if '[' in item:
            this_row = re.findall('\[.\]',item.replace('    ',' [ ]').replace('][','] ['))
            this_row = [ crate[1] for crate in this_row ]
            clean_crates.append(this_row)
            
    for i in range(0,len(clean_crates[0])):
        stacks.append([])
            
    for row in clean_crates:
        for pos in range(0,len(row)):
            if row[pos] != ' ':
                stacks[pos+1].append(row[pos])
            
    for move in moves:
        this_move = move.split()
        how_many = int(this_move[1])
        move_from = int(this_move[3])
        move_to = int(this_move[5])
        for crate in range(0,how_many):
            try:
                stacks[move_to].insert(0,stacks[move_from].pop(0))                
            except:
                continue
            
    message = ""
    for stack in stacks:
        if type(stack) == list:
            message += stack[0]    
    
    return message

def part_two(input_text=SAMPLE_INPUT):
    input_list = input_text.split('\n')
    moves = list()
    clean_crates = list()
    stacks = [ None ]
    for item in input_list:
        if 'move' in item:
            moves.append(item)
        if '[' in item:
            this_row = re.findall('\[.\]',item.replace('    ',' [ ]').replace('][','] ['))
            this_row = [ crate[1] for crate in this_row ]
            clean_crates.append(this_row)
            
    for i in range(0,len(clean_crates[0])):
        stacks.append([])
            
    for row in clean_crates:
        for pos in range(0,len(row)):
            if row[pos] != ' ':
                stacks[pos+1].append(row[pos])
            
    for move in moves:
        this_move = move.split()
        how_many = int(this_move[1])
        move_from = int(this_move[3])
        move_to = int(this_move[5])
        moving = stacks[move_from][0:how_many]
        stacks[move_from] = stacks[move_from][how_many:]
        stacks[move_to] = moving+stacks[move_to]
            
    message = ""
    for stack in stacks:
        if type(stack) == list:
            message += stack[0]    
    
    return message
        
def main():
    parser = argparse.ArgumentParser(description=f'AOC2022 Puzzle Day { DAY }')
    parser.add_argument("-p", "--showpuzzle", help="Display Puzzle Text", action='store_true')
    parser.add_argument("-s", "--showsample", help="Display Sample Input", action='store_true')
    args = parser.parse_args()
    
    if args.showpuzzle:
        print(f"###############\nAOC 2022 DAY {DAY} PUZZLE TEXT\n###############")
        print(PUZZLE_TEXT)
    
    if args.showsample:
        print(f"###############\nAOC 2022 DAY {DAY} SAMPLE INPUT\n###############")
        print(SAMPLE_INPUT.strip())
        print(f"\n###############\nAOC 2022 DAY {DAY} P1 SAMPLE SOLUTION\n###############")
        print(P1_SAMPLE_SOLUTION)
        print(f"\n###############\nAOC 2022 DAY {DAY} P2 SAMPLE SOLUTION\n###############")
        print(P2_SAMPLE_SOLUTION)


    if P1_SAMPLE_SOLUTION:            
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        solution_output = part_one()
        if P1_SAMPLE_SOLUTION == solution_output:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {solution_output}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {part_one(PUZZLE_INPUT)}')
            print(f"Elapsed time {elapsed_time(start_time)}")
        
    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...\n")
        start_time = time()
        solution_output = part_two()
        if P2_SAMPLE_SOLUTION == solution_output:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {solution_output}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {part_two(PUZZLE_INPUT)}')
            print(f"Elapsed time {elapsed_time(start_time)}")
    
if __name__ == "__main__":
    main()
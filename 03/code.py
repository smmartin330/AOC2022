import argparse
from time import time
import json
import math

DAY = 3

PUZZLE_TEXT = '''
--- Part One ---

One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, 
that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two 
compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your 
help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A 
refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same 
number of items in each of its two compartments, so the first half of the characters represent items in the first 
compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

 - The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items 
vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both 
compartments is lowercase p.
- The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in 
both compartments is uppercase L.
- The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
- The fourth rucksack's compartments only share item type v.
- The fifth rucksack's compartments only share item type t.
- The sixth rucksack's compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 
42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?

--- Part Two ---

As you finish identifying the misplaced items, the Elves come to you with another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For efficiency, 
within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is 
item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying 
any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be 
pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right 
one is by finding the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type. So, in the 
above example, the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg

And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. In the second group, 
their badge item type must be Z.

Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for the first group and 52 
(Z) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
'''

SAMPLE_INPUT = '''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''

P1_SAMPLE_SOLUTION = 157

P2_SAMPLE_SOLUTION = 70

PRIORITIES = [ None, "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]

class Rucksack():
    def __init__(self,contents):
        self.contents = [ contents[0:len(contents)//2], contents[len(contents)//2:len(contents)] ]
        self.both = { item for item in self.contents[0] if item in self.contents[1] }
        self.carried = { item for item in contents }
        self.priority_both = 0
        for item in self.both:
            self.priority_both += PRIORITIES.index(item)

class Group():
    def __init__(self,rucksacks):
        self.rucksacks = rucksacks
        self.all_carried_items = set()
        for rucksack in self.rucksacks:
            self.all_carried_items = self.all_carried_items.union(rucksack.carried)
        self.carried_by_all = [ item for item in self.all_carried_items if (item in self.rucksacks[0].carried) and (item in self.rucksacks[1].carried) and (item in self.rucksacks[2].carried) ]

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def part_one(input_text=SAMPLE_INPUT):
    input_list = input_text.strip().split('\n')
    rucksacks = [ ]
    priority_sum = 0
    for row in input_list:
        rucksacks.append(Rucksack(row))
        priority_sum += rucksacks[-1].priority_both
    return priority_sum

def part_two(input_text=SAMPLE_INPUT):
    input_list = input_text.strip().split('\n')
    rucksacks = [ ]
    groups = [ ]
    total_badge_priority = 0
    for row in input_list:
        rucksacks.append(Rucksack(row))
        if len(rucksacks) % 3 == 0:
            groups.append(Group(rucksacks[-3:]))
            total_badge_priority += PRIORITIES.index(groups[-1].carried_by_all[0])
            
    return total_badge_priority
        

def main():
    parser = argparse.ArgumentParser(description=f'AOC2022 Puzzle Day { DAY }')
    parser.add_argument("-p", "--showpuzzle", help="Display Puzzle Text", action='store_true')
    parser.add_argument("-s", "--showsample", help="Display Sample Input", action='store_true')
    parser.add_argument("-i", "--inputfile", help="Puzzle Input", type=str)
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
    
    if args.inputfile:        
        try:
            my_input = ""
            with open(args.inputfile, 'r') as file:
                while (line := file.readline()):
                    my_input += line            
        except FileNotFoundError:
            print("Specified input file not found.")
            quit()

    if P1_SAMPLE_SOLUTION:            
        print("PART 1\nTesting Sample...")
        start_time = time()
        solution_output = part_one()
        if P1_SAMPLE_SOLUTION == solution_output:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {solution_output}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if args.inputfile:
            print("Processing Input...")
            start_time = time()
            print(f'SOLUTION: {part_one(my_input)}')
            print(f"Elapsed time {elapsed_time(start_time)}")
        
    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...")
        start_time = time()
        solution_output = part_two()
        if P2_SAMPLE_SOLUTION == solution_output:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {solution_output}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if args.inputfile:
            print("Processing Input...")
            start_time = time()
            print(f'SOLUTION: {part_two(my_input)}')
            print(f"Elapsed time {elapsed_time(start_time)}")
    
if __name__ == "__main__":
    main()
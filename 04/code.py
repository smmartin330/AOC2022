import argparse
from time import time
import json
import math

DAY = 4

PUZZLE_TEXT = '''
--- Day 4: Camp Cleanup ---
--- Part One ---

Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been 
assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is 
assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of 
the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make 
a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:
 - Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second 
Elf was assigned sections 6-8 (sections 6, 7, 8).
 - The Elves in the second pair were each assigned two sections.
 - The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also 
got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger 
numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8

Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully 
contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf 
in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the 
most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?

---Part Two---
--- Part Two ---

It seems like there is still quite a bit of duplicate work planned. 
Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't 
overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

5-7,7-9 overlaps in a single section, 7.
2-8,3-7 overlaps all of the sections 3 through 7.
6-6,4-6 overlaps in a single section, 6.
2-6,4-8 overlaps in sections 4, 5, and 6.
So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?
'''

SAMPLE_INPUT = '''
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''

P1_SAMPLE_SOLUTION = 2

P2_SAMPLE_SOLUTION = 4

class Pair():
    def __init__(self,pair):
        self.pair = pair.split(',') # [ '2-8', '3-7' ]
        self.first = [ int(item) for item in self.pair[0].split('-') ] # [ '2', '8' ]
        self.second = [ int(item) for item in self.pair[1].split('-') ]
        self.assignments = [ list(range(self.first[0],self.first[1]+1)), list(range(self.second[0],self.second[1]+1)) ]
        self.assignments_overlap_completely = all(item in self.assignments[0] for item in self.assignments[1]) or all(item in self.assignments[1] for item in self.assignments[0])
        self.assignments_overlap_partially = any(item in self.assignments[0] for item in self.assignments[1]) or any(item in self.assignments[1] for item in self.assignments[0])

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def part_one(input_text=SAMPLE_INPUT):
    input_list = input_text.strip().split('\n')
    pairs = list()
    overlap_count = 0
    for row in input_list:
        pairs.append(Pair(row))
        overlap_count += int(pairs[-1].assignments_overlap_completely)
    
    return overlap_count
        

def part_two(input_text=SAMPLE_INPUT):
    input_list = input_text.strip().split('\n')
    pairs = list()
    overlap_count = 0
    for row in input_list:
        pairs.append(Pair(row))
        overlap_count += int(pairs[-1].assignments_overlap_partially)
    
    return overlap_count 
        

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
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        solution_output = part_one()
        if P1_SAMPLE_SOLUTION == solution_output:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {solution_output}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if args.inputfile:
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {part_one(my_input)}')
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
        if args.inputfile:
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {part_two(my_input)}')
            print(f"Elapsed time {elapsed_time(start_time)}")
    
if __name__ == "__main__":
    main()
import argparse
from time import time
import json
import math

DAY = 1

PUZZLE_TEXT = '''
https://adventofcode.com/2022/day/1

--- Day 1: Calorie Counting ---

Santa's reindeer typically eat regular reindeer food, but they need a lot of magical 
energy to deliver presents on Christmas. For that, their favorite snack is a special 
type of star fruit that only grows deep in the jungle. The Elves have brought you on 
their annual expedition to the grove where the fruit grows.

To supply enough magical energy, the expedition needs to retrieve a minimum of fifty 
stars by December 25th. Although the Elves assure you that the grove has plenty of 
fruit, you decide to grab any fruit you see along the way, just in case.

Collect stars by solving puzzles. Two puzzles will be made available on each day in 
the Advent calendar; the second puzzle is unlocked when you complete the first. Each 
puzzle grants one star. Good luck!

The jungle must be too overgrown and difficult to navigate in vehicles or access from 
the air; the Elves' expedition traditionally goes on foot. As your boats approach 
land, the Elves begin taking inventory of their supplies. One important consideration 
is food - in particular, the number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by the various meals, 
snacks, rations, etc. that they've brought with them, one item per line. Each Elf 
separates their own inventory from the previous Elf's inventory (if any) by a blank line.

For example, suppose the Elves finish writing their items' Calories and end up with the 
following list:

1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
This list represents the Calories of the food carried by five Elves:

The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 
Calories.
The second Elf is carrying one food item with 4000 Calories.
The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 
Calories.
The fifth Elf is carrying one food item with 10000 Calories.

In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: 
they'd like to know how many Calories are being carried by the Elf carrying the most 
Calories. In the example above, this is 24000 (carried by the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
'''

SAMPLE_INPUT = '''
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''

P1_SAMPLE_SOLUTION = 24000

P2_SAMPLE_SOLUTION = 45000

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def part_one(input_text=SAMPLE_INPUT):
    input_list = input_text.lstrip().rstrip().split('\n')
    
    calories_per_elf = { }
    
    calories = 0
    highest_calorie_count = {"elf": 0, "calories": 0}
    for row in input_list:
        try:
            calories += int(row)
        except ValueError:
            calories_per_elf[len(calories_per_elf)] = calories
            if calories > highest_calorie_count["calories"]:
                highest_calorie_count = {"elf": len(calories_per_elf), "calories": calories}
            calories = 0
    
    return int(highest_calorie_count["calories"])

def part_two(input_text=SAMPLE_INPUT):
    input_list = input_text.lstrip().rstrip().split('\n')
    
    calories_per_elf = []
    calories = 0
    for row in input_list:
        try:
            calories += int(row)
        except ValueError:
            calories_per_elf.append(calories)
            calories = 0
    
    calories_per_elf.append(calories)
    
    calories_per_elf.sort()
    
    top_three = calories_per_elf.pop() + calories_per_elf.pop() + calories_per_elf.pop()
    
    return top_three
        

def main():
    parser = argparse.ArgumentParser(description=f'AOC2022 Puzzle Day { DAY }')
    parser.add_argument("-p", "--showpuzzle", help="Display Puzzle Text", action='store_true')
    parser.add_argument("-s", "--showsample", help="Display Sample Input", action='store_true')
    parser.add_argument("-t", "--testsample", help="Test Sample Input", action='store_true')
    parser.add_argument("-i", "--inputfile", help="Puzzle Input", type=str)
    args = parser.parse_args()
    
    if args.showpuzzle:
        print(f"###############\nAOC 2022 DAY {DAY} PUZZLE TEXT\n###############")
        print(PUZZLE_TEXT)
    
    if args.showsample:
        print(f"###############\nAOC 2022 DAY {DAY} SAMPLE INPUT\n###############")
        print(SAMPLE_INPUT.lstrip())
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
import argparse
from time import time
import json
import math

DAY = 0

PUZZLE_TEXT = '''
'''

SAMPLE_INPUT = '''
'''

P1_SAMPLE_SOLUTION = False

P2_SAMPLE_SOLUTION = False

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def part_one(input_text=SAMPLE_INPUT):
    input_list = input_text.lstrip().rstrip().split('\n')
    
    return 

def part_two(input_text=SAMPLE_INPUT):
    input_list = input_text.lstrip().rstrip().split('\n')
        
    return
        

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
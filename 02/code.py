import argparse
from time import time
import json
import math

DAY = 2

PUZZLE_TEXT = '''
https://adventofcode.com/2022/day/2

--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage,
 a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the
players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner 
for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If 
both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) 
that they say will be sure to help you win. "The first column is what your opponent is going to play: A 
for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help 
with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z 
for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of 
your scores for each round. The score for a single round is the score for the shape you selected (1 for 
Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if 
the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you 
would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win
for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a 
loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?
'''

SAMPLE_INPUT = '''
A Y
B X
C Z
'''

P1_SAMPLE_SOLUTION = 15

P2_SAMPLE_SOLUTION = 12

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def part_one(input_text=SAMPLE_INPUT):
    input_list = input_text.strip().split('\n')

    winning_conditions = [ "A Y", "B Z", "C X"]
    losing_conditions = [ "A Z", "B X", "C Y"]
    points = { "X": 1, "Y": 2, "Z": 3 }
    score = 0
    for line in input_list:
        if line in winning_conditions:
            score += 6 + points[line[-1]]
        elif line in losing_conditions:
            score += 0 + points[line[-1]]
        else:
            score += 3 + points[line[-1]]            

    return score

def part_two(input_text=SAMPLE_INPUT):
    input_text = input_text.replace("A","0").replace("B","1").replace("C","2").replace("X","-1").replace("Y","0").replace("Z","1")
    input_list = input_text.strip().split('\n')
    total_score = 0
    
    for line in input_list:
        line = line.split()
        their_play = int(line[0])
        result = int(line[-1])
        my_play = list(range(0,3))[(their_play + result) % 3]
        points = lambda y : (3*y) + 3
        total_score += (my_play + 1) + points(result)
    
    return total_score
        

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
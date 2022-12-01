import argparse
import time

DAY = 0

PUZZLE = '''

'''

SAMPLE = '''

'''

SAMPLE_SOLUTION = ""

def main():
    parser = argparse.ArgumentParser(description=f'AOC2022 Puzzle Day { DAY }')
    parser.add_argument("input", type=str, help="Puzzle Input")
    args = parser.parse_args()
    
    try:
        file = open(args.input, 'r')
    except FileNotFoundError:
        print("File not found.")
        quit()
    

if __name__ == "__main__":
    main()

import argparse
from time import time
import json
import math

DAY = 15

PUZZLE_TEXT = """
--- Day 15: Beacon Exclusion Zone ---

You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels. You don't have time to search them all, but you don't need to: your pack contains a set of deployable sensors that you imagine were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the source of the distress signal to use them. You pull the emergency sensor system out of your pack, hit the big button on top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins monitoring for the nearest signal source beacon. Sensors and beacons always exist at integer coordinates. Each sensor knows its own position and can determine the position of a beacon precisely; however, sensors can only lock on to the one beacon closest to the sensor as measured by the Manhattan distance. (There is never a tie where two beacons are the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input). For example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the sensor at 9,16, the closest beacon to it is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This isn't necessarily a comprehensive map of all beacons in the area, though. Because each sensor only identifies its closest beacon, if a sensor detects a beacon, you know there are no other beacons that close or closer to that sensor. There could still be beacons that just happen to not be the closest beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This sensor's closest beacon is at 2,10, and so you know there are no beacons that close or closer (in any positions marked #).

None of the detected beacons seem to be producing the distress signal, so you'll need to work out where the distress beacon is by working out where it isn't. For now, keep things simple by counting the positions where a beacon cannot possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the example above and, just in the row where y=10, you'd like to count the number of positions a beacon cannot possibly exist. The coverage from all sensors near that row looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.
In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.

Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a beacon?
"""

SAMPLE_INPUT = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

PUZZLE_INPUT = """
Sensor at x=155404, y=2736782: closest beacon is at x=2062250, y=2735130
Sensor at x=2209843, y=541855: closest beacon is at x=2159715, y=2000000
Sensor at x=3437506, y=3046523: closest beacon is at x=3174767, y=2783059
Sensor at x=925392, y=1508378: closest beacon is at x=941123, y=1223290
Sensor at x=2349988, y=3272812: closest beacon is at x=1912017, y=3034331
Sensor at x=292610, y=374034: closest beacon is at x=941123, y=1223290
Sensor at x=2801735, y=1324309: closest beacon is at x=2159715, y=2000000
Sensor at x=3469799, y=2027984: closest beacon is at x=3174767, y=2783059
Sensor at x=3292782, y=2910639: closest beacon is at x=3174767, y=2783059
Sensor at x=3925315, y=2646100: closest beacon is at x=3174767, y=2783059
Sensor at x=1883646, y=2054943: closest beacon is at x=2159715, y=2000000
Sensor at x=2920303, y=3059306: closest beacon is at x=3073257, y=3410773
Sensor at x=2401153, y=2470599: closest beacon is at x=2062250, y=2735130
Sensor at x=2840982, y=3631975: closest beacon is at x=3073257, y=3410773
Sensor at x=1147584, y=3725625: closest beacon is at x=1912017, y=3034331
Sensor at x=2094987, y=2782172: closest beacon is at x=2062250, y=2735130
Sensor at x=3973421, y=982794: closest beacon is at x=3751293, y=-171037
Sensor at x=2855728, y=2514334: closest beacon is at x=3174767, y=2783059
Sensor at x=1950500, y=2862580: closest beacon is at x=1912017, y=3034331
Sensor at x=3233071, y=2843812: closest beacon is at x=3174767, y=2783059
Sensor at x=2572577, y=3883463: closest beacon is at x=3073257, y=3410773
Sensor at x=3791570, y=3910685: closest beacon is at x=3073257, y=3410773
Sensor at x=3509554, y=311635: closest beacon is at x=3751293, y=-171037
Sensor at x=1692070, y=2260914: closest beacon is at x=2159715, y=2000000
Sensor at x=1265756, y=1739058: closest beacon is at x=941123, y=1223290
"""

P1_SAMPLE_SOLUTION = False

P2_SAMPLE_SOLUTION = False


def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"


class Puzzle:
    def __init__(self, input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split("\n")

    def p1(self):
        return True

    def p2(self):
        return True


def main():
    parser = argparse.ArgumentParser(description=f"AOC2022 Puzzle Day { DAY }")
    parser.add_argument(
        "-p", "--showpuzzle", help="Display Puzzle Text", action="store_true"
    )
    parser.add_argument(
        "-s", "--showsample", help="Display Sample Input", action="store_true"
    )
    args = parser.parse_args()

    if args.showpuzzle:
        print(f"###############\nAOC 2022 DAY {DAY} PUZZLE TEXT\n###############")
        print(PUZZLE_TEXT)

    if args.showsample:
        print(f"###############\nAOC 2022 DAY {DAY} SAMPLE INPUT\n###############")
        print(SAMPLE_INPUT.strip())
        print(
            f"\n###############\nAOC 2022 DAY {DAY} P1 SAMPLE SOLUTION\n###############"
        )
        print(P1_SAMPLE_SOLUTION)
        print(
            f"\n###############\nAOC 2022 DAY {DAY} P2 SAMPLE SOLUTION\n###############"
        )
        print(P2_SAMPLE_SOLUTION)

    if P1_SAMPLE_SOLUTION:
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=SAMPLE_INPUT)
        sample.p1()
        if P1_SAMPLE_SOLUTION == sample.p1_solution:
            print("Sample correct.")
        else:
            print(
                f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {sample.p1_solution}"
            )
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            puzzle = Puzzle(input_text=PUZZLE_INPUT)
            puzzle.p1()
            print("Processing Input...\n")
            start_time = time()
            print(f"SOLUTION: {puzzle.p1_solution}")
            print(f"Elapsed time {elapsed_time(start_time)}")

    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...\n")
        start_time = time()
        sample.p2()
        if P2_SAMPLE_SOLUTION == sample.p2_solution:
            print("Sample correct.")
        else:
            print(
                f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {sample.p2_solution}"
            )
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            puzzle.p2()
            print(f"SOLUTION: {puzzle.p2_solution}")
            print(f"Elapsed time {elapsed_time(start_time)}")


if __name__ == "__main__":
    main()

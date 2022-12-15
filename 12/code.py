import argparse
from time import time
import numpy

DAY = 12

PUZZLE_TEXT = """
--- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
"""

SAMPLE_INPUT = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

PUZZLE_INPUT = """
abccccaaacaccccaaaaacccccccaaccccccccaaaaaaccccccaaaaaccccccccccaaaaaaaaacccccccaaaaaaaaaaaaaaccaaaaaccccccccccccaccacccccccccccccccccccccccccccccccccccccccaaaaaa
abccaacaaaaaccaaaaacccccaaaaaccccccccaaaaaaccccccaaaaaacccccccccaaaaaaaaaaaaacccaaaaaaaaaaaaaaaaaaaaaccccccccccccaaaacccccccccccccccccccccccccccccccccccccccaaaaaa
abccaaaaaaaaccaaaaaacccccaaaaaccccccaaaaaaaacccccaaaaaaccccccccccaaaaaaaaaaaacccaaaaaacaaaaaacaaaaaaaaccccccccccaaaaacccccaccccccccccccccccccaaacccccccccccccaaaaa
abcccaaaaaccccccaaaacccccaaaaacccccaaaaaaaaaaccccaaaaaacccccccccaaaaaaaaaaaaaacaaaaaaaaaaaaaacaaaaaaaaccccccccccaaaaaacccaaacccccccccccccccccaaaccccccccccccccaaaa
abaaacaaaaacccccacccccccaaaaaccccccaaaaaaaaaaccccccaaaccccccccccaaaaaaaaacaaaaaaaaaaaaaaaaaaacccaaacaccaaaccccccaaaaaaaacaaacccccccccccaaccccaaacccccccccccccccaac
abaaacaacaaaaccccccccccccccaaccccccacaaaaacccccaacccccccccccccccaaaacaaaaaaaaaacccaacccaaacaacccaaccccaaaaccccccccaacaaaaaaaaaaccccccccaaaaccaaaccccccccccccccaaac
abaaccaaccaaacacccccccccccccccccccccccaaaacccaaaaaaccaaaccccccccccaacaaaaaaaaaacccaaccccccccccccccccccaaaaccccccccccccaaaaaaaaaccccccciiiiiaaaaacccccccccccccccccc
abaaccccaaaaaaaacccccccccccccccccccccccaaccccaaaaaaccaaaaaccccacccaaccaaacaaaaacccccccccccccccaacccccccaaaccccccccccccccaaaaacccccccciiiiiiiiaaaaaccccccaaaccccccc
abaaacccaaaaaaaacccccccccccccccccccccccccccccaaaaaacaaaaaccccaaaaaaaccaaccaaacccccccaaaaacacccaaccccccccccaacccccccccccaaaaaaccccccciiiiiiiiijjaaaaaccccaaacaccccc
abaaaccccaaaaaaccccccccccccccccccccaaccccccccaaaaaccaaaaacccccaaaaaaaaccccccccccccccaaaaaaaaaaaaccccccccccaaacaaccccccaaaaaaaccccccciiinnnnoijjjjjjjjjjaaaaaaacccc
abccccccccaaaaacccccaacccccccccccaaaacccccccccaaaacccaaaaaccccaaaaaaaaacccccccccccccaaaaaaaaaaaaaaccccccccaaaaaacccaacaaacaaacccccchhinnnnnoojjjjjjjjjkkaaaaaacccc
abcccccccaaaaaacaaacaacccccccccccaaaaaaccccccccccccccaacccccccaaaaaaaaacaaccccccccccaaaaaaaaaaaaaaacccccaaaaaaacccaaaaccccccacaaccchhinnnnnoooojjjjjjkkkkaaaaccccc
abaacccaccaaaccccaaaaaccccccccccccaaaaccccccccccccccccccccccccaaaaaaaacaaaaaaaccccccaaaaaaaaaaaaaaacccccaaaaaaacccaaaaccccaaacaaachhhnnntttuooooooooppkkkaaaaccccc
abaacccaaaaaaaccccaaaaaacccccccccaaaaaccccccccccccccccccccccccaaaaaaacccaaaaacccccccccaaacaaaaaaaaccccccccaaaaacccaaaacccccaaaaacchhhnnnttttuooooooppppkkkaaaccccc
abaacccaaaaaaccccaaaaaaacccccccccaacaaccccccccccccccccccccccaaaccaaaccaaaaaaacccccccccccccaaaaaaaccccccaacaacaaacccccccccccaaaaaahhhhnntttttuuouuuuupppkkkcccccccc
abaaaacaaaaaaaaaaaaaaacccccccccccccccccccccccccccccccccccccaaaacccaaacaaaaaaaaccccccccccccaccaaaccccccaaacaaccccccccccccccaaaaaahhhhnnntttxxxuuuuuuupppkkkcccccccc
abaaaacaaaaaaaaaaacaaacccaaacccccccccccccccccccccacccccccccaaaacccccccaaaaaaaaccccccccccccccccaaacccccaaacaaacccccccccccccaaaaaahhhhmnnttxxxxuuyuuuuuppkkkcccccccc
abaaaccaaaaaaaaccccaaaccccaaaccacccccccccccaaaaaaaaccccccccaaaacccccccccaaacaacccccccccccccccccccccaaaaaaaaaacccccacccccccaacaghhhmmmmtttxxxxxxyyyuupppkkccccccccc
abaaccaaaaaaaccccccccccccaaaaaaaacccccccccccaaaaaaccccccccccccccccccccccaaccccccaacccccccccccccccccaaaaaaaaacccccaaccccccccccagggmmmmttttxxxxxyyyyvvppkkkccccccccc
abaacccaccaaacccccccccccaaaaaaaaccccccccccccaaaaaaccccccccccccccccccccccccccaaacaaaccccccccccccccccccaaaaaccccaaaaacaacccccccgggmmmmttttxxxxxyyyyvvpppiiiccccccccc
SbaaaaaccccaaccccccccccaaaaaaaaacacccccccccaaaaaaaacccccccccccccccaacccccccccaaaaaccccccccccaaaacccccaaaaaacccaaaaaaaaccaaaccgggmmmsssxxxEzzzzyyvvvpppiiiccccccccc
abaaaaaccccccccccccccccaaaaaaaaaaaaaaaaaccaaaaaaaaaacccccccccccaaaaacccccccccaaaaaaaccccccccaaaaaccccaaaaaaaccccaaaaacccaaaaagggmmmsssxxxxxyyyyyyvvqqqiiiccccccccc
abaaaaacccccccccccccccccaaaaaaaacaaaaaacccaaaaaaaaaaccccccccccccaaaaacccccccaaaaaaaacccccccaaaaaaccccaaacaaacccaaaaacccaaaaaagggmmmssswwwwwyyyyyyyvvqqqiiicccccccc
abaaaaccccccccccccccccccccaaaaaaaaaaaaacccacacaaacccccccccccccccaaaaacccccccaaaaaaaacccccccaaaaaaccccacccccccccaacaaaccaaaaaagggmmmsssswwwwyyyyyyyvvvqqiiicccccccc
abaaaaacccccccccccccccccccaacccaaaaaaaaaccccccaaaccccccccccccccaaaaaccccccccaacaaacccccccccaaaaaacccccccccccccccccaaccccaaaaagggmmmmssssswwyywwvvvvvvqqiiicccccccc
abaaaaaccccccccccccccccccaaacccaaaaaaaaaacccccaaaccccccaacccccccccaaccaaccccccaaaacaccccaacccaacccccccccccccccccccccccccaaaaccggglllllssswwwywwwvvvvqqqiiicccccccc
abaccccccccccccccccccccccccccccaaaaaaaaaaccccaaaacccaaaacccccccccccccaaaccccccaaaaaaaaaaaacccccccccccccccccccccccccccccccccccccffffllllsswwwwwwrrqvqqqqiiicccccccc
abccccccccccccccccccccccccccccccccaaacacaccccaaaacccaaaaaacccccccccaaaaaaaaccccaaaaaaaaaaaacccccccccccccccccccccccccccccccccccccfffflllssrwwwwrrrqqqqqqjjicccccccc
abcccccccaaaccccccccaaccccccccccccaaacccccccccaaaccccaaaaacccccccccaaaaaaaaccaaaaaaacaaaaaaacccccccccccccccccccccccccccccccccccccfffflllrrwwwrrrrqqqqjjjjjcccccccc
abaaaccaaaaacccccccaaacaaccccccccccaacccccccccccccccaaaaacccccccccccaaaaaacccaaaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccccccffffllrrrrrrrkjjjjjjjjjcccaccccc
abaaaccaaaaaacccccccaaaaacaacaaccccccccccccccccccccccccaacccccccccccaaaaaacccaaaaaaaaaaaaacccccccccccccccccccccccccccccccccccccccccfffllrrrrrrkkjjjjjjjcccccaccccc
abaaaccaaaaaacccccaaaaaaccaaaaacccccccccccccccccccccccccccccccccccccaaaaaacccccaaacaaaaaaacccccccccccccccccccccccccccccccccccccccccfffllkkrrrkkkjjddcccccccaaacccc
abaaaccaaaaaccccccaaaaaaaacaaaaaccccccccccccccccccccccccccccccccccccaaacaacccccaaaccccccaaaaccccaaaccccccccccccccccaaaccccccccccccccfeekkkkkkkkkdddddccccaaaaacccc
abaaacccaaaaccccccaacaaaaaaaaaaaccccccccccccccccccccccccccccccccccccccaacaacccccccccccccccaaccccaaaacccccccccccccccaaaacccccccccccccceeekkkkkkdddddddcccaaacaccccc
abaccccccccccccccccccaacccaaaaccccccccccccccccccccccccccccaaccaaccaacccaaaaccccccccccccaaaaaaaacaaaacccccccccccccccaaaacccaaaaacccccceeeekkkkdddddaaccccaacccccccc
abccccccccccccccccccaaccccccaaccccccccccccaaacccccccccccccaaaaaaccaaaacaaaaacccccccccccaaaaaaaacaaaccccccccccccccccaaaacccaaaaaccccccceeeeeeedddcacacccccccccccccc
abccccccccccccccccccccccccccccccccccccccccaaaacaacccccccccaaaaacccaaaaaaaaaaccccccccccccaaaaaacccccccccccccccccccccccccccaaaaaacccccccaeeeeeeddcccccccccccccccaaac
abccccccccccccccccccccccccccccccccccccccccaaaaaaacccccccccaaaaaaccaaaaaaaacaccccccaaacaaaaaaaacccccccccccccccccccccccccccaaaaaacccccccccceeeeaaccccccccccccccccaaa
abcccccccccccccccccccccccccccccccccccccccccaaaaaaccccccccaaaaaaaaccaaaaaaaccccccccaaaaaaaaaaaacccccccccccccccccccccccccccaaaaaacccccccccccccaaaccccccccccccccccaaa
abccccccccccccccccccccccccccccccccccccccaaaaaaaaccccaaaccaaaaaaaacaaaaaaaaaacccccccaaaaaaaccaacccccccccccccccccccccccccccccaacccccccccccccccaaaccccccccccccccaaaaa
abccccccccccccccccccccccccccccccccccccccaaaaaaaaacccaaaaccccaaccaaaaaaaaaaaaaccccaaaaaaaaaacccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccaaaaaa
"""

P1_SAMPLE_SOLUTION = 31

P2_SAMPLE_SOLUTION = 29


def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"


class Grid:
    def __init__(self, gridmap) -> None:
        self.gridmap = gridmap
        self.gridmap_t = numpy.transpose(self.gridmap).tolist()
        self.height = len(self.gridmap)
        self.width = len(self.gridmap_t)
        self.every_node = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.every_node.append((x, y))

    def pos(self, coordinate):
        x, y = coordinate[0], coordinate[1]
        return self.gridmap[y][x]

    def adj(self, coordinate) -> "dict":
        """
        returns a dictionary containing the valid cardinal adjacents and their vlaues
        """
        x, y = coordinate[0], coordinate[1]
        adj = dict()

        if x > 0:
            adj[(x - 1, y)] = self.gridmap[y][x - 1]
        if x < self.width - 1:
            adj[(x + 1, y)] = self.gridmap[y][x + 1]
        if y > 0:
            adj[(x, y - 1)] = self.gridmap[y - 1][x]
        if y < self.height - 1:
            adj[(x, y + 1)] = self.gridmap[y + 1][x]

        return adj

    def adjd(self, coordinate) -> "dict":
        """returns a dictionary of all valid adjacents including diagonals, and their value."""
        x, y = coordinate[1], coordinate[0]
        adjd = dict()
        adj_x = list(range(max(0, x - 1), min(self.width, x + 2)))
        adj_y = list(range(max(0, y - 1), min(self.height, y + 2)))
        for _x in adj_x:
            for _y in adj_y:
                if (_x, _y) != (x, y):
                    adjd[(_x, _y)] = self.gridmap[_y][_x]

        return adjd


class DjikstraInTheHills:
    def __init__(self, grid) -> None:
        self.grid = Grid(grid)
        self.elevations = [*".abcdefghijklmnopqrstuvwxyz"]

    def find_path(self, start_position=None, current_shortest_distance=None):
        self.unvisited = [node for node in self.grid.every_node]
        self.unvisited.reverse()

        self.distance = {}
        for node in self.unvisited:
            self.distance[node] = 99999999
        if start_position:
            self.position = start_position
            self.destination = None
            while not self.destination:
                for node in self.unvisited:
                    if self.grid.pos(node) == "E":
                        self.destination = node
        else:
            for node in self.unvisited:
                if self.grid.pos(node) == "S":
                    self.position = node
                if self.grid.pos(node) == "E":
                    self.destination = node
        self.distance[self.position] = 0
        # 3. For the current node, consider all of its unvisited neighbors and calculate their
        # tentative distances through the current node. Compare the newly calculated
        # tentative distance to the one currently assigned to the neighbor and assign
        # it the smaller one. For example, if the current node A is marked with a distance
        # of 6, and the edge connecting it with a neighbor B has length 2, then the distance
        # to B through A will be 6 + 2 = 8. If B was previously marked with a distance greater
        # than 8 then change it to 8. Otherwise, the current value will be kept.
        while self.position != self.destination and len(self.unvisited) != 0:
            if (
                current_shortest_distance
                and self.distance.get(self.position)
                and current_shortest_distance < self.distance[self.position]
            ):
                self.unvisited.remove(self.position)

                tentative_distance = 99999999
                for candidate in self.unvisited:
                    if self.distance[candidate] < tentative_distance:
                        tentative_distance = self.distance[candidate]
                        next_node = candidate
                    else:
                        self.unvisited.remove(candidate)

                self.position = next_node

                continue
            candidates = self.grid.adj(self.position)
            if self.grid.pos(self.position) == "S":
                current_elevation = 1
            else:
                current_elevation = self.elevations.index(self.grid.pos(self.position))
            next_node = None
            for position, elevation in candidates.items():
                if elevation == "S":
                    this_elevation = 1
                elif elevation == "E":
                    this_elevation = 26
                else:
                    this_elevation = self.elevations.index(elevation)
                if (
                    this_elevation in range(0, current_elevation + 2)
                    and position in self.unvisited
                ):
                    tentative_distance = self.distance[self.position] + 1
                    if self.distance[position] >= tentative_distance:
                        self.distance[position] = tentative_distance

            # 4. When we are done considering all of the unvisited neighbors of the current node,
            # mark the current node as visited and remove it from the unvisited set. A visited
            # node will never be checked again
            # 5. If the destination node has been marked visited (when planning a route between two
            # specific nodes) ,then stop. The algorithm has finished.
            # 6. Otherwise, select the unvisited node that is marked with the smallest tentative
            # distance, set it as the new current node, and go back to step 3.
            self.unvisited.remove(self.position)

            tentative_distance = 99999999
            for candidate in self.unvisited:
                if self.distance[candidate] < tentative_distance:
                    tentative_distance = self.distance[candidate]
                    next_node = candidate

            if next_node == None:
                return False

            self.position = next_node
        if self.position == self.destination:
            return self.distance[self.destination]
        else:
            return False


class Puzzle:
    def __init__(self, input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split("\n")
        self.heightmap = [[*row] for row in self.input_list]

    def p1(self):
        find_path = DjikstraInTheHills(self.heightmap)
        self.p1_solution = find_path.find_path()

    def p2(self):
        smallest = 9999999
        find_path = DjikstraInTheHills(self.heightmap)
        for node in [
            node
            for node in find_path.grid.every_node
            if find_path.grid.pos(node) in "Sa"
        ]:
            result = find_path.find_path(start_position=node)
            if result is not False and result < smallest:
                smallest = result
                print(f"New Best Path Found: Node {node} - Distance {result}")

        self.p2_solution = smallest


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

import argparse
from time import time

DAY = 9

PUZZLE_TEXT = '''
--- Day 9: Rope Bridge ---

This rope bridge creaks as you walk along it. You aren't sure how old it is, or whether it can even support your weight.

It seems to support the Elves just fine, though. The bridge spans a gorge which was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist. You decide to distract yourself by modeling rope physics; maybe you can even figure out where not to step.

Consider a rope with a knot at each end; these knots mark the head and the tail of the rope. If the head moves far enough away from the tail, the tail is pulled toward the head.

Due to nebulous reasoning involving Planck lengths, you should be able to model the positions of the knots on a two-dimensional grid. Then, by following a hypothetical series of motions (your puzzle input) for the head, you can determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head (H) and tail (T) must always be touching (diagonally adjacent and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...
If the head is ever two steps directly up, down, left, or right from the tail, the tail must also move one step in that direction so it remains close enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...
Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....
You just need to work out where the tail goes as the head follows a series of motions. Assume the head and the tail both start at the same position, overlapping.

For example:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
This series of motions moves the head right four steps, then up four steps, then left three steps, then down one step, and so on. After each step, you'll need to update the position of the tail if the step means the head is no longer adjacent to the tail. Visually, these motions occur as follows (s marks the starting position as a reference point):

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

== R 4 ==

......
......
......
......
TH....  (T covers s)

......
......
......
......
sTH...

......
......
......
......
s.TH..

......
......
......
......
s..TH.

== U 4 ==

......
......
......
....H.
s..T..

......
......
....H.
....T.
s.....

......
....H.
....T.
......
s.....

....H.
....T.
......
......
s.....

== L 3 ==

...H..
....T.
......
......
s.....

..HT..
......
......
......
s.....

.HT...
......
......
......
s.....

== D 1 ==

..T...
.H....
......
......
s.....

== R 4 ==

..T...
..H...
......
......
s.....

..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....
After simulating the rope, you can count up all of the positions the tail visited at least once. In this diagram, s again marks the starting position (which the tail also visited) and # marks other positions the tail visited:

..##..
...##.
.####.
....#.
s###..
So, there are 13 positions the tail visited at least once.

Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least once?

Your puzzle answer was 5878.

--- Part Two ---

A rope snaps! Suddenly, the river is getting a lot closer than you remember. The bridge is still there, but some of the ropes that broke are now whipping toward you as you fall through the air!

The ropes are moving too quickly to grab; you only have a few seconds to choose how to arch your body to avoid being hit. Fortunately, your simulation can be extended to support longer ropes.

Rather than two knots, you now must simulate a rope consisting of ten knots. One knot is still the head of the rope and moves according to the series of motions. Each knot further down the rope follows the knot in front of it using the same rules as before.

Using the same series of motions as the above example, but with the knots marked H, 1, 2, ..., 9, the motions now occur as follows:

== Initial State ==

......
......
......
......
H.....  (H covers 1, 2, 3, 4, 5, 6, 7, 8, 9, s)

== R 4 ==

......
......
......
......
1H....  (1 covers 2, 3, 4, 5, 6, 7, 8, 9, s)

......
......
......
......
21H...  (2 covers 3, 4, 5, 6, 7, 8, 9, s)

......
......
......
......
321H..  (3 covers 4, 5, 6, 7, 8, 9, s)

......
......
......
......
4321H.  (4 covers 5, 6, 7, 8, 9, s)

== U 4 ==

......
......
......
....H.
4321..  (4 covers 5, 6, 7, 8, 9, s)

......
......
....H.
.4321.
5.....  (5 covers 6, 7, 8, 9, s)

......
....H.
....1.
.432..
5.....  (5 covers 6, 7, 8, 9, s)

....H.
....1.
..432.
.5....
6.....  (6 covers 7, 8, 9, s)

== L 3 ==

...H..
....1.
..432.
.5....
6.....  (6 covers 7, 8, 9, s)

..H1..
...2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

.H1...
...2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

== D 1 ==

..1...
.H.2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

== R 4 ==

..1...
..H2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

..1...
...H..  (H covers 2)
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

......
...1H.  (1 covers 2)
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

......
...21H
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

== D 1 ==

......
...21.
..43.H
.5....
6.....  (6 covers 7, 8, 9, s)

== L 5 ==

......
...21.
..43H.
.5....
6.....  (6 covers 7, 8, 9, s)

......
...21.
..4H..  (H covers 3)
.5....
6.....  (6 covers 7, 8, 9, s)

......
...2..
..H1..  (H covers 4; 1 covers 3)
.5....
6.....  (6 covers 7, 8, 9, s)

......
...2..
.H13..  (1 covers 4)
.5....
6.....  (6 covers 7, 8, 9, s)

......
......
H123..  (2 covers 4)
.5....
6.....  (6 covers 7, 8, 9, s)

== R 2 ==

......
......
.H23..  (H covers 1; 2 covers 4)
.5....
6.....  (6 covers 7, 8, 9, s)

......
......
.1H3..  (H covers 2, 4)
.5....
6.....  (6 covers 7, 8, 9, s)
Now, you need to keep track of the positions the new tail, 9, visits. In this example, the tail never moves, and so it only visits 1 position. However, be careful: more types of motion are possible than before, so you might want to visually compare your simulated rope to the one above.

Here's a larger example:

R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
These motions occur as follows (individual steps are not shown):

== Initial State ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........H..............  (H covers 1, 2, 3, 4, 5, 6, 7, 8, 9, s)
..........................
..........................
..........................
..........................
..........................

== R 5 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........54321H.........  (5 covers 6, 7, 8, 9, s)
..........................
..........................
..........................
..........................
..........................

== U 8 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
................H.........
................1.........
................2.........
................3.........
...............54.........
..............6...........
.............7............
............8.............
...........9..............  (9 covers s)
..........................
..........................
..........................
..........................
..........................

== L 8 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
........H1234.............
............5.............
............6.............
............7.............
............8.............
............9.............
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

== D 3 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
.........2345.............
........1...6.............
........H...7.............
............8.............
............9.............
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

== R 17 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
................987654321H
..........................
..........................
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

== D 10 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........s.........98765
.........................4
.........................3
.........................2
.........................1
.........................H

== L 25 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
H123456789................

== U 20 ==

H.........................
1.........................
2.........................
3.........................
4.........................
5.........................
6.........................
7.........................
8.........................
9.........................
..........................
..........................
..........................
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

Now, the tail (9) visits 36 positions (including s) at least once:

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
#.........................
#.............###.........
#............#...#........
.#..........#.....#.......
..#..........#.....#......
...#........#.......#.....
....#......s.........#....
.....#..............#.....
......#............#......
.......#..........#.......
........#........#........
.........########.........
Simulate your complete series of motions on a larger rope with ten knots. How many positions does the tail of the rope visit at least once?

Your puzzle answer was 2405.


'''

SAMPLE_INPUT = '''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''

P2_SAMPLE_INPUT = '''
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''

PUZZLE_INPUT = '''
D 2
R 1
U 1
L 1
D 2
L 2
R 1
U 1
D 2
U 1
R 1
U 1
D 2
R 2
L 2
U 2
D 1
L 2
R 2
D 2
U 2
R 2
U 1
D 1
L 2
D 2
L 2
U 1
R 2
L 2
D 2
L 1
D 2
L 1
R 2
L 2
U 1
D 2
L 1
U 2
R 1
D 2
L 2
D 1
L 2
U 1
L 1
R 2
U 2
L 2
D 1
L 1
D 1
L 2
R 1
D 2
U 2
D 2
R 1
L 2
R 2
U 1
R 1
L 2
U 2
D 1
U 2
L 1
R 2
D 2
L 2
U 1
L 1
D 2
R 2
U 1
R 2
U 2
D 2
L 1
U 1
D 1
R 1
U 1
D 2
L 1
D 2
U 2
D 1
U 2
L 2
D 2
R 2
D 1
R 2
L 2
U 1
R 1
L 1
U 2
D 2
U 2
L 2
U 2
R 2
L 1
U 1
D 1
L 2
D 2
R 2
U 3
R 3
U 2
L 1
U 1
L 1
U 2
R 2
U 2
D 1
R 3
D 1
L 3
R 2
D 3
U 1
D 2
L 2
D 2
L 1
R 3
D 1
R 1
L 3
R 1
U 2
D 2
L 3
R 1
U 2
L 2
R 3
D 1
U 2
D 2
L 3
D 1
R 3
U 3
R 2
U 3
D 1
U 2
R 2
U 3
R 1
U 2
L 3
D 3
U 1
D 2
U 2
L 2
R 1
L 3
R 1
L 3
U 2
R 1
U 1
L 1
R 2
U 2
D 1
R 3
D 3
L 2
D 2
R 2
L 3
R 1
L 1
R 3
L 3
D 2
U 1
L 2
U 3
R 1
L 1
R 1
L 1
D 1
R 2
D 2
U 1
L 1
D 3
R 2
D 1
L 3
R 3
U 3
D 2
U 1
D 2
R 1
U 1
R 2
D 2
U 1
D 3
R 2
U 3
D 3
R 1
D 1
U 2
D 1
U 2
D 3
U 3
D 2
R 4
D 2
R 1
L 4
U 2
D 1
U 2
R 2
U 1
R 1
U 4
L 4
U 3
L 2
U 3
D 3
R 2
L 2
U 3
D 1
L 3
U 1
L 1
U 2
L 4
R 3
U 3
D 1
L 3
R 4
D 4
L 3
R 4
D 1
R 4
D 1
L 3
D 1
L 1
U 2
D 1
U 4
R 1
D 2
U 2
D 4
U 3
D 2
L 4
R 3
U 3
R 2
D 3
U 4
R 4
L 3
U 2
D 2
U 2
L 1
R 3
D 4
U 1
D 2
U 1
R 2
L 2
R 3
U 4
D 1
L 1
R 1
D 4
L 4
D 4
L 2
R 3
L 1
U 2
L 1
D 3
U 2
R 2
D 1
R 1
U 1
L 2
D 2
U 3
L 3
U 1
L 1
D 1
L 3
R 4
L 2
R 1
U 2
D 4
U 2
L 4
U 4
R 1
D 3
U 2
L 2
D 4
L 2
U 1
D 5
L 5
R 1
D 1
L 4
D 5
R 4
U 2
R 2
L 2
D 3
U 4
L 1
U 1
R 2
L 4
R 3
U 1
D 5
U 4
D 2
R 3
L 1
D 4
L 5
D 1
L 2
U 1
R 2
L 2
R 1
L 2
U 4
D 1
U 5
L 2
R 1
D 5
L 2
D 5
U 5
R 3
L 4
D 2
L 2
D 2
U 5
R 3
U 1
D 3
R 4
U 3
R 2
U 3
D 5
U 4
L 3
R 3
D 3
R 1
L 1
D 4
R 3
D 2
L 2
R 4
L 3
R 2
D 4
L 3
U 1
D 2
L 3
U 4
D 5
U 2
L 2
R 1
D 1
L 3
U 2
R 4
D 4
L 4
U 2
D 1
R 5
L 3
U 3
L 5
R 2
D 1
L 2
D 2
L 2
R 4
L 3
D 3
R 5
L 5
D 3
R 5
L 2
R 1
D 4
L 2
D 1
U 2
D 4
U 5
L 4
D 2
U 2
D 4
U 6
L 3
U 1
D 2
R 1
U 5
D 2
L 4
R 6
U 2
L 2
D 1
R 5
U 2
D 5
R 5
U 4
D 6
U 1
D 2
U 5
D 5
L 6
U 5
D 6
L 4
U 6
R 5
L 6
D 5
L 5
D 6
U 5
L 6
U 5
L 3
R 2
D 1
R 1
L 6
U 5
D 1
R 2
D 2
L 2
D 6
U 6
L 1
R 6
L 3
D 6
R 3
D 2
U 5
D 4
L 2
R 3
D 5
U 1
D 3
R 6
U 4
L 4
U 4
D 1
R 4
U 2
R 6
L 1
D 3
R 3
U 1
L 6
R 4
D 2
U 2
D 6
L 4
R 6
U 3
R 3
D 3
L 1
R 5
U 4
R 6
L 2
R 1
U 1
L 6
D 6
L 3
R 2
D 6
R 6
L 3
U 3
D 1
L 3
D 1
R 4
D 3
U 3
D 2
U 6
D 4
L 4
R 5
D 1
L 7
R 3
L 5
R 3
U 6
L 5
U 3
D 1
L 5
R 4
L 1
U 6
L 1
R 4
D 3
R 7
D 7
R 4
L 4
D 4
L 2
R 1
U 7
L 1
D 7
L 1
D 1
R 5
D 5
U 2
L 6
R 2
U 5
L 7
D 7
L 7
U 1
L 6
D 2
L 6
U 2
R 4
U 7
D 2
L 6
U 7
R 5
U 7
L 7
D 2
R 4
U 6
R 1
D 3
R 2
L 5
R 5
U 3
L 5
U 4
D 4
L 5
R 1
L 4
D 5
U 1
L 4
D 7
R 6
D 7
U 7
D 4
R 1
D 2
L 5
R 4
D 3
U 2
D 4
R 3
L 4
R 4
U 3
D 7
R 2
L 1
D 5
R 3
D 2
L 7
R 3
D 5
R 1
D 2
R 6
L 5
R 7
L 5
U 2
R 3
D 6
L 1
D 4
R 2
U 1
D 1
R 6
D 5
L 3
R 7
L 3
U 5
R 5
U 3
D 8
L 2
U 6
L 8
U 4
D 5
R 7
U 7
L 4
R 3
L 3
D 1
L 6
R 5
L 6
R 6
L 8
D 3
U 2
L 7
R 2
U 8
D 3
L 4
R 3
U 8
R 3
U 6
D 8
R 2
L 8
U 2
R 5
D 1
U 1
D 8
R 4
L 7
D 2
U 3
D 1
R 2
U 1
L 5
U 4
R 5
D 6
L 3
U 1
D 6
U 6
D 6
U 2
L 6
U 6
D 5
L 1
D 7
U 2
D 4
L 5
R 4
D 2
L 6
U 2
R 1
U 4
L 3
D 3
R 6
D 4
R 3
L 2
U 8
R 5
L 2
U 3
R 7
U 7
R 4
U 5
D 1
L 8
R 8
U 3
L 1
U 7
L 7
D 2
L 8
D 7
R 7
L 3
R 4
L 3
R 4
U 6
L 5
R 4
U 7
L 3
D 3
R 2
L 6
U 3
L 1
R 8
L 6
D 7
L 8
R 7
L 6
D 2
U 2
R 3
L 9
R 7
D 1
R 9
L 2
D 5
U 7
D 5
U 4
L 4
D 5
L 6
R 3
U 2
R 6
D 3
U 2
R 1
D 5
U 6
L 8
D 8
U 9
L 2
U 5
L 2
U 3
L 4
U 6
L 3
D 2
R 5
L 3
R 8
D 8
U 8
R 4
U 2
D 3
L 9
U 2
L 4
U 5
R 5
L 7
U 9
L 7
U 5
L 6
U 6
R 5
L 9
U 9
R 3
D 8
U 8
R 9
D 4
U 9
D 9
L 3
R 2
D 3
U 1
R 7
D 5
U 9
D 7
U 3
D 8
L 9
U 1
R 6
L 8
R 2
L 7
D 3
U 4
D 9
L 1
R 4
D 9
U 1
D 1
L 8
U 2
D 8
U 1
L 1
U 2
D 7
L 1
D 2
L 6
U 2
D 8
R 7
L 4
U 5
R 2
U 8
D 6
R 3
D 8
R 4
L 5
U 4
L 1
U 6
L 10
D 7
R 5
D 9
U 6
D 5
L 9
U 2
R 3
U 7
R 7
D 1
R 4
U 10
D 4
R 7
L 7
D 3
R 5
U 5
D 6
U 2
D 2
U 6
D 5
L 6
U 10
D 7
R 6
L 9
R 7
L 7
U 6
D 6
R 8
D 8
R 4
D 4
L 1
R 3
U 5
R 2
L 9
R 8
L 3
U 3
R 6
U 2
L 6
U 4
D 5
R 6
U 5
R 8
U 10
L 5
U 2
R 1
D 9
U 8
D 2
U 9
L 7
R 2
D 10
L 7
D 3
R 4
L 2
U 2
R 7
U 6
D 9
U 8
L 7
D 4
U 4
R 6
U 3
D 9
L 1
U 9
R 9
D 4
L 9
R 6
L 6
U 9
L 10
R 1
L 5
R 1
L 2
D 8
U 2
L 1
R 4
U 9
L 3
D 9
L 6
R 8
U 6
R 8
L 5
D 2
R 5
U 8
R 2
L 9
R 3
U 3
R 8
U 5
D 5
U 8
D 10
R 4
L 5
U 2
L 4
D 2
L 1
D 3
U 8
D 3
U 4
L 6
D 6
U 9
L 5
D 5
U 10
R 9
D 2
U 11
D 4
L 8
D 8
L 4
U 6
D 3
R 9
U 11
L 7
U 7
D 9
U 10
D 9
U 2
R 2
U 7
R 2
U 10
R 7
L 7
U 6
D 10
L 5
U 4
D 4
L 3
D 3
L 2
R 5
D 5
U 10
R 3
U 8
L 10
U 5
R 3
L 9
R 5
D 1
L 8
R 8
D 10
L 6
D 5
L 6
R 7
D 10
U 3
D 9
L 8
D 5
U 10
L 5
U 4
D 7
U 11
L 6
U 6
L 9
R 6
U 8
R 8
L 6
U 8
L 8
U 9
D 4
L 10
D 6
R 5
D 8
L 7
D 6
R 4
D 11
U 5
D 4
R 7
U 11
L 5
U 7
D 7
L 11
R 9
U 1
D 11
R 8
L 4
R 2
D 6
L 4
R 8
D 9
R 11
U 2
L 9
U 6
R 10
L 11
R 9
D 10
U 11
L 6
U 3
L 2
R 11
L 2
D 2
L 5
D 6
U 11
D 10
U 8
L 3
R 9
D 5
R 9
D 6
R 2
U 2
D 11
R 6
U 9
R 12
U 6
L 1
D 2
L 5
D 9
L 5
D 4
U 10
L 12
U 6
R 6
U 4
L 4
U 1
L 4
R 12
L 11
R 3
U 10
L 4
R 11
D 9
L 9
U 11
D 1
L 1
R 3
D 7
U 6
R 4
D 3
L 8
U 5
R 6
L 9
U 4
L 6
D 6
U 6
L 5
R 7
D 10
R 5
U 8
L 5
R 6
U 10
R 2
U 2
R 10
U 12
D 12
L 7
U 3
R 1
L 6
D 6
L 5
D 8
U 8
D 11
L 2
D 10
L 6
R 10
L 9
D 5
R 1
D 7
R 6
U 10
D 8
R 9
D 11
R 8
U 7
R 10
L 1
U 3
R 11
D 11
L 8
D 13
U 6
D 12
U 2
L 2
U 11
D 1
R 3
U 8
R 4
L 3
U 7
D 4
L 3
R 2
L 3
R 6
D 13
L 1
R 8
L 5
R 11
D 7
L 8
D 12
U 12
D 3
L 6
U 1
R 7
U 2
D 9
L 3
U 11
R 2
U 6
D 11
L 10
D 4
U 13
D 1
R 11
L 3
U 2
D 7
R 8
D 10
R 12
D 4
R 1
U 5
R 5
U 2
R 12
D 3
L 8
D 11
U 3
R 1
U 2
R 3
D 5
U 8
D 4
R 6
L 2
R 4
U 6
D 12
L 7
U 2
L 8
U 8
R 13
U 10
L 11
R 1
D 4
R 1
U 5
L 9
D 9
U 11
D 13
U 9
R 2
D 9
U 6
R 1
D 12
R 3
U 1
R 13
U 11
L 6
R 3
D 11
U 13
R 2
U 8
L 11
R 12
D 7
L 11
U 10
D 2
L 9
R 1
L 9
R 10
D 5
U 7
R 6
D 11
U 11
L 7
R 6
L 12
D 12
L 5
R 3
L 12
R 4
L 7
D 4
U 11
R 2
L 9
R 11
D 14
L 7
R 10
U 1
D 2
L 7
D 2
U 12
R 2
D 6
R 12
L 7
D 4
U 13
L 11
D 13
R 11
D 5
U 14
R 1
L 8
U 10
R 3
D 3
L 13
R 6
U 5
D 4
L 12
D 2
R 9
D 1
R 7
D 10
U 14
L 12
R 11
U 6
D 11
L 8
D 2
U 4
L 1
R 14
D 8
U 11
L 13
U 1
D 2
R 14
D 10
R 4
L 1
R 10
U 9
D 8
L 10
R 10
U 6
D 14
L 10
U 13
R 8
L 3
D 6
L 13
D 11
U 14
R 13
U 12
L 2
D 6
U 13
L 13
U 12
D 1
U 10
L 5
U 3
R 4
D 10
L 14
U 8
R 7
U 6
R 13
D 14
L 5
U 6
L 1
D 7
R 2
D 14
U 13
R 3
U 5
R 13
L 2
D 12
U 1
R 11
L 7
U 2
D 11
L 2
R 7
D 7
L 1
U 10
L 12
R 6
L 7
R 4
D 3
R 3
U 15
D 13
U 6
D 6
U 3
R 14
U 10
L 1
R 8
D 7
R 13
D 10
R 9
U 11
D 11
U 4
D 11
U 10
D 3
R 12
U 5
D 1
L 4
R 10
D 11
U 2
D 9
U 12
D 9
R 3
D 6
U 4
L 14
R 15
U 4
D 11
R 13
L 3
U 12
R 5
U 11
L 11
D 6
U 15
R 5
U 5
R 1
D 8
U 4
L 12
D 2
U 9
L 15
D 6
R 12
L 10
D 14
R 14
D 8
L 2
D 11
U 13
L 1
R 8
D 8
L 5
D 14
R 10
U 13
R 10
L 4
R 5
L 6
U 7
R 7
L 5
D 3
L 15
U 10
D 6
L 1
R 15
D 11
U 13
R 12
U 4
D 8
L 4
D 11
R 12
L 5
D 2
U 8
D 8
L 10
U 16
L 15
D 9
U 10
R 16
L 7
R 7
U 9
D 12
L 16
U 12
R 13
U 5
R 5
U 8
D 8
U 15
L 4
R 2
L 2
U 10
D 2
U 6
L 15
R 11
D 2
L 5
R 16
L 13
R 14
U 5
R 2
L 11
U 9
D 4
L 14
U 6
D 6
U 7
D 2
U 5
D 6
U 10
D 5
L 11
R 13
L 9
U 5
R 7
D 13
U 12
L 6
U 14
R 15
L 3
U 4
D 4
U 8
R 1
U 12
L 7
U 2
L 11
R 10
D 6
R 9
L 6
R 2
L 16
U 8
D 16
R 8
U 7
D 7
U 12
D 13
L 14
R 3
U 7
L 14
R 14
U 4
D 15
R 13
D 2
R 9
D 14
U 15
D 8
L 8
R 10
U 4
D 5
L 16
D 17
R 14
U 10
D 15
L 15
R 13
L 17
U 12
R 1
D 8
U 2
R 11
U 8
D 9
R 6
U 10
D 3
L 7
R 4
L 15
U 14
L 9
R 15
U 9
D 5
U 4
D 10
R 13
U 9
D 5
R 12
D 6
U 7
D 8
L 7
U 13
D 5
R 4
L 10
D 16
L 11
R 16
L 16
U 15
D 1
R 3
L 13
D 7
U 1
R 15
U 15
D 2
U 3
L 7
U 4
D 14
L 10
D 8
U 8
D 6
R 16
U 6
D 7
L 13
U 3
L 9
R 10
D 5
R 2
D 16
U 14
R 11
D 10
R 13
U 12
L 4
U 7
L 2
R 5
D 13
U 3
R 3
U 16
L 5
R 13
L 16
D 7
L 4
R 14
U 8
L 9
U 2
L 10
D 9
R 17
U 14
R 2
D 7
U 14
R 3
U 3
L 14
D 16
U 6
L 5
U 2
R 7
L 4
U 3
D 12
L 7
D 15
U 6
L 1
D 5
U 11
L 9
D 15
L 12
R 18
L 4
D 9
U 17
R 1
D 5
L 13
U 16
R 17
U 10
D 5
L 16
D 2
R 10
L 1
U 14
L 16
U 3
D 2
R 5
U 3
R 17
D 17
L 15
U 11
L 16
R 4
L 3
R 7
L 5
R 8
U 15
R 9
U 9
R 18
L 17
R 9
U 18
L 11
U 14
R 7
L 16
R 15
L 1
U 9
L 10
U 9
L 14
U 5
D 1
R 16
D 6
R 1
D 14
R 11
U 10
D 17
L 12
D 5
U 4
L 12
U 1
L 7
R 13
D 2
U 14
D 3
U 6
R 1
U 2
R 11
U 9
D 14
R 9
U 14
R 9
D 14
R 2
D 9
U 8
D 10
U 3
R 8
D 11
R 5
U 4
D 1
U 16
L 17
U 1
R 14
U 10
R 5
U 12
D 4
R 10
D 10
L 5
R 2
L 18
D 3
L 17
D 10
U 4
L 15
U 4
L 9
U 14
R 9
U 16
L 1
R 7
U 10
D 1
U 13
D 15
R 6
U 2
L 17
U 11
L 14
U 12
R 11
U 4
D 11
R 7
D 13
U 16
L 5
U 7
R 4
L 17
D 2
U 18
R 8
U 16
L 15
R 8
L 19
U 17
D 2
U 8
D 9
U 3
L 12
U 16
L 3
R 14
D 16
U 11
D 2
L 16
U 4
L 18
R 15
U 9
L 18
U 11
R 18
L 13
D 8
U 12
D 14
L 12
U 2
D 13
L 12
U 16
R 17
L 14
U 10
R 15
U 19
L 17
R 8
L 17
R 8
U 4
R 8
U 11
L 17
R 8
D 13
U 6
D 7
R 9
L 2
R 4
D 16
L 2
D 10
U 4
L 10
D 14
U 5
D 7
U 4
D 16
U 14
L 4
U 14
L 3
D 16
L 14
U 11
D 3
L 10
U 8
D 6
L 9
D 17
R 16
'''

P1_SAMPLE_SOLUTION = 13

P2_SAMPLE_SOLUTION = 36

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

class Knot():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.positions = {(0,0)}
        self.leader = None
        self.follower = None

    def lead(self,x=0,y=0):
        self.x += x
        self.y += y
        self.adjx = range(self.x-1,self.x+2)
        self.adjy = range(self.y-1,self.y+2)
        self.positions.add((self.x,self.y))
        self.follower.follow()
    
    def follow(self):
        if self.y not in self.leader.adjy or self.x not in self.leader.adjx:
            if self.y > self.leader.y:
                self.y -= 1
            elif self.y < self.leader.y:
                self.y += 1
            
            if self.x > self.leader.x:
                self.x -= 1
            if self.x < self.leader.x:
                self.x += 1
                
            self.adjx = range(self.x-1,self.x+2)
            self.adjy = range(self.y-1,self.y+2)
            self.positions.add((self.x,self.y))
            
            if self.follower:
                self.follower.follow()        

class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')
    
    def update_input_list(self):
        self.input_list = self.input_text.strip().split('\n')
    
    def build_rope(self,knots):
        self.knots = []
        for knot in range(0,knots):        
            self.knots.append(Knot())
            if knot > 0:
                self.knots[knot-1].follower = self.knots[knot]
                self.knots[knot].leader = self.knots[knot-1]
    
    def move_rope(self,direction,length):
        match direction:
            case "U":
                for _ in range(0,length):
                    self.knots[0].lead(x=1)                    
            case "D":
                for _ in range(0,length):
                    self.knots[0].lead(x=-1)
            case "L":
                for _ in range(0,length):
                    self.knots[0].lead(y=1)
            case "R":
                for _ in range(0,length):
                    self.knots[0].lead(y=-1)
    
    def p1(self):
        self.build_rope(knots=2)                
        for move in self.input_list:
            direction,length = move.split()[0],int(move.split()[1])
            self.move_rope(direction,length)            
        self.p1_solution = len(self.knots[-1].positions)
        
    def p2(self):
        self.build_rope(knots=10)
        for move in self.input_list:
            direction,length = move.split()[0],int(move.split()[1])
            self.move_rope(direction,length)            
        self.p2_solution = len(self.knots[-1].positions)

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
        if P2_SAMPLE_INPUT:
            print(f"###############\nAOC 2022 DAY {DAY} P2 SAMPLE INPUT\n###############")
            print(P2_SAMPLE_INPUT.strip())
        print(f"\n###############\nAOC 2022 DAY {DAY} P1 SAMPLE SOLUTION\n###############")
        print(P1_SAMPLE_SOLUTION)
        print(f"\n###############\nAOC 2022 DAY {DAY} P2 SAMPLE SOLUTION\n###############")
        print(P2_SAMPLE_SOLUTION)
    

    if P1_SAMPLE_SOLUTION:            
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=SAMPLE_INPUT)
        sample.p1()
        if P1_SAMPLE_SOLUTION == sample.p1_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {sample.p1_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            puzzle = Puzzle(input_text=PUZZLE_INPUT)
            puzzle.p1()
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {puzzle.p1_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")
        
    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...\n")
        start_time = time()
        if P2_SAMPLE_INPUT:
            sample.input_text = P2_SAMPLE_INPUT
            sample.update_input_list()
        sample.p2()
        if P2_SAMPLE_SOLUTION == sample.p2_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {sample.p2_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            puzzle.p2()
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {puzzle.p2_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")
    
if __name__ == "__main__":
    main()
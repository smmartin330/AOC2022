import argparse
from time import time
import json
import numpy

DAY = 14

PUZZLE_TEXT = """
--- Day 14: Regolith Reservoir ---

The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?
"""

SAMPLE_INPUT = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

PUZZLE_INPUT = """
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
477,77 -> 477,81 -> 473,81 -> 473,84 -> 484,84 -> 484,81 -> 483,81 -> 483,77
497,15 -> 497,16 -> 502,16
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
498,52 -> 498,54 -> 490,54 -> 490,61 -> 508,61 -> 508,54 -> 501,54 -> 501,52
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
507,40 -> 512,40
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
498,52 -> 498,54 -> 490,54 -> 490,61 -> 508,61 -> 508,54 -> 501,54 -> 501,52
467,101 -> 471,101
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
487,128 -> 492,128
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
499,123 -> 503,123
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
470,95 -> 474,95
477,130 -> 482,130
481,104 -> 481,107 -> 475,107 -> 475,114 -> 494,114 -> 494,107 -> 486,107 -> 486,104
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
497,15 -> 497,16 -> 502,16
521,40 -> 526,40
477,77 -> 477,81 -> 473,81 -> 473,84 -> 484,84 -> 484,81 -> 483,81 -> 483,77
490,48 -> 490,49 -> 498,49 -> 498,48
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
481,132 -> 486,132
486,45 -> 486,46 -> 493,46 -> 493,45
499,135 -> 499,137 -> 495,137 -> 495,144 -> 505,144 -> 505,137 -> 502,137 -> 502,135
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
499,135 -> 499,137 -> 495,137 -> 495,144 -> 505,144 -> 505,137 -> 502,137 -> 502,135
481,104 -> 481,107 -> 475,107 -> 475,114 -> 494,114 -> 494,107 -> 486,107 -> 486,104
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
461,101 -> 465,101
490,48 -> 490,49 -> 498,49 -> 498,48
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
505,32 -> 510,32
461,97 -> 465,97
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
486,45 -> 486,46 -> 493,46 -> 493,45
455,101 -> 459,101
490,48 -> 490,49 -> 498,49 -> 498,48
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
498,52 -> 498,54 -> 490,54 -> 490,61 -> 508,61 -> 508,54 -> 501,54 -> 501,52
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
490,120 -> 494,120
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
498,52 -> 498,54 -> 490,54 -> 490,61 -> 508,61 -> 508,54 -> 501,54 -> 501,52
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
509,34 -> 514,34
477,77 -> 477,81 -> 473,81 -> 473,84 -> 484,84 -> 484,81 -> 483,81 -> 483,77
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
464,99 -> 468,99
493,123 -> 497,123
503,38 -> 508,38
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
498,52 -> 498,54 -> 490,54 -> 490,61 -> 508,61 -> 508,54 -> 501,54 -> 501,52
493,40 -> 498,40
499,135 -> 499,137 -> 495,137 -> 495,144 -> 505,144 -> 505,137 -> 502,137 -> 502,135
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
470,90 -> 477,90
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
495,132 -> 500,132
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
506,36 -> 511,36
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
483,126 -> 488,126
499,135 -> 499,137 -> 495,137 -> 495,144 -> 505,144 -> 505,137 -> 502,137 -> 502,135
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
476,99 -> 480,99
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
488,132 -> 493,132
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
477,77 -> 477,81 -> 473,81 -> 473,84 -> 484,84 -> 484,81 -> 483,81 -> 483,77
464,95 -> 468,95
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
498,52 -> 498,54 -> 490,54 -> 490,61 -> 508,61 -> 508,54 -> 501,54 -> 501,52
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
477,77 -> 477,81 -> 473,81 -> 473,84 -> 484,84 -> 484,81 -> 483,81 -> 483,77
486,45 -> 486,46 -> 493,46 -> 493,45
510,38 -> 515,38
473,101 -> 477,101
514,40 -> 519,40
493,117 -> 497,117
480,128 -> 485,128
496,120 -> 500,120
487,123 -> 491,123
499,135 -> 499,137 -> 495,137 -> 495,144 -> 505,144 -> 505,137 -> 502,137 -> 502,135
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
481,104 -> 481,107 -> 475,107 -> 475,114 -> 494,114 -> 494,107 -> 486,107 -> 486,104
481,104 -> 481,107 -> 475,107 -> 475,114 -> 494,114 -> 494,107 -> 486,107 -> 486,104
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
477,77 -> 477,81 -> 473,81 -> 473,84 -> 484,84 -> 484,81 -> 483,81 -> 483,77
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
481,104 -> 481,107 -> 475,107 -> 475,114 -> 494,114 -> 494,107 -> 486,107 -> 486,104
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
470,99 -> 474,99
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
502,34 -> 507,34
473,97 -> 477,97
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
491,130 -> 496,130
481,104 -> 481,107 -> 475,107 -> 475,114 -> 494,114 -> 494,107 -> 486,107 -> 486,104
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
477,77 -> 477,81 -> 473,81 -> 473,84 -> 484,84 -> 484,81 -> 483,81 -> 483,77
474,132 -> 479,132
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
499,36 -> 504,36
458,99 -> 462,99
500,40 -> 505,40
496,38 -> 501,38
498,52 -> 498,54 -> 490,54 -> 490,61 -> 508,61 -> 508,54 -> 501,54 -> 501,52
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
484,130 -> 489,130
497,29 -> 497,27 -> 497,29 -> 499,29 -> 499,25 -> 499,29 -> 501,29 -> 501,20 -> 501,29 -> 503,29 -> 503,19 -> 503,29 -> 505,29 -> 505,25 -> 505,29 -> 507,29 -> 507,24 -> 507,29
467,93 -> 471,93
479,101 -> 483,101
467,97 -> 471,97
499,135 -> 499,137 -> 495,137 -> 495,144 -> 505,144 -> 505,137 -> 502,137 -> 502,135
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
481,104 -> 481,107 -> 475,107 -> 475,114 -> 494,114 -> 494,107 -> 486,107 -> 486,104
494,170 -> 494,161 -> 494,170 -> 496,170 -> 496,168 -> 496,170 -> 498,170 -> 498,162 -> 498,170 -> 500,170 -> 500,161 -> 500,170 -> 502,170 -> 502,166 -> 502,170
500,157 -> 500,156 -> 500,157 -> 502,157 -> 502,156 -> 502,157 -> 504,157 -> 504,152 -> 504,157 -> 506,157 -> 506,155 -> 506,157 -> 508,157 -> 508,151 -> 508,157 -> 510,157 -> 510,153 -> 510,157
499,135 -> 499,137 -> 495,137 -> 495,144 -> 505,144 -> 505,137 -> 502,137 -> 502,135
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
513,36 -> 518,36
517,38 -> 522,38
481,74 -> 481,73 -> 481,74 -> 483,74 -> 483,67 -> 483,74 -> 485,74 -> 485,73 -> 485,74 -> 487,74 -> 487,65 -> 487,74
"""

P1_SAMPLE_SOLUTION = 24

P2_SAMPLE_SOLUTION = 93


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

    def pos(self, coordinate, x_offset=0, y_offset=0):
        x, y = coordinate[0] + x_offset, coordinate[1] + y_offset
        return self.gridmap[y][x]

    def pos_set(self, coordinate, new, x_offset=0, y_offset=0):
        x, y = coordinate[0] + x_offset, coordinate[1] + y_offset
        self.gridmap[y][x] = new
        self.gridmap_t[x][y] = new
        return True

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


class Puzzle:
    def __init__(self, input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split("\n")
        self.max_x = 0
        self.max_y = 0
        self.points = []

        for line in self.input_list:
            vertices = line.split(" -> ")
            for v in range(0, len(vertices) - 1):
                point_a = list(map(lambda x: int(x), vertices[v].split(",")))
                point_b = list(map(lambda x: int(x), vertices[v + 1].split(",")))

                if point_a[0] == point_b[0]:  # vertical line
                    x = point_a[0]
                    self.max_x = max(x, self.max_x)
                    for y in range(
                        min(point_a[1], point_b[1]), max(point_a[1], point_b[1]) + 1
                    ):
                        self.max_y = max(y, self.max_y)
                        self.points.append((x, y))
                if point_a[1] == point_b[1]:  # horizontal
                    y = point_a[1]
                    self.max_y = max(y, self.max_y)
                    for x in range(
                        min(point_a[0], point_b[0]), max(point_a[0], point_b[0]) + 1
                    ):
                        self.max_x = max(x, self.max_x)
                        self.points.append((x, y))
        self.cave_map = []
        for y in range(0, self.max_y + 2):
            self.cave_map.append(["."] * (self.max_x * 2))
        for point in self.points:
            self.cave_map[point[1]][point[0]] = "#"
        self.cave_map.append(["#"] * (self.max_x * 2))

    def drop_sand(self):
        sand_x = 500
        sand_y = 0

        while self.cave.pos((sand_x, sand_y)) != "o":
            # If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.
            if self.cave.pos((sand_x, sand_y), y_offset=1) == ".":
                # A unit of sand always falls down one step if possible.
                sand_y += 1
            else:  # If the tile immediately below is blocked (by rock or sand),
                # the unit of sand attempts to instead move diagonally one step down and to the left.
                if self.cave.pos((sand_x, sand_y), x_offset=-1, y_offset=1) == ".":
                    sand_y += 1
                    sand_x -= 1
                elif self.cave.pos((sand_x, sand_y), x_offset=1, y_offset=1) == ".":
                    # If that tile is blocked, the unit of sand attempts to instead move diagonally
                    # one step down and to the right.
                    sand_y += 1
                    sand_x += 1
                else:
                    # If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves.
                    self.cave.pos_set((sand_x, sand_y), new="o")
                    return sand_x, sand_y

    def p1(self):
        self.cave_map = []
        for y in range(0, self.max_y + 2):
            self.cave_map.append(["."] * (self.max_x * 2))
        for point in self.points:
            self.cave_map[point[1]][point[0]] = "#"
        self.cave_map.append(["#"] * (self.max_x * 2))
        self.cave = Grid(self.cave_map)
        i = 0
        while True:
            sand_x, sand_y = self.drop_sand()
            if sand_y >= self.max_y:
                self.p1_solution = i
                return
            i += 1

    def p2(self):
        del self.cave
        self.cave_map = []
        for y in range(0, self.max_y + 2):
            self.cave_map.append(["."] * (self.max_x * 2))
        for point in self.points:
            self.cave_map[point[1]][point[0]] = "#"
        self.cave_map.append(["#"] * (self.max_x * 2))
        self.cave = Grid(self.cave_map)
        i = 1
        while True:
            sand_x, sand_y = self.drop_sand()
            if sand_x == 500 and sand_y == 0:
                self.p2_solution = i
                return
            i += 1


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

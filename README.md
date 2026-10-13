# CIS 579 Programming Assignment 1: Eight Puzzle
Analysis of an 8 puzzle problem using Search Algorithms

## Background

Problem Statement:  The 8-Puzzle problem consists of a 3x3 grid with one blank space and eight numbered tiles.

Scope: The goal is to arrange the tiles in numerical order by sliding them into the empty space.

## Description of Code

The following Python code implements search algortihms that solves the 8-puzzle using six search algorithms.  The main objective is to find a sequence of legal moves that transforms an initial puzzle configuration into a specified goal state.  The program demonstrates state-space, graph traversal, uninformed & informed search, heuristics, path costs, and execution time of search algorithms.  

The Python code was derived from starter code; eightpuzzle.py, search.py, and util.py from UC Berkeley Pacman sample.  The files retain the UC Berkeley Pacman sample code structure and licensing notice (http://ai.berkeley.edu).  Therefore, these files were revised and modified to solve the 8-puzzle problem.

The Search algorithms explored in the code are the following;

- Breadth-First Search (BFS): Explores the shallowest nodes first using a FIFO queue to find the shortest path to the goal.

- Depth-First Search (DFS): Explores the deepest nodes first using a LIFO stack, backtracking when necessary, but does not guarantee the shortest path.

- Iterative Deepening Search (IDS): Repeatedly performs depth-limited DFS with increasing depth limits until the goal is found or the maximum depth is reached.

- Uniform Cost Search (UCS): Uses a priority queue to expand nodes with the lowest accumulated path cost, ensuring an optimal solution when move costs are positive.

- Greedy Best-First Search (GBS): Uses a heuristic function, such as Manhattan distance or misplaced tiles, to expand nodes estimated.

- A* Search: Uses a priority queue to expand the node with the lowest combined actual path cost g(n) and estimated remaining cost h(n) heuristic, using f(n) = g(n) + h(n) to find an optimal path to the goal.

Each search function returns five values; actions, states, cost, expanded, and elapsed.

The code will require use of Visual Studio code IDE for execution.  This code and the output files are available at Github under (https://github.com/algjor/8-Puzzle-Search) for reference.

## Files
- `eightpuzzle.py`: parses command-line arguments, defines puzzle states and goal, selects algorithm, and writes results to file.
- `search.py`: implements BFS, DFS, IDS, UCS, Greedy Best-First, A* with heuristics.
- `util.py`: original supplied utility module - which remained unchanged - to provides Stack, Queue and PriorityQueue.
- `output_BFS.txt`: generated search paths and metrics for Breadth First Search.
- `output_DFS.txt`: generated search paths and metrics for Depth First Search.
- `output_IDS.txt`: generated search paths and metrics for Iterative Deeping Search.
- `output_UCS.txt`: generated search paths and metrics for Uniform Cost Search.
- `output_GBS_misplaced.txt`: generated search paths and metrics for Greedy Best First Search with misplaced heuristic.
- `output_GBS_manhattan.txt`: generated search paths and metrics for Greedy Best First Search with manhattan heuristic.
- `output_A*_misplaced.txt`: generated search paths and metrics for A* Search with misplaced heuristic.
- `output_A*_manhattan.txt`: generated search paths and metrics for A* Search with manhattan heuristic..
- `report_file.pdf`: comparison table from the included example.

## Run
From the directory containing the three Python files:

```bash
python3 eightpuzzle.py --search BFS --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]'
python3 eightpuzzle.py --search DFS --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]'
python3 eightpuzzle.py --search IDS --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]'
python3 eightpuzzle.py --search UCS --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]'
python3 eightpuzzle.py --search GBS --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]' --heuristic misplaced
python3 eightpuzzle.py --search GBS --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]' --heuristic manhattan
python3 eightpuzzle.py --search 'A*' --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]' --heuristic misplaced
python3 eightpuzzle.py --search 'A*' --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]' --heuristic manhattan
```

Use `--search` with BFS, DFS, IDS, UCS, GBS, or A*. The Heuristic can be `misplaced` or `manhattan` for GBS and A*. Each command writes a separate output file in the current working directory. The hyphen (`-`) is the blank tile; `0` is also accepted. Use straight ASCII `--` dashes and normal quote characters.

## Implementation Premises
- Every move costs 1. Goal can be any valid 3x3 arrangement.
- Misplaced counts numbered tiles in incorrect positions. Manhattan sums numbered-tile row/column distances from goal positions. Blank excluded.
- Search depth in the output means *solution depth* (number of actions), not maximum explored depth.
- Nodes expanded counts states for which successors were generated. IDS totals expansions over all iterations.
- DFS has a 25-move depth limit to keep this simple path-storing implementation practical; it is a bounded DFS and may fail to find solutions deeper than 25. IDS has a 40-move maximum depth. These are implementation limitations, not guarantees of completeness for all 8-puzzles.
- Visited set prevents previously explored states from being revisited in BFS and DFS.
- Best dictionary allows UCS and A* to revisit a state when a lower-cost path is found.
- Execution times vary between machines/runs. The comparison in the report file is for the specific example start/goal boards above.

## Process Flow and Program Execution
Command-line input [input algorithm, IS, GS, heuristic] ->  `eightpuzzle.py` [parse input and construct the search problem] -> `EightPuzzleSearchProblem` -> calls algorithm in `search.py` -> `search.py` [executes BFS, DFS, IDS, UCS, GBS, or A*] invokes problem's getStartState, isGoalState and getSuccessors and uses data structures from `util.py` -> `eightpuzzle.py` saves path and metrics.

## Acknowledgment of AI Assistance

OpenAI's ChatGPT (2026) was used as a supplementary learning and programming assistance tool during the development of this code.  ChatGPT was consulted to further explain the search algorithms, including Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deepening Search (IDS), Uniform Cost Search (UCS), Greedy Best-First Search (GBS), and A* Search.

ChatGPT was also used to review Python programming concepts, provide suggestions for simplifying code, assist with debugging, and explain the implementation of search algorithms in eightpuzzle.py and search.py along with the heuristics.

Reference

OpenAI. (2026). ChatGPT [Large language model]. https://chatgpt.com/

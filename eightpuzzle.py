# eightpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import search
import argparse
import ast
import csv

# Module Classes

class EightPuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__(self, numbers):
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:]  # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(3):
            self.cells.append([])
            for col in range(3):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if row != 2:
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 2:
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise ValueError("Illegal Move")

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range(3):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class EightPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, puzzle, goal):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle
        self.goal = goal

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state == self.goal

    def getSuccessors(self, state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def parse_board(text):
    board = ast.literal_eval(text.replace('-', '0'))
    numbers = []

    for row in board:
        for number in row:
            numbers.append(number)

    return EightPuzzleState(numbers)

def run_search(problem, algorithm, heuristic):
    if algorithm == 'BFS':
        return search.breadthFirstSearch(problem)
    elif algorithm == 'DFS':
        return search.depthFirstSearch(problem)
    elif algorithm == 'IDS':
        return search.iterativeDeepeningSearch(problem)
    elif algorithm == 'UCS':
        return search.uniformCostSearch(problem)

    if heuristic == 'misplaced':
        h = search.misplacedHeuristic
    else:
        h = search.manhattanHeuristic

    if algorithm == 'GBS':
        return search.greedyBestFirstSearch(problem, h)
    elif algorithm == 'A*':
        return search.aStarSearch(problem, h)

    raise ValueError('Unknown search algorithm')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='8-puzzle search')
    parser.add_argument('--search', '-search', required=True,
                        choices=['BFS', 'DFS', 'IDS', 'UCS', 'GBS', 'A*'])
    parser.add_argument('--initial', '-initial', required=True, type=parse_board)
    parser.add_argument('--goal', '-goal', required=True, type=parse_board)
    parser.add_argument('--heuristic', '-heuristic', default='manhattan',
                        choices=['misplaced', 'manhattan'])
    args = parser.parse_args()

    puzzle = args.initial
    print('The initial puzzle:')
    print(puzzle)
    print('The goal puzzle:')
    print(args.goal)

    problem = EightPuzzleSearchProblem(puzzle, args.goal)
    path, states, cost, expanded, elapsed = run_search(
        problem, args.search, args.heuristic)
    
    name = args.search
    if args.search == 'GBS' or args.search == 'A*':
        name = name + '_' + args.heuristic
    filename = 'output_' + name + '.txt'
    lines = [name, '**********']

    if states:
        lines.append('The %s found a path of %d moves: %s' %
                     (args.search, len(path), str(path)))
        curr = puzzle
        lines.append('Initial puzzle:\n' + str(curr))
        i = 1
        for a in path:
            curr = curr.result(a)
            lines.append('After %d move%s: %s' % (i, ('', 's')[i > 1], a))
            lines.append(str(curr))
            i += 1

        # Full path as (state, action) -> ... -> (goal).
        steps = []
        for i in range(len(path)):
            steps.append('(%s, %s)' % (states[i].cells, path[i]))
        steps.append('(%s)' % states[-1].cells)
        lines.append('Path:')
        lines.append(' -> '.join(steps))
    else:
        lines.append('No solution was found')

    if states:
        lines.append('Path cost: %s' % cost)
        lines.append('Depth of the Search Tree (solution depth): %d' % len(path))
    else:
        lines.append('Path cost: N/A')
        lines.append('Depth of the Search Tree (solution depth): N/A')
    lines.append('Time taken: %.6f seconds' % elapsed)
    lines.append('Nodes expanded: %d' % expanded)
    report = '\n'.join(lines) + '\n'
    print(report)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(report)

    with open('comparison.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Algorithm', 'Path cost', 'Depth', 'Time (s)', 'Nodes expanded'])
        if states:
            writer.writerow([name, cost, len(path), '%.6f' % elapsed, expanded])
        else:
            writer.writerow([name, 'N/A', 'N/A', '%.6f' % elapsed, expanded])

    print('Saved %s and updated comparison.csv' % filename)

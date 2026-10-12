# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import time

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    started = time.perf_counter()
    stack = util.Stack()
    start = problem.getStartState()
    stack.push((start, [], [start], 0))
    visited = set()
    expanded = 0

    while not stack.isEmpty():
        state, actions, states, cost = stack.pop()
        if state in visited:
            continue
        if problem.isGoalState(state):
            return actions, states, cost, expanded, time.perf_counter() - started
        visited.add(state)
        expanded += 1
        for successor, action, stepCost in reversed(problem.getSuccessors(state)):
            if successor not in visited:
                stack.push((successor, actions + [action],
                            states + [successor], cost + stepCost))
    return [], [], 0, expanded, time.perf_counter() - started


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    started = time.perf_counter()
    queue = util.Queue()
    start = problem.getStartState()
    queue.push((start, [], [start], 0))
    visited = {start}
    expanded = 0

    while not queue.isEmpty():
        state, actions, states, cost = queue.pop()
        if problem.isGoalState(state):
            return actions, states, cost, expanded, time.perf_counter() - started
        expanded += 1
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                queue.push((successor, actions + [action],
                            states + [successor], cost + stepCost))
    return [], [], 0, expanded, time.perf_counter() - started


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    started = time.perf_counter()
    queue = util.PriorityQueue()
    start = problem.getStartState()
    queue.push((start, [], [start], 0), 0)
    best = {start: 0}
    expanded = 0

    while not queue.isEmpty():
        state, actions, states, cost = queue.pop()
        if cost > best[state]:
            continue
        if problem.isGoalState(state):
            return actions, states, cost, expanded, time.perf_counter() - started
        expanded += 1
        for successor, action, stepCost in problem.getSuccessors(state):
            newCost = cost + stepCost
            if newCost < best.get(successor, float('inf')):
                best[successor] = newCost
                queue.push((successor, actions + [action],
                            states + [successor], newCost), newCost)
    return [], [], 0, expanded, time.perf_counter() - started


def iterativeDeepeningSearch(problem: SearchProblem):
    """Repeated depth-limited DFS. Stops after all reachable states are exhausted."""
    started = time.perf_counter()
    start = problem.getStartState()
    expanded = 0

    for limit in range(32):
        stack = util.Stack()
        stack.push((start, [], [start], 0))
        while not stack.isEmpty():
            state, actions, states, cost = stack.pop()
            if problem.isGoalState(state):
                return actions, states, cost, expanded, time.perf_counter() - started
            if len(actions) == limit:
                continue
            expanded += 1
            for successor, action, stepCost in reversed(problem.getSuccessors(state)):
                if successor not in states:  # Avoid cycles on current path
                    stack.push((successor, actions + [action],
                                states + [successor], cost + stepCost))
    return [], [], 0, expanded, time.perf_counter() - started


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    total = 0

    for row in range(3):
        for col in range(3):
            tile = state.cells[row][col]

            if tile != 0:
                for goalRow in range(3):
                    for goalCol in range(3):
                        if tile == problem.goal.cells[goalRow][goalCol]:
                            total += abs(row - goalRow) + abs(col - goalCol)

    return total


def misplacedHeuristic(state, problem):
    misplaced = 0
    for row in range(3):
        for col in range(3):
            tile = state.cells[row][col]
            if tile != 0 and tile != problem.goal.cells[row][col]:
                misplaced += 1
    return misplaced


def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the state with the smallest heuristic estimate."""
    started = time.perf_counter()
    queue = util.PriorityQueue()
    start = problem.getStartState()
    queue.push((start, [], [start], 0), heuristic(start, problem))
    visited = set()
    expanded = 0

    while not queue.isEmpty():
        state, actions, states, cost = queue.pop()
        if state in visited:
            continue
        if problem.isGoalState(state):
            return actions, states, cost, expanded, time.perf_counter() - started
        visited.add(state)
        expanded += 1
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                queue.push((successor, actions + [action],
                            states + [successor], cost + stepCost),
                           heuristic(successor, problem))
    return [], [], 0, expanded, time.perf_counter() - started


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    started = time.perf_counter()
    queue = util.PriorityQueue()
    start = problem.getStartState()
    queue.push((start, [], [start], 0), heuristic(start, problem))
    best = {start: 0}
    expanded = 0

    while not queue.isEmpty():
        state, actions, states, cost = queue.pop()
        if cost > best[state]:
            continue
        if problem.isGoalState(state):
            return actions, states, cost, expanded, time.perf_counter() - started
        expanded += 1
        for successor, action, stepCost in problem.getSuccessors(state):
            newCost = cost + stepCost
            if newCost < best.get(successor, float('inf')):
                best[successor] = newCost
                queue.push((successor, actions + [action],
                            states + [successor], newCost),
                           newCost + heuristic(successor, problem))
    return [], [], 0, expanded, time.perf_counter() - started

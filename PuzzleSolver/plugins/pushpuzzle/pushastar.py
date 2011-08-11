"""
Uses AStar to solve a push puzzle.

"""

import math

from solver.utility.astar import AStar
from plugins.pushpuzzle import directions
    
####
#
# Distance functions
#
####

def manhattan_dist(state, a, b):
    """Get distance from a to b, moving in a grid."""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def direct_dist(state, a, b):
    """Get distance from a to b, moving in a direct line."""
    return math.sqrt(a*a + b*b)

def path_dist(state, a, b):
    """Get distance from a to b, moving through the given puzzle."""
    goal = (lambda s: s == b)
    heuristic = lambda s: manhattan_dist(s, b)
    def transitions(s):
        dirs = directions.adjacent(s).values()
        return [(p, 1) for p in dirs if state.cleared_square(p)]
    distance = AStar(a, goal, heuristic, transitions).solve()
    return None if distance == None else len(distance)-1
    
def transitions(state):
    for box in state.boxes:
        for dir in directions.DIRECTIONS:
            if state.can_move_box(box, dir):
                new_state = state.copy()
                new_state.boxes.remove(box)
                new_state.boxes.add(directions.adjacent(box, dir))
                new_state.player = box
                new_state.finalise()
                yield (new_state, 1) # TODO maybe work out real distance?

def solve(initial, heuristic=(lambda s: 0), solver=AStar, **kwargs):
    """Try to solve the puzzle from the initial state."""
    
    goal = (lambda state: state.goal())

    return solver(
        initial,
        goal,
        heuristic,
        transitions,
        **kwargs).solve()

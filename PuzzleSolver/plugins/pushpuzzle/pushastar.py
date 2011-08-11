"""
Uses AStar to solve a push puzzle.

"""

import math

from solver.utility.astar import AStar
from . import directions
from . import pathfinder
    
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
        return [(p, 1) for p in dirs if state.cleared_square(p) or p == b]
    distance = AStar(a, goal, heuristic, transitions).solve()
    return None if distance == None else len(distance)-1

####
#
# Heuristic functions
#
####

def matched_separation(separator, dist, state, boxprimary=True):
    """
    Use separator to find a sum of distance between matched boxes/targets.
    
    One of targets or boxes is the primary set and each item from this set will be
    matched against the other.
    
    """
    
    distance = (lambda a, b: dist(state, a, b))
    
    if boxprimary:
        return separator(state.boxes, state.base.targets, distance)
    else:
        return separator(state.base.targets, state.boxes, distance)

def blind_separation(primary, secondary, dist):
    """
    Get the sum of distances of primary items to their nearest secondary.
    
    We ignore the nearest targets of other boxes, so could use the same one twice.
    
    """
    
    return sum(min(dist(p, s) for s in secondary) for p in primary)

####
#
# Solver functions
#
####

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

    return recover_directions(solver(
        initial,
        goal,
        heuristic,
        transitions,
        **kwargs).solve())

def recover_directions(states):
    """Given a set of states, return the directions needed to create the complete path."""
    
    dirs = []
    
    for current, to in zip(states, states[1:]):
        box_from = current.boxes.difference(to.boxes)
        box_to = to.boxes.difference(current.boxes)
        assert len(box_from) == 1, "Too many boxes moved in one step."
        assert len(box_to) == 1, "Too many boxes moved in one step."
        
        box_from = next(iter(box_from))
        box_to = next(iter(box_to))
        assert manhattan_dist(current, box_from, box_to) == 1, "Box moved too far in one step"
        
        dir = directions.movement(box_from, box_to)
        player_push = directions.adjacent(box_from, directions.opposite(dir))
        
        dirs += pathfinder.find_path(current, player_push)
        dirs.append(dir)
        
    return dirs

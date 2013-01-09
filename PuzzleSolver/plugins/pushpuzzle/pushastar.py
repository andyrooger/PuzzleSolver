"""
Uses AStar to solve a push puzzle.

"""

# PuzzleSolver
# Copyright (C) 2010  Andy Gurden
#
#     This file is part of PuzzleSolver.
#
#     PuzzleSolver is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     PuzzleSolver is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PuzzleSolver.  If not, see <http://www.gnu.org/licenses/>.

import inspect

from thirdparty import munkres

from solver.utility.astar import AStar
from . import directions
from . import navigation

####
#
# Heuristic functions
#
####

def matched_separation(separator, dist):
    """
    Get a function that uses separator to find a sum of distance between matched
    boxes/targets.
    
    One of targets or boxes is the primary set and each item from this set will be
    matched against the other. Distance can take or not take state.
    
    """
    
    convert = len(inspect.getargspec(dist).args) > 2
    
    def sep(state):
        def distance(a, b):
            return dist(a, b, state) if convert else dist(a, b)
        return separator(state, distance)
    
    return sep

def blind_match(state, dist):
    """
    Get the sum of distances of primary items to their nearest secondary.
    
    We ignore the nearest targets of other boxes, so could use the same one twice.
    
    """
    
    try:
        return sum(
                   min(d for d in (dist(p, s) for s in state.base.targets) if d != None)
                   for p in state.boxes)
    except ValueError: # There was no accessible target
        return None

def far_match(state, dist):
    """Match pairs of items starting with the farthest primary item from anywhere."""
    
    p_set = set(state.boxes)
    s_set = set(state.base.targets)
    
    distances = {
        (p, s): dist(p, s)
        for p in p_set
        for s in s_set
    }
    
    big = state.base.height * state.base.width + 1 # larger than distance could possibly be
    distances = {k: (big if distances[k] == None else distances[k]) for k in distances}
    
    total = 0
    while p_set:
        closest_s = {
            p: min(s_set, key=(lambda s: distances[(p, s)]))
            for p in p_set
        }
        if any(distances[(p, closest_s[p])] == big for p in p_set):
            return None
        paired_p = max(p_set, key=(lambda p: distances[(p, closest_s[p])]))
        paired_s = closest_s[paired_p]
        total += distances[(paired_p, paired_s)]
        p_set.remove(paired_p)
        s_set.remove(paired_s)
    
    return total
    
def close_match(state, dist):
    """Match pairs of items starting with the closest."""

    p_set = set(state.boxes)
    s_set = set(state.base.targets)
    
    distances = {
        (p, s): dist(p, s)
        for p in p_set
        for s in s_set
    }
    big = state.base.height * state.base.width + 1
    keyfunc = (lambda k: big if distances[k] == None else distances[k])
    
    total = 0
    while p_set and s_set:
        closest = min( ((p, s) for p in p_set for s in s_set), key=keyfunc)
        if distances[closest] == None:
            return
        total += distances[closest]
        p_set.remove(closest[0])
        s_set.remove(closest[1])

    return total

_munkres = munkres.Munkres()

def munkres_value(state, dist):
    """Get the distance of the best matching between boxes and targets using the munkres algorithm."""
    
    global _munkres
    
    big = state.base.height * state.base.width + 1 # larger than distance could possibly be
    distances = [[dist(p, s) for p in state.boxes] for s in state.base.targets]
    distances = [[big if d == None else d for d in row] for row in distances]
    
    closest_match = [distances[p][s] for p,s in _munkres.compute(distances)]
    if big in closest_match:
        return None
    return sum(closest_match)

def shift_sum(state):
    """Align targets and boxes in a single dimensions and sum the distances in these dimensions."""

    # Actually only need to sort ordinates, not boxes
    box_x, box_y = zip(*state.boxes)
    target_x, target_y = zip(*state.base.targets)
    
    absdiff = (lambda x, y: abs(x-y))
    xs = map(absdiff, sorted(box_x), sorted(target_x))
    ys = map(absdiff, sorted(box_y), sorted(target_y))
    
    return sum(xs) + sum(ys)

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

    soln = solver(
        initial,
        goal,
        heuristic,
        transitions,
        **kwargs).solve()
    
    return recover_directions(soln) if soln else None

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
        assert navigation.manhattan_distance(box_from, box_to) == 1, "Box moved too far in one step"
        
        dir = directions.movement(box_from, box_to)
        player_push = directions.adjacent(box_from, directions.opposite(dir))
        
        dirs += navigation.player_path(current, player_push)
        dirs.append(dir)
    
    return dirs

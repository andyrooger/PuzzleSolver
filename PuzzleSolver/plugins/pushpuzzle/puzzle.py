"""
Contains the structures to store our puzzles in.

"""

class Puzzle:
    """Main class for storing our puzzles."""

    def __init__(self, h, w, initial = None):
        self.height = h
        self.width = w
        self.walls = set()
        self.targets = set()
        self.states = [initial] if initial != None else [PuzzleState()]

    def __getitem__(self, index):
        return self.states[index]

    # THINK ABOUT HOW TO EDIT THE STATES PROPERLY

class PuzzleState:
    """Information on parts of the puzzle that can change during the play."""

    def __init__(self):
        self.player = None
        self.boxes = set()

# - dimensions (stationary)
# - wall locations (stationary)
# - target locations (stationary)
# - box locations (mobile)
# - player location (mobile)
# * nothing can be in same place as a wall
# * player cannot be in same place as box
# * coords have to be inside dimensions

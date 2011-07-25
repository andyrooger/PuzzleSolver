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

    def inArea(self, x, y):
        """Are the given coordinates within our range?"""

        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True

    def valid(self, children=True):
        """Is this a valid setup?"""

        if not all(self.inArea(x, y) for x, y in self.walls.union(self.targets)):
            return False

        if children and not all(s.valid(self) for s in self.states):
            return False

        if self.walls.intersection(self.targets):
            return False

        if children and not all(len(self.states[0].boxes) == len(s.boxes) for s in self.states):
            return False

        return True

class PuzzleState:
    """Information on parts of the puzzle that can change during the play."""

    def __init__(self):
        self.player = None
        self.boxes = set()

    def valid(self, parent):
        if self.player == None or not parent.inArea(*self.player):
            return False

        if not all(parent.inArea(x, y) for (x, y) in self.boxes):
            return False

        if self.player in parent.walls.union(self.boxes):
            return False

        if self.boxes.intersection(parent.walls):
            return False

        return True

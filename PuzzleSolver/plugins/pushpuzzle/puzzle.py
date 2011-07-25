"""
Contains the structures to store our puzzles in.

"""

class Puzzle:
    """Main class for storing our puzzles."""

    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.walls = set()
        self.targets = set()
        self.states = [PuzzleState(self)]

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

        if children and not all(s.valid() for s in self.states):
            return False

        if self.walls.intersection(self.targets):
            return False

        if children and not all(len(self.states[0].boxes) == len(s.boxes) for s in self.states):
            return False

        return True

class PuzzleState:
    """Information on parts of the puzzle that can change during the play."""

    def __init__(self, parent):
        self.parent = parent
        self.player = None
        self.boxes = set()
        self.recordAccessibility()

    def valid(self):
        if self.player == None or not self.parent.inArea(*self.player):
            return False

        if not all(self.parent.inArea(x, y) for (x, y) in self.boxes):
            return False

        if self.player in self.parent.walls.union(self.boxes):
            return False

        if self.boxes.intersection(self.parent.walls):
            return False

        return True

    def recordAccessibility(self):
        """Create and record a set describing accessible coordinates from this state."""

        self.accessible = set()
        if self.player != None:
            self._expandAccessible(self.player)

    def _expandAccessible(self, pos):
        """Open up accessibility from the position pos."""

        if (self.parent.inArea(*pos) and
            pos not in self.accessible and
            pos not in self.parent.walls and
            pos not in self.boxes):

            self.accessible.add(pos)

            x, y = pos
            self._expandAccessible(self.parent, (x-1, y))
            self._expandAccessible(self.parent, (x+1, y))
            self._expandAccessible(self.parent, (x, y-1))
            self._expandAccessible(self.parent, (x, y+1))

    def goal(self):
        """Have we achieved our goal?"""

        return self.parent.targets.difference(self.boxes)

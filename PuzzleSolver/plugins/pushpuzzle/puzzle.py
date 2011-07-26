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
        self.curstate = 0

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

    def initial(self):
        """Get the initial puzzle state."""

        return self.states[0]

    def state(self):
        """Get the current puzzle state."""

        return self.states[self.curstate]

    def cursor(self, cur=None):
        if cur != None:
            if cur < 0 or cur >= len(self):
                raise IndexError
            self.curstate = cur
        return self.curstate

    def __len__(self):
        return len(self.states)

class PuzzleState:
    """Information on parts of the puzzle that can change during the play."""

    def __init__(self, parent):
        self.parent = parent
        self.player = None
        self.boxes = set()
        self.finalised = False

    # Allow finalisation
    def __setattr__(self, *vargs):
        if not hasattr(self, "finalised") or not self.finalised:
            super().__setattr__(*vargs)
        else:
            raise ValueError("Cannot edit a finalised puzzle state.")

    def finalise(self):
        self.recordAccessibility()
        self.finalised = True

    def valid(self):
        if self.player == None or not self.parent.inArea(*self.player):
            return False

        if len(self.boxes) != len(self.parent.targets):
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
            self._expandAccessible((x-1, y))
            self._expandAccessible((x+1, y))
            self._expandAccessible((x, y-1))
            self._expandAccessible((x, y+1))

    def goal(self):
        """Have we achieved our goal?"""

        return self.parent.targets.difference(self.boxes)

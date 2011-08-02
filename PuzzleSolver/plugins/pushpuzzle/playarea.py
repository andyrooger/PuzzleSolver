"""
Area for playing the Push Puzzle.

"""

#import tkinter
import tkinter.tix

from . import style
from . puzzle import Puzzle

KEYCODES = {111: "UP", 116: "DOWN", 113: "LEFT", 114: "RIGHT"}

class PlayArea(tkinter.tix.ScrolledWindow):
    """GUI component for playing push puzzles."""

    def __init__(self, master, puzzle, changecb=None):
        tkinter.tix.ScrolledWindow.__init__(self, master, scrollbar="auto")

        if not isinstance(puzzle, Puzzle) or not puzzle.valid():
            raise ValueError

        self.puzzle = puzzle
        self.changecb = changecb or (lambda: None)

        self.focus_set()
        self.bind("<Key>", self.keypress)

        self.createView()

    def setupTile(self, tile, pos):
        """Setup view for a single tile."""

        content = ("WALL" if pos in self.puzzle.walls else "EMPTY")
        if self.puzzle.state().player == pos:
            content = "PLAYER"
        if pos in self.puzzle.state().boxes:
            content = "BOX"
        target = (pos in self.puzzle.targets)
        tile.config(**style.tileStyle(content, target, separated=False))

    def createView(self):
        """Create the main part of the GUI."""

        self.buttons = []
        for y in range(self.puzzle.height):
            row = []
            for x in range(self.puzzle.width):
                tile = self.createTile((x,y))
                row.append(tile)
                tile.grid(sticky="nsew", row=y, column=x)
                self.setupTile(tile, (x, y))
            self.buttons.append(row)

    def updateView(self):
        """Update the look of each tile."""

        for y, row in enumerate(self.buttons):
            for x, tile in enumerate(row):
                self.setupTile(tile, (x, y))

    def createTile(self, pos):
        def click():
            self.clicked(pos)
        btn = tkinter.Button(self.window, relief=tkinter.FLAT, command=click)
        return btn

    def clicked(self, pos):
        """One of the tiles has been clicked."""

        player = self.puzzle.state().player
        dist = abs(pos[0] - player[0]) + abs(pos[1] - player[1])
        if dist == 1: # adjacent
            if pos[0] < player[0]:
                self.move("LEFT")
            elif pos[0] > player[0]:
                self.move("RIGHT")
            elif pos[1] < player[1]:
                self.move("UP")
            elif pos[1] > player[1]:
                self.move("DOWN")
            return

        if pos in self.puzzle.state().accessible:
            return # TODO - implement path finding

    def keypress(self, evt):
        """A key has been pressed."""

        if evt.keycode in KEYCODES:
            self.move(KEYCODES[evt.keycode])

    def move(self, direction):
        """Move the player if possible."""

        current = self.puzzle.state().player
        to = self.puzzle.adjacent(current, direction)

        if to == None:
            return False

        boxto = None

        if to not in self.puzzle.state().accessible: # not accessible
            if to not in self.puzzle.state().boxes: # and not pushing box
                return False
            boxto = self.puzzle.adjacent(to, direction)
            if boxto == None: # box not moving inside play area
                return False
            if boxto in self.puzzle.state().boxes or boxto in self.puzzle.walls: # box moving into resistance
                return False

        self.puzzle.addState()
        if boxto != None:
            self.puzzle.state().boxes.remove(to)
            self.puzzle.state().boxes.add(boxto)
        self.puzzle.state().player = to
        self.puzzle.state().finalise()
        self.updateView()
        self.changecb()
        return True

    def rewind(self):
        """Go to the beginning of the play area."""

        self.puzzle.cursor(0)
        self.updateView()

    def next(self):
        """Go to the next state. Return whether successful."""

        try:
            self.puzzle.cursor(self.puzzle.cursor()+1)
            self.updateView()
            return True
        except IndexError:
            return False

    def hasnext(self):
        """Do we have a next state?"""

        return self.puzzle.cursor()+1 < len(self.puzzle)

    def prev(self):
        """Go to previous state. Returns whether successful."""

        try:
            self.puzzle.cursor(self.puzzle.cursor()-1)
            self.updateView()
            return True
        except IndexError:
            return False

    def hasprev(self):
        """Do we have a previous state?"""

        return self.puzzle.cursor() > 0

    def metrics(self):
        """Return useful info about the puzzle state."""

        return {
            "move": self.puzzle.cursor(),
            "total": len(self.puzzle)
        }

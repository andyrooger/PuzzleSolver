"""
Area for playing the Push Puzzle.

"""

import tkinter

from tkinter import messagebox

from solver.utility.scrollable_window import ScrollableWindow

from . import style
from . puzzle import Puzzle
from . import pathfinder

KEYCODES = {111: "UP", 116: "DOWN", 113: "LEFT", 114: "RIGHT"}

class PlayArea(ScrollableWindow):
    """GUI component for playing push puzzles."""

    def __init__(self, master, puzzle, changecb=None):
        ScrollableWindow.__init__(self, master)

        if not isinstance(puzzle, Puzzle) or not puzzle.valid():
            raise ValueError

        self.puzzle = puzzle
        self.changecb = changecb or (lambda: None)
        self.automover_cb = None
        self.frozen = False

        self.focus_set()
        self.bind("<Key>", self.keypress)

        self.createView()
        # now all buttons are created we can centre on the player
        def update_centre(evt=None):
            self.update_idletasks()
            x, y = self.puzzle.state().player
            self.centre_on(self.buttons[y][x])
        self.bind('<Configure>', update_centre)

    def setupTile(self, tile, pos):
        """Setup view for a single tile."""

        content = ("WALL" if pos in self.puzzle.walls else "EMPTY")
        if self.puzzle.state().player == pos:
            content = "PLAYER"
            self.centre_on(tile)
        if pos in self.puzzle.state().boxes:
            content = "BOX"
        target = (pos in self.puzzle.targets)
        tile.config(**style.tile_style(content, target, separated=False))

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

        if self.frozen:
            return

        self.automove([])

        player = self.puzzle.state().player
        dist = abs(pos[0] - player[0]) + abs(pos[1] - player[1])
        if dist == 1: # adjacent
            if pos[0] < player[0]:
                self.automove(["LEFT"])
            elif pos[0] > player[0]:
                self.automove(["RIGHT"])
            elif pos[1] < player[1]:
                self.automove(["UP"])
            elif pos[1] > player[1]:
                self.automove(["DOWN"])
            return

        # Try long path find, will be None if not accessible
        # Don't worry about blocking, should be fast and we don't want the user to interact in between
        path = pathfinder.find_path(self.puzzle.state(), pos)
        self.automove(path or [])

    def keypress(self, evt):
        """A key has been pressed."""

        if self.frozen:
            return

        if evt.keycode in KEYCODES:
            self.automove([KEYCODES[evt.keycode]])

    def automove(self, directions):
        """Keep calling move at regular intervals until the list is completed."""
        
        if self.automover_cb != None:
            self.after_cancel(self.automover_cb)
        if directions:
            directions.reverse()
            self._automover(directions)
        
    def _automover(self, directions):
        """Performs the given moves at regular intervals."""
        
        dir = directions.pop()
        self.move(dir)
        
        if directions:
            self.automover_cb = self.after(100, self._automover, directions)

    def move(self, direction):
        """Move the player if possible."""

        if self.puzzle.state().goal():
            return

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

        if boxto == None:
            self.puzzle.add_state(to)
        else:
            self.puzzle.add_state()
            self.puzzle.state().boxes.remove(to)
            self.puzzle.state().boxes.add(boxto)
            self.puzzle.state().player = to
            self.puzzle.state().finalise()
            
        self.updateView()
        self.changecb()
        
        
        # don't actually need first if, but saves checking completely for goal
        if boxto in self.puzzle.targets:
            if self.puzzle.state().goal():
                messagebox.showinfo("Congratulations", "Well done, you completed the puzzle!")
        return True

    def freeze(self, frozen):
        self.frozen = frozen

    def rewind(self):
        """Go to the beginning of the play area."""

        self.automove([])
        self.puzzle.cursor(0)
        self.updateView()

    def next(self):
        """Go to the next state. Return whether successful."""
        
        self.automove([])
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

        self.automove([])
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
            "move": self.puzzle.cursor()+1,
            "total": len(self.puzzle),
            "targets": len(self.puzzle.targets),
            "filled": len(self.puzzle.targets.intersection(self.puzzle.state().boxes))
        }

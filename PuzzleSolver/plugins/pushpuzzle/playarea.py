"""
Area for playing the Push Puzzle.

"""

import tkinter

from tkinter import messagebox

from solver.utility.scrollable_window import ScrollableWindow

from . import style
from . puzzle import Puzzle
from . import navigation
from . import directions

_KEYCODES = {111: "UP", 116: "DOWN", 113: "LEFT", 114: "RIGHT"}

class PlayArea(ScrollableWindow):
    """GUI component for playing push puzzles."""

    def __init__(self, master, puzzle, changecb=None):
        ScrollableWindow.__init__(self, master)

        if not isinstance(puzzle, Puzzle) or not puzzle.valid():
            raise ValueError

        self._puzzle = puzzle
        self._changecb = changecb or (lambda: None)
        self._automover_cb = None
        self._frozen = False

        self.focus_set()
        self.bind("<Key>", self._keypress)

        self._create_view()
        # now all buttons are created we can centre on the player
        def update_centre(evt=None):
            self.update_idletasks()
            x, y = self._puzzle.state().player
            self.centre_on(self._buttons[y][x])
        self.bind('<Configure>', update_centre)

    def _setup_tile(self, tile, pos):
        """Setup view for a single tile."""

        content = ("WALL" if pos in self._puzzle.base.walls else "EMPTY")
        if self._puzzle.state().player == pos:
            content = "PLAYER"
            self.centre_on(tile)
        if pos in self._puzzle.state().boxes:
            content = "BOX"
        target = (pos in self._puzzle.base.targets)
        tile.config(**style.tile_style(content, target, separated=False))

    def _create_view(self):
        """Create the main part of the GUI."""

        self._buttons = []
        for y in range(self._puzzle.base.height):
            row = []
            for x in range(self._puzzle.base.width):
                tile = self._create_tile((x,y))
                row.append(tile)
                tile.grid(sticky="nsew", row=y, column=x)
                self._setup_tile(tile, (x, y))
            self._buttons.append(row)

    def _update_view(self):
        """Update the look of each tile."""

        for y, row in enumerate(self._buttons):
            for x, tile in enumerate(row):
                self._setup_tile(tile, (x, y))

    def _create_tile(self, pos):
        def click():
            self._clicked(pos)
        btn = tkinter.Button(self.window, relief=tkinter.FLAT, command=click)
        return btn

    def _clicked(self, pos):
        """One of the tiles has been clicked."""

        if self._frozen:
            return

        self.automove([])

        player = self._puzzle.state().player
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
        path = navigation.player_path(self._puzzle.state(), pos)
        self.automove(path or [])

    def _keypress(self, evt):
        """A key has been pressed."""

        if self._frozen:
            return

        if evt.keycode in _KEYCODES:
            self.automove([_KEYCODES[evt.keycode]])

    def automove(self, dirs):
        """Keep calling move at regular intervals until the list is completed."""
        
        if self._automover_cb != None:
            self.after_cancel(self._automover_cb)
        if dirs:
            dirs.reverse()
            self._automover(dirs)
        
    def _automover(self, dirs):
        """Performs the given moves at regular intervals."""
        
        dir = dirs.pop()
        self._move(dir)
        
        if dirs:
            self._automover_cb = self.after(100, self._automover, dirs)

    def _move(self, direction):
        """Move the player if possible."""

        if self._puzzle.state().goal():
            return

        current = self._puzzle.state().player
        to = directions.adjacent(current, direction)

        if not self._puzzle.base.in_area(to):
            return False

        boxto = None

        if to not in self._puzzle.state().accessible: # not accessible
            if to not in self._puzzle.state().boxes: # and not pushing box
                return False
            boxto = directions.adjacent(to, direction)
            if not self._puzzle.state().cleared_square(boxto): # box moving into resistance
                return False

        if boxto == None:
            self._puzzle.add_state(to)
        else:
            self._puzzle.add_state()
            self._puzzle.state().boxes.remove(to)
            self._puzzle.state().boxes.add(boxto)
            self._puzzle.state().player = to
            self._puzzle.state().finalise()
            
        self._update_view()
        self._changecb()
        
        
        # don't actually need first if, but saves checking completely for goal
        if boxto in self._puzzle.base.targets:
            if self._puzzle.state().goal():
                messagebox.showinfo("Congratulations", "Well done, you completed the puzzle!")
        return True

    def freeze(self, frozen):
        self.automove([])
        self._frozen = frozen

    def rewind(self):
        """Go to the beginning of the play area."""

        self.automove([])
        self._puzzle.cursor(0)
        self._update_view()

    def next(self):
        """Go to the next state. Return whether successful."""
        
        self.automove([])
        try:
            self._puzzle.cursor(self._puzzle.cursor()+1)
            self._update_view()
            return True
        except IndexError:
            return False

    def hasnext(self):
        """Do we have a next state?"""

        return self._puzzle.cursor()+1 < len(self._puzzle)

    def prev(self):
        """Go to previous state. Returns whether successful."""

        self.automove([])
        try:
            self._puzzle.cursor(self._puzzle.cursor()-1)
            self._update_view()
            return True
        except IndexError:
            return False

    def hasprev(self):
        """Do we have a previous state?"""

        return self._puzzle.cursor() > 0

    def get_puzzle(self):
        return self._puzzle

    def metrics(self):
        """Return useful info about the puzzle state."""

        return {
            "move": self._puzzle.cursor()+1,
            "total": len(self._puzzle),
            "targets": len(self._puzzle.base.targets),
            "filled": len(self._puzzle.base.targets.intersection(self._puzzle.state().boxes))
        }

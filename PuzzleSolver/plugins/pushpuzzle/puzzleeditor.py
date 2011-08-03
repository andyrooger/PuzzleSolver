"""
Editor frame for push puzzle.

"""

import tkinter

from . puzzle import Puzzle
from solver.utility.buttonselector import ButtonSelector
from solver.utility.scrollable_window import ScrollableWindow
from . import style

EDIT_MODES = ["EMPTY", "WALL", "TARGET", "BOX", "PLAYER"]

class PuzzleEditor(tkinter.Frame):
    def __init__(self, master, puzzle):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.modeselect = ButtonSelector(self)
        for mode in EDIT_MODES:
            self.modeselect.add("Edit " + mode.title(), mode, style.loadIcon(mode))
        self.modeselect.grid(sticky="nsew", row=1, column=0)

        self.creation = CreationArea(self, puzzle, getmode=self.modeselect.selection)
        self.creation.grid(sticky="nsew", row=0, column=0)

    def getPuzzle(self):
        return self.creation.getPuzzle()

    def saved(self):
        self.creation.saved()

    def changed(self):
        return self.creation.changed()

class CreationArea(ScrollableWindow):
    """Creation area, containing scrolled grid of tiles."""

    def __init__(self, master, puzzle, getmode=None):
        ScrollableWindow.__init__(self, master)

        if not isinstance(puzzle, Puzzle):
            raise ValueError("Type is not a puzzle: " + puzzle.__class__.__name__)

        self._changed = True

        self.getmode = getmode
        self.buttons = []
        for y in range(puzzle.height):
            row = []
            for x in range(puzzle.width):
                pos = (x, y)
                p = PuzzleTile(self.window, pos, clicked=self.click)
                row.append(p)
                p.grid(sticky="nsew", row=y, column=x)
            self.buttons.append(row)
        self.setContent(puzzle)

    def saved(self):
        self._changed = False

    def changed(self):
        return self._changed

    def setContent(self, puzzle):
        """Tell each tile what their content should be."""

        self.player = puzzle.initial().player

        for x,y in puzzle.walls:
            self.buttons[y][x].content("WALL")
        for x,y in puzzle.targets:
            self.buttons[y][x].target(True)
        for x,y in puzzle.initial().boxes:
            self.buttons[y][x].content("BOX")
        try:
            x,y = puzzle.initial().player
            self.buttons[y][x].content("PLAYER")
        except TypeError:
            pass # No player

    def click(self, tile, content=None, target=None):
        """On click callback for clicks on PuzzleTiles."""

        if content == None and target == None:
            mode = self.getmode()

            if mode == "EMPTY":
                self.click(tile, "EMPTY", None)
            elif mode == "PLAYER":
                self.click(tile, "PLAYER", None)
            elif mode == "WALL":
                self.click(tile, "EMPTY" if tile.content() == "WALL" else "WALL", None)
            elif mode == "BOX":
                self.click(tile, "EMPTY" if tile.content() == "BOX" else "BOX", None)
            elif mode == "TARGET":
                self.click(tile, None, not tile.target())
        else:
            self._changed = True
            if target != None:
                tile.target(target)

                if target and tile.content() == "WALL":
                    tile.content("EMPTY")
            if content != None:
                if self.player == tile.pos and content != "PLAYER":
                    self.player = None
                if content == "PLAYER" and self.player != tile.pos:
                    try:
                        x, y = self.player
                        self.buttons[y][x].content("EMPTY")
                    except TypeError:
                        pass # no previous player
                    self.player = tile.pos

                tile.content(content)

                if content == "EMPTY" or content == "WALL":
                    tile.target(False)

    def getPuzzle(self):
        p = Puzzle(*reversed(self.window.grid_size()))
        for row in self.buttons:
            for tile in row:
                if tile.content() == "PLAYER":
                    p.initial().player = tile.pos
                elif tile.content() == "BOX":
                    p.initial().boxes.add(tile.pos)
                elif tile.content() == "WALL":
                    p.walls.add(tile.pos)
                if tile.target():
                    p.targets.add(tile.pos)
        p.initial().finalise()
        return p

class PuzzleTile(tkinter.Button):
    """Single tile in the puzzle."""

    def __init__(self, master, pos, clicked=None):
        tkinter.Button.__init__(self, master, relief="flat", command=self.click)
        self.pos = pos
        self.clicked = clicked
        # could raise and propagate valueerror
        self.content("EMPTY", noupdate=True)
        self.target(False, noupdate=True)
        self.appearance()

    def target(self, t = None, noupdate=False):
        if t != None:
            self._target = t
            noupdate or self.appearance()
        return self._target

    def content(self, c = None, noupdate=False):
        if c != None:
            self._content = c
            noupdate or self.appearance()
        return self._content

    def appearance(self):
        """Set up appearance."""

        self.config(**style.tileStyle(self.content(), self.target()))

    def click(self):
        self.clicked(self)

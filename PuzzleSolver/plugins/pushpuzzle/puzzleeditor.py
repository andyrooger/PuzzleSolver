"""
Editor frame for push puzzle.

"""

import tkinter

from . analysisdialog import AnalysisDialog
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

        self._modeselect = ButtonSelector(self)
        for mode in EDIT_MODES:
            self._modeselect.add("Edit " + mode.title(), mode, style.load_icon(mode))
        self._modeselect.grid(sticky="nsew", row=1, column=0)

        self._creation = CreationArea(self, puzzle, getmode=self._modeselect.selection)
        self._creation.grid(sticky="nsew", row=0, column=0, columnspan=2)
        
        tkinter.Button(self, text="Analyse", command=self._analyse).grid(sticky="nsew", row=1, column=1)

    def get_puzzle(self):
        return self._creation.get_puzzle()

    def saved(self):
        self._creation.saved()

    def changed(self):
        return self._creation.changed()
    
    def _analyse(self):
        puzzle = self._creation.get_puzzle()
        self.wait_window(AnalysisDialog(self, puzzle))
        

class CreationArea(ScrollableWindow):
    """Creation area, containing scrolled grid of tiles."""

    def __init__(self, master, puzzle, getmode=None):
        ScrollableWindow.__init__(self, master)

        if not isinstance(puzzle, Puzzle):
            raise ValueError("Type is not a puzzle: " + puzzle.__class__.__name__)

        self._changed = True

        self._getmode = getmode
        self._buttons = []
        for y in range(puzzle.base.height):
            row = []
            for x in range(puzzle.base.width):
                pos = (x, y)
                p = PuzzleTile(self.window, pos, clicked=self._click)
                row.append(p)
                p.grid(sticky="nsew", row=y, column=x)
            self._buttons.append(row)
        self._update_tiles(puzzle)

    def saved(self):
        self._changed = False

    def changed(self):
        return self._changed

    def _update_tiles(self, puzzle):
        """Tell each tile what their content should be."""

        self._player = puzzle.initial().player

        for x,y in puzzle.base.walls:
            self._buttons[y][x].content("WALL")
        for x,y in puzzle.base.targets:
            self._buttons[y][x].target(True)
        for x,y in puzzle.initial().boxes:
            self._buttons[y][x].content("BOX")
        try:
            x,y = puzzle.initial().player
            self._buttons[y][x].content("PLAYER")
        except TypeError:
            pass # No player

    def _click(self, tile, content=None, target=None):
        """On click callback for clicks on PuzzleTiles."""

        if content == None and target == None:
            mode = self._getmode()

            if mode == "EMPTY":
                self._click(tile, "EMPTY", None)
            elif mode == "PLAYER":
                self._click(tile, "PLAYER", None)
            elif mode == "WALL":
                self._click(tile, "EMPTY" if tile.content() == "WALL" else "WALL", None)
            elif mode == "BOX":
                self._click(tile, "EMPTY" if tile.content() == "BOX" else "BOX", None)
            elif mode == "TARGET":
                self._click(tile, None, not tile.target())
        else:
            self._changed = True
            if target != None:
                tile.target(target)

                if target and tile.content() == "WALL":
                    tile.content("EMPTY")
            if content != None:
                if self._player == tile.pos and content != "PLAYER":
                    self._player = None
                if content == "PLAYER" and self._player != tile.pos:
                    try:
                        x, y = self._player
                        self._buttons[y][x].content("EMPTY")
                    except TypeError:
                        pass # no previous player
                    self._player = tile.pos

                tile.content(content)

                if content == "EMPTY" or content == "WALL":
                    tile.target(False)

    def get_puzzle(self):
        p = Puzzle(*reversed(self.window.grid_size()))
        for row in self._buttons:
            for tile in row:
                if tile.content() == "PLAYER":
                    p.initial().player = tile.pos
                elif tile.content() == "BOX":
                    p.initial().boxes.add(tile.pos)
                elif tile.content() == "WALL":
                    p.base.walls.add(tile.pos)
                if tile.target():
                    p.base.targets.add(tile.pos)
        p.initial().finalise()
        return p

class PuzzleTile(tkinter.Button):
    """Single tile in the puzzle."""

    def __init__(self, master, pos, clicked=None):
        tkinter.Button.__init__(self, master, relief="flat", command=(lambda: clicked(self)))
        self.pos = pos
        # could raise and propagate valueerror
        self.content("EMPTY", noupdate=True)
        self.target(False, noupdate=True)
        self._appearance()

    def target(self, t = None, noupdate=False):
        if t != None:
            self._target = t
            noupdate or self._appearance()
        return self._target

    def content(self, c = None, noupdate=False):
        if c != None:
            self._content = c
            noupdate or self._appearance()
        return self._content

    def _appearance(self):
        """Set up appearance."""

        self.config(**style.tile_style(self.content(), self.target()))

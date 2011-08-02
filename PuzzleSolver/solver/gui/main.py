"""
Contains the main window for the puzzle solver.

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

#import tkinter
import tkinter.tix

import solver.state

from . controlpanel import ControlPanel
from . puzzlechoice import PuzzleChoice
from . modechoice import ModeChoice
from . solverbutton import SolverButton
from . viewframe import ViewFrame

class SolverGUI(tkinter.Frame):
    """Main window for the puzzle solver."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctrlpanel = ControlPanel(self)
        ctrlpanel.grid(sticky="sew", row=2, column=0, columnspan=3)

        pzlChoice = PuzzleChoice(self)
        pzlChoice.grid(sticky="wns", row=1, column=0)

        mdChoice = ModeChoice(self)
        mdChoice.grid(sticky="nwe", row=0, column=0, columnspan=2)

        slv = SolverButton(self)
        slv.grid(sticky="nwe", row=0, column=2)

        vw = ViewFrame(self)
        vw.grid(sticky="nsew", row=1, column=1, columnspan=2)


def start_gui():
    APP_TITLE = "Puzzle Solver"

    root = tkinter.tix.Tk()
    root.title(APP_TITLE)

    solver.state.quitting.onChange(lambda _: root.destroy())

    def puzzle_change(n_puz):
        if n_puz == None:
            root.title(APP_TITLE)
        else:
            root.title(APP_TITLE + " - " + n_puz.name().title())
    solver.state.puzzle.onChange(puzzle_change)

    root.protocol("WM_DELETE_WINDOW", solver.state.quitting.attempt)
    appwin = SolverGUI(root)
    appwin.pack(expand=True, fill=tkinter.BOTH)
    appwin.mainloop()
#    root.destroy()

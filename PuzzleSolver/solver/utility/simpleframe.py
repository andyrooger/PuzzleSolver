"""
Contains a frame that allows a single child to be displayed at a time.

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

import tkinter

class SimpleFrame(tkinter.Frame):
    """Display a single child at any time."""

    def __init__(self, master, init=None):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = None
        self.set_content(init)

    def set_content(self, child=None):
        if self.content != None:
            self.content.grid_forget()
        self.content = child
        if self.content != None:
            self.content.grid(sticky="nsew", column=0, row=0)

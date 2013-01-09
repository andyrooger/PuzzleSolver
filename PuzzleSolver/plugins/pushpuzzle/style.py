"""
Helps with a consistent style and avoids loading images more than once.

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
import os.path

_icons = {}

def load_icon(name):
    """Load and record all available icons."""

    global _icons

    if name in _icons:
        return _icons[name]

    file = os.path.dirname(__file__)
    file = os.path.join(file, "resources", "images", name.lower() + ".gif")
    _icons[name] = tkinter.PhotoImage(file=file)
    return _icons[name]

def tile_style(content=None, target=None, separated=True):
    """Get the style for a certain tile."""

    conf = {"highlightthickness": 3}

    if content != None:
        conf["bg"] = "blue" if content == "WALL" else "white"
        conf["activebackground"] = "darkblue" if content == "WALL" else "gray"
        conf["image"] = (load_icon(content)
                         if content in ["PLAYER", "BOX"]
                         else load_icon("BLANK"))
    if target != None:
        if separated:
            conf["highlightbackground"] = "red" if target else "lightgray"
        else:
            conf["highlightbackground"] = "red" if target else "white"

    return conf

"""
Maintains state for the solver.

Sorry for globals, these are needed for access by the entire program.

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

from . import plugin

class WatchedValue:
    """Keeps track of an updateable value."""

    def __init__(self, default, *allowable):
        self._value = default
        self._during = set()
        self._callbacks = set()
        self._vitos = set()
        self.allowable = allowable if allowable else None
        self.default = default

    def during_change(self, callback):
        """Add a callback that is called as part of the changing process."""
        
        self._during.add(callback)

    def on_change(self, callback):
        """Add a callback to be called with new value on change."""

        self._callbacks.add(callback)

    def vito_change(self, callback):
        """Add a callback that can vito a change."""

        self._vitos.add(callback)
        
    def value(self):
        """Get the current value for this variable."""

        return self._value

    def change(self, to):
        """Try to change the variable and return whether successfull."""
        if self.allowable != None and to not in self.allowable:
            return False

        if any(vito(to) for vito in self._vitos):
            return False

        for cb in self._during:
            cb(to)

        for cb in self._callbacks:
            cb(to)
            
        self._value = to # after, so callbacks can still see the old value as well as the new
        return True

    def attempt(self):
        """
        Change the variable to default.

        This can be used when we do not care about the actual value, just
        whether it can be changed.

        """

        return self.change(self.default)

# GLOBAL STATE VARIABLES

puzzletype = WatchedValue(None)
mode = WatchedValue(None, "CREATE", "PLAY")
quitting = WatchedValue(None)
solving = WatchedValue(None) # Holds current solver or None
wiping = WatchedValue(None) # Wiping puzzle info

view = WatchedValue(plugin.DummyView())

def _update_puzzletype(p):
    _update_view(p, mode.value())
def _update_mode(m):
    _update_view(puzzletype.value(), m)
def _update_view(p, m):
    view.change(plugin.DummyView() if p == None or m == None else p.get(m))

puzzletype.on_change(_update_puzzletype)
mode.on_change(_update_mode)

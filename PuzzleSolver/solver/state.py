"""
Maintains state for the solver.

Sorry for globals, these are needed for access by the entire program.

"""

from . import plugin

class WatchedValue:
    """Keeps track of an updateable value."""

    def __init__(self, default, *allowable):
        self._value = default
        self._callbacks = set()
        self._vitos = set()
        self.allowable = allowable if allowable else None
        self.default = default

    def onChange(self, callback):
        """Add a callback to be called with new value on change."""

        self._callbacks.add(callback)

    def vitoChange(self, callback):
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

        for cb in self._callbacks:
            cb(to)
        self._value = to
        return True

    def attempt(self):
        """
        Change the variable to default.

        This can be used when we do not care about the actual value, just
        whether it can be changed.

        """

        return self.change(self.default)

# GLOBAL STATE VARIABLES

puzzle = WatchedValue(None)
mode = WatchedValue(None, "CREATE", "PLAY")
quitting = WatchedValue(None)
solving = WatchedValue(None) # Holds current solver or None
wiping = WatchedValue(None) # Wiping puzzle info

view = WatchedValue(plugin.DummyView())

def _update_puzzle(p):
    _update_view(p, mode.value())
def _update_mode(m):
    _update_view(puzzle.value(), m)
def _update_view(p, m):
    view.change(plugin.DummyView() if p == None or m == None else p.get(m))

puzzle.onChange(_update_puzzle)
mode.onChange(_update_mode)

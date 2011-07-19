"""
Maintains state for the solver.

Sorry for globals, these are needed for access by the entire program.

"""

class WatchedValue:
    """Keeps track of an updateable value."""

    def __init__(self, default, *allowable):
        self._value = None
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
        return self._value

    def change(self, to):
        if self.allowable != None and to not in self.allowable:
            return False

        if any(vito(to) for vito in self._vitos):
            return False

        for cb in self._callbacks:
            cb(to)
        self._value = to
        return True

# GLOBAL STATE VARIABLES

puzzle = WatchedValue(None, None)
mode = WatchedValue(None, "CREATE", "PLAY")
quitting = WatchedValue(False, True, False)
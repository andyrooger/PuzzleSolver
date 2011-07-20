"""
Dialogs and such for dumping and retriving puzzles to HDD.

"""

from tkinter import messagebox

class PuzzleSaver:
    """Allows saving/loading and querying of puzzles."""

    def __init__(self, view):
        self.view = view

    def check(self, master):
        if not self.view.changed():
            return True
        choice = messagebox.askyesnocancel(
            "I'm helping you",
            "Looks like you've changed things and not saved, do you want to now?",
            default=messagebox.CANCEL,
            icon=messagebox.WARNING,
            parent=master)
        if choice == True:
            return self.save(master)
        else:
            return (choice == False) # If cancelled then will be None

    def save(self, master):
        pass

    def load(self, master):
        pass

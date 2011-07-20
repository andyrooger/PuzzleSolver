"""
Dialogs and such for dumping and retriving puzzles to HDD.

"""

import solver.state

import pickle

from tkinter import messagebox
from tkinter import filedialog

class PuzzleSaver:
    """Allows saving/loading and querying of puzzles."""

    def __init__(self, view):
        self.view = view

    def check(self, master):
        if not self.view.changed():
            return True
        choice = messagebox.askyesnocancel(
            "I'm helping you",
            "Looks like you have changed things and not saved, do you want to now?",
            default=messagebox.CANCEL,
            icon=messagebox.QUESTION,
            parent=master)
        if choice == True:
            return self.save(master)
        else:
            return (choice == False) # If cancelled then will be None

    def save(self, master):
        ext = self.view.getExtension()
        puzzle = self.view.getPuzzle()
        if puzzle == None:
            messagebox.showinfo("Whoops", "Sorry, this puzzle is not saveable.")
            return False
        filename = filedialog.asksaveasfilename(
            defaultextension = ext,
            filetypes = [(solver.state.puzzle.value().name() + " file", ext)],
            parent = master)
        if not filename:
            return False
        if not filename.endswith(ext):
            filename += ext

        try:
            with open(filename, "wb") as file:
                pickle.dump(puzzle, file)
        except pickle.PickleError:
            messagebox.showwarning("Whoops", "Could not convert this puzzle to a saveable form.")
            return False
        except IOError:
            messagebox.showwarning("Whoops", "Could not write this puzzle to file.")
            return False
        self.view.saved()
        messagebox.showinfo("Finished", "Puzzle written successfully.")
        return True

    def load(self, master):
        pass

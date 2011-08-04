"""
Dialogs and such for dumping and retriving puzzles to HDD.

"""

import solver.state

import pickle

from tkinter import messagebox
from tkinter import filedialog

class PuzzleSaver:
    """Allows saving/loading and querying of puzzles."""

    def __init__(self):
        self._view = solver.state.view.value()

    def check(self, master):
        if not self._view.changed():
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
        ext = self._view.get_extension()
        puzzle = self._view.get_puzzle()
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
        self._view.saved()
        messagebox.showinfo("Finished", "Puzzle written successfully.")
        return True

    def load(self, master):
        ext = self._view.get_extension()
        if ext == None:
            messagebox.showinfo("Whoops", "Sorry, this puzzle type is not loadable.")
            return False
        filename = filedialog.askopenfilename(
            defaultextension = ext,
            filetypes = [(solver.state.puzzle.value().name() + " file", ext)],
            parent = master)
        if not filename:
            return False
        if not filename.endswith(ext):
            filename += ext

        try:
            with open(filename, "rb") as file:
                puzzle = pickle.load(file)
        except pickle.PickleError:
            messagebox.showwarning("Whoops", "The file was corrupted or of an unreadable format.")
            return False
        except IOError:
            messagebox.showwarning("Whoops", "The file could not be read.")
            return False
            
        return self._view.load(puzzle)

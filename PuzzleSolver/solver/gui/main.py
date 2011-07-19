"""
Contains the main window for the puzzle solver.

"""

import tkinter

class SolverGUI(tkinter.Frame):
    """Main window for the puzzle solver."""

    def __init__(self, master, pluginmodule):
        tkinter.Frame.__init__(self, master)
        self.pluginmodule = pluginmodule
        tkinter.Label(master, text="I am the puzzle solver.").pack()
        self.pack()

def start_gui(pluginmodule):
    root = tkinter.Tk()
    root.title("Puzzle Solver")
    appwin = SolverGUI(root, pluginmodule)
    appwin.mainloop()
#    root.destroy()

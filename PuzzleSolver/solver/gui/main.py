"""
Contains the main window for the puzzle solver.

"""

import tkinter

import solver.state

from . controlpanel import ControlPanel
from . puzzlechoice import PuzzleChoice
from . modechoice import ModeChoice
from . solverbutton import SolverButton

class SolverGUI(tkinter.Frame):
    """Main window for the puzzle solver."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctrlpanel = ControlPanel(self)
        ctrlpanel.setEnabled(False)
        ctrlpanel.grid(sticky="sew", row=2, column=0, columnspan=3)

        pzlChoice = PuzzleChoice(self)
        pzlChoice.grid(sticky="wns", row=1, column=0)

        mdChoice = ModeChoice(self)
        mdChoice.setEnabled(False)
        mdChoice.grid(sticky="nwe", row=0, column=0, columnspan=2)

        slv = SolverButton(self)
        slv.setEnabled(False)
        slv.grid(sticky="nwe", row=0, column=2)

        self.content = None
        self.setContent(tkinter.Label(self, text="No puzzle type is currently selected."))

    def setContent(self, frame):
        if self.content != None:
            self.content.grid_forget()
        self.content = frame
        self.content.grid(sticky="nsew", row=1, column=1, columnspan=2)

def start_gui(pluginmodule):
    class Dummy:
        def name(self):
            return "Lala"
    solver.state.puzzle.allowable = [Dummy() for a in range(10)]

    root = tkinter.Tk()
    root.title("Puzzle Solver")

    def try_quit():
        solver.state.quitting.change(True)

    def do_quit(quitting):
        if quitting:
            root.destroy()
    solver.state.quitting.onChange(do_quit)

    root.protocol("WM_DELETE_WINDOW", try_quit)
    appwin = SolverGUI(root)
    appwin.pack(expand=True, fill=tkinter.BOTH)
    appwin.mainloop()
#    root.destroy()

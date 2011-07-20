"""
Contains the main window for the puzzle solver.

"""

import tkinter

import solver.plugin
import solver.state

from . controlpanel import ControlPanel
from . puzzlechoice import PuzzleChoice
from . modechoice import ModeChoice
from . solverbutton import SolverButton
from . puzzlesaver import PuzzleSaver

class SolverGUI(tkinter.Frame):
    """Main window for the puzzle solver."""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctrlpanel = ControlPanel(self)
        ctrlpanel.grid(sticky="sew", row=2, column=0, columnspan=3)

        pzlChoice = PuzzleChoice(self)
        pzlChoice.grid(sticky="wns", row=1, column=0)

        mdChoice = ModeChoice(self)
        mdChoice.grid(sticky="nwe", row=0, column=0, columnspan=2)

        slv = SolverButton(self)
        slv.grid(sticky="nwe", row=0, column=2)

        self.content = None

        solver.state.view.onChange(self.onViewChange)
        solver.state.puzzle.change(None)

        solver.state.mode.vitoChange(self.vitoPuzzleOrModeChange)
        solver.state.puzzle.vitoChange(self.vitoPuzzleOrModeChange)

    def setContent(self, frame):
        if self.content != None:
            self.content.grid_forget()
        self.content = frame
        self.content.grid(sticky="nsew", row=1, column=1, columnspan=2)

    def vitoPuzzleOrModeChange(self, _):
        if solver.state.view.value() == None:
            return False
        return not PuzzleSaver(solver.state.view.value()).check(self)

    def onViewChange(self, view):
        frame = (
            tkinter.Label(self, text="No puzzle type is currently selected.")
            if view == None else view.getFrame(self))
        self.setContent(frame)

def start_gui(pluginmodule):
    solver.state.puzzle.allowable = solver.plugin.load_plugins(pluginmodule)
    solver.state.puzzle.allowable = [P() for P in solver.state.puzzle.allowable for i in range(10)]
    solver.state.puzzle.allowable += [None]

    APP_TITLE = "Puzzle Solver"

    root = tkinter.Tk()
    root.title(APP_TITLE)

    def try_quit():
        solver.state.quitting.change(True)

    def do_quit(quitting):
        if quitting:
            root.destroy()
    solver.state.quitting.onChange(do_quit)

    def puzzle_change(n_puz):
        if n_puz == None:
            root.title(APP_TITLE)
        else:
            root.title(APP_TITLE + " - " + n_puz.name().title())
    solver.state.puzzle.onChange(puzzle_change)

    root.protocol("WM_DELETE_WINDOW", try_quit)
    appwin = SolverGUI(root)
    appwin.pack(expand=True, fill=tkinter.BOTH)
    appwin.mainloop()
#    root.destroy()

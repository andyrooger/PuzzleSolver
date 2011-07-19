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
        ctrlpanel.grid(sticky="sew", row=2, column=0, columnspan=3)

        pzlChoice = PuzzleChoice(self)
        pzlChoice.grid(sticky="wns", row=1, column=0)

        mdChoice = ModeChoice(self)
        mdChoice.grid(sticky="nwe", row=0, column=0, columnspan=2)

        slv = SolverButton(self)
        slv.setEnabled(False)
        slv.grid(sticky="nwe", row=0, column=2)

        self.content = None

        solver.state.mode.onChange(self.onModeChange)
        solver.state.puzzle.onChange(self.onPuzzleChange)
        solver.state.puzzle.change(None)

    def setContent(self, frame):
        if self.content != None:
            self.content.grid_forget()
        self.content = frame
        self.content.grid(sticky="nsew", row=1, column=1, columnspan=2)

    def onPuzzleChange(self, type):
        frame = (type.get(solver.state.mode.value()).getFrame(self) if type != None
                else tkinter.Label(self, text="No puzzle type is currently selected."))
        self.setContent(frame)

    def onModeChange(self, mode):
        puzzle = solver.state.puzzle.value()
        frame = (puzzle.get(mode).getFrame(self) if puzzle != None
                else tkinter.Label(self, text="No puzzle type is currently selected."))
        self.setContent(frame)

def start_gui(pluginmodule):
    class Dummy:
        def __init__(self, i):
            self.i = i
        def name(self):
            return "Lala " + str(self.i)
        def get(self, mode):
            upper = self
            class Dummy2:
                def getFrame(self, master):
                    return tkinter.Label(master, text="Hello I am " + str(upper.i) + " and my mode is " + mode)
            return Dummy2()
    solver.state.puzzle.allowable = [Dummy(a) for a in range(10)] + [None]

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

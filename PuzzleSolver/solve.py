#!/usr/bin/env python3

import plugins

import solver.gui.main
import solver.state
import solver.plugin

if __name__ == "__main__":
    solver.state.puzzletype.allowable = solver.plugin.load_plugins(plugins)
    solver.state.puzzletype.allowable = [P() for P in solver.state.puzzletype.allowable]
    solver.state.puzzletype.allowable += [None]
    solver.gui.main.start_gui()

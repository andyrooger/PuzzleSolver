#!/usr/bin/env python3

import plugins

import solver.gui.main
import solver.state
import solver.plugin

if __name__ == "__main__":
    solver.state.puzzle.allowable = solver.plugin.load_plugins(plugins)
    solver.state.puzzle.allowable = [P() for P in solver.state.puzzle.allowable]
    solver.state.puzzle.allowable += [None]
    solver.gui.main.start_gui()

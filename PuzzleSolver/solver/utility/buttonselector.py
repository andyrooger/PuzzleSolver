"""
Toggle button group that works as a radio group.

"""

import tkinter

class ButtonSelector(tkinter.Frame):
    """Frame that allows adding any number of toggle buttons."""

    def __init__(self, master, vertical=False, selected=None):
        tkinter.Frame.__init__(self, master)

        self._selected = None
        self.buttons = set()
        self.cb_selected = selected

        self.vertical = vertical
        if vertical:
            self.grid_columnconfigure(0, weight=1)
        else:
            self.grid_rowconfigure(0, weight=1)

    def _select(self, item):
        for b, i in self.buttons:
            if i is item:
                b.config(relief=tkinter.SUNKEN)
            else:
                b.config(relief=tkinter.RAISED)
        self._selected = item

    def selection(self, select=None):
        """Get selection or force change."""

        if select != None:
            self._selected = select
            self._select(select)

        return self._selected

    def add(self, text, item):
        def callback():
            if self.cb_selected and self.selection() is not item:
                self.cb_selected(item)
            self._select(item)

        dims = self.grid_size()
        dims = dims[1] if self.vertical else dims[0]
        btn = tkinter.Button(self, text=text, command=callback)
        if self.vertical:
            self.grid_rowconfigure(dims, weight=1)
            btn.grid(row=dims, column=0, sticky="nsew")
        else:
            self.grid_columnconfigure(dims, weight=1)
            btn.grid(row=0, column=dims, sticky="nsew")
        self.buttons.add((btn, item))

    def setEnabled(self, enabled):
        state = tkinter.NORMAL if enabled else tkinter.DISABLED
        for b, i in self.buttons:
            b.configure(state=state)

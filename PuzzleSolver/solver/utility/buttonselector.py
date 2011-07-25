"""
Toggle button group that works as a radio group.

"""

import tkinter
from tkinter.tix import Balloon

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

    def selection(self, select=None):
        """Get selection or force change."""

        if select != None:
            self._select(select)
            self._selected = select

        return self._selected

    def add(self, text, item, icon=None):
        def callback():
            self._select(item)
            if self.cb_selected and self.selection() is not item:
                self.cb_selected(item)
            self._selected = item

        dims = self.grid_size()
        dims = dims[1] if self.vertical else dims[0]
        btn = tkinter.Button(self, text=text, image=icon, command=callback)
        if icon != None:
            Balloon(self.winfo_toplevel()).bind_widget(btn, msg=text)
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

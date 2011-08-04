"""
Scrollable window designed to replace tix.ScrolledWindow but programatically scrollable.

"""

import tkinter

class ScrollableWindow(tkinter.Frame):
    """Replacement for ScrolledWindow."""
    
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._vscrollbar = _AutoScrollbar(self, orient=tkinter.VERTICAL)
        self._vscrollbar.grid(row=0, column=1, sticky="wns")
        self._hscrollbar = _AutoScrollbar(self, orient=tkinter.HORIZONTAL)
        self._hscrollbar.grid(row=1, column=0, sticky="new")

        self._scroller = tkinter.Canvas(self,
                                       yscrollcommand=self._vscrollbar.set,
                                       xscrollcommand=self._hscrollbar.set)
        self._vscrollbar.config(command=self._scroller.yview)
        self._hscrollbar.config(command=self._scroller.xview)

        self.window = tkinter.Frame(self._scroller)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.window.grid(sticky="nsew")
        self.window.bind('<Configure>', self._frame_resized)
        
        self._scroller.create_window(0, 0, anchor="nw", window=self.window)
        self._scroller.grid(row=0, column=0)
        
    def _frame_resized(self, event=None):
        self.window.update_idletasks()
        _1, _2, w, h = self._scroller.bbox("all")
        self._scroller.config(scrollregion=self._scroller.bbox("all"), width=w, height=h)
        
    def centre_on(self, widget, x=None, y=None):
        """Centre the window on the given position within the widget. (MUST be an ancestor of window)"""
        
        if x == None:
            x = widget.winfo_width() // 2
        if y == None:
            y = widget.winfo_height() // 2
            
        while widget is not self.window:
            # Convert x, y to x, y in the parent
            parent = widget.master
            x += widget.winfo_x()
            y += widget.winfo_y()
            widget = parent
        # now widget is self.window
        # we have a wanted centre in self.window coordinates
        # find where we want top left
        x -= self._scroller.winfo_width() // 2
        y -= self._scroller.winfo_height() // 2
        # normalise
        x /= widget.winfo_width()
        y /= widget.winfo_height()
        # clamp
        x = max(0, min(x, 1))
        y = max(0, min(y, 1))
        # scroll
        self._scroller.xview_moveto(x)
        self._scroller.yview_moveto(y)

class _AutoScrollbar(tkinter.Scrollbar):
    """Copied from http://effbot.org/zone/tkinter-autoscrollbar.htm"""
    
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        tkinter.Scrollbar.set(self, lo, hi)
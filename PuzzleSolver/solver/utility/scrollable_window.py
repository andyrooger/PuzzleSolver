"""
Scrollable window designed to replace tix.ScrolledWindow but programatically scrollable.

"""

import tkinter

class ScrollableWindow(tkinter.Canvas):
    """Replacement for ScrolledWindow."""
    
    def __init__(self, master):
        tkinter.Canvas.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.vscrollbar = _AutoScrollbar(self, orient=tkinter.VERTICAL)
        self.vscrollbar.grid(row=0, column=1, sticky="wns")
        self.hscrollbar = _AutoScrollbar(self, orient=tkinter.HORIZONTAL)
        self.hscrollbar.grid(row=1, column=0, sticky="new")

        self.scroller = tkinter.Canvas(self,
                                       yscrollcommand=self.vscrollbar.set,
                                       xscrollcommand=self.hscrollbar.set)
        self.scroller.grid(row=0, column=0, sticky="nsew")
        self.vscrollbar.config(command=self.scroller.yview)
        self.hscrollbar.config(command=self.scroller.xview)

        self.window = tkinter.Frame(self.scroller)
        self.window.grid(row=0, column=0)
        
        self.window.bind('<Configure>', self._frame_resized)
        self.scroller.create_window(0, 0, anchor="nw", window=self.window)
        
    def _frame_resized(self, event=None):
        self.update_idletasks()
        self.scroller.config(scrollregion=self.scroller.bbox("all"))
        
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
        x -= self.scroller.winfo_width() // 2
        y -= self.scroller.winfo_height() // 2
        # normalise
        x /= widget.winfo_width()
        y /= widget.winfo_height()
        # clamp
        x = max(0, min(x, 1))
        y= max(0, min(y, 1))
        # scroll
        self.scroller.xview_moveto(x)
        self.scroller.yview_moveto(y)

class _AutoScrollbar(tkinter.Scrollbar):
    """Copied from http://effbot.org/zone/tkinter-autoscrollbar.htm"""
    
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        tkinter.Scrollbar.set(self, lo, hi)
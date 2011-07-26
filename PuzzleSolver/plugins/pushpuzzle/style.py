"""
Helps with a consistent style and avoids loading images more than once.

"""

import tkinter
import os.path

icons = {}

def loadIcon(name):
    """Load and record all available icons."""

    global icons

    if name in icons:
        return icons[name]

    file = os.path.dirname(__file__)
    file = os.path.join(file, "resources", "images", name.lower() + ".gif")
    icons[name] = tkinter.PhotoImage(file=file)
    return icons[name]

def tileStyle(content=None, target=None, separated=True):
    """Get the style for a certain tile."""

    conf = {"highlightthickness": 3}

    if content != None:
        conf["bg"] = "blue" if content == "WALL" else "white"
        conf["activebackground"] = "darkblue" if content == "WALL" else "gray"
        conf["image"] = (loadIcon(content)
                         if content in ["PLAYER", "BOX"]
                         else loadIcon("BLANK"))
    if target != None:
        if separated:
            conf["highlightbackground"] = "red" if target else "lightgray"
        else:
            conf["highlightbackground"] = "red" if target else "white"

    return conf

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

def tileStyle(content, target, separated=True):
    """Get the style for a certain tile."""

    bg = "blue" if content == "WALL" else "white"
    abg = "darkblue" if content == "WALL" else "gray"
    icon = (loadIcon(content)
            if content in ["PLAYER", "BOX"]
            else loadIcon("BLANK"))
    if separated:
        hbg = "red" if target else "lightgray"
    else:
        hbg = "red" if target else "white"

    return {"bg": bg, "image": icon,
            "highlightbackground": hbg,
            "highlightthickness": 3,
            "activebackground": abg}

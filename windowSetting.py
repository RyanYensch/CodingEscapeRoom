from tkinter import *
from screeninfo import get_monitors # type: ignore


def setCenter(window, w, h):
    monitors = get_monitors()
    primary = next((m for m in monitors if getattr(m, "is_primary", False)), None)
    
    if primary is None:
        primary = monitors[0]
    
    screenWidth, screenHeight = primary.width, primary.height
    originX, originY = primary.x, primary.y
    
    x = originX + (screenWidth - w) // 2
    y = originY + (screenHeight - h) // 2
    
    window.geometry(f"{w}x{h}+{x}+{y}")
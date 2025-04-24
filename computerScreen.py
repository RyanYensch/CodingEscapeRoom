from tkinter import *
from windowSetting import setCenter # type: ignore

class ComputerScreen():
    windowHeight = 700
    windowWidth = 700
    
    def __init__(self, title="Computer"):    
        self.window = Toplevel()
        self.window.title(title)
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
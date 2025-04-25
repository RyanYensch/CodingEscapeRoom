from tkinter import *
from windowSetting import setCenter


class LockInterface():
    windowHeight = 500
    windowWidth = 500
    
    
    def __init__(self, title = "Door Lock", numRows = 4, code = [1,2,3,4], locked = True):
        self.numRows = numRows
        self.title = title
        self.numRows = numRows
        self.code = code
        self.currCode = [0] * numRows
        self.locked = locked
    
    def openWindow(self):
        self.window = Toplevel()
        self.window.title(self.title)
        setCenter(self.window, self.windowWidth, self.windowHeight)
    
    def isLocked(self):
        return self.locked
    
    def getWindow(self):
        return self.window
    
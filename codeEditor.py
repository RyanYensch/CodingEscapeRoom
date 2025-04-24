from tkinter import *
from windowSetting import setCenter

class Editor():
    def __init__(self, title):
        self.window = Toplevel()
        self.window.title(title)
        
        setCenter(self.window, 700, 700)
        
    def getWindow(self):
        return self.window
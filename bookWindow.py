from tkinter import *
from tkinter.font import *
from windowSetting import setCenter

class Book():
    windowHeight = 700
    windowWidth = 700
    currPage = 0
    
    def __init__(self, title="Book", pagesText = [""], borderColour ="brown"):
        self.window = Toplevel()
        self.window.title(title)
        self.pages = pagesText
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
        
        self.screenFrame = Frame(self.window, width=self.windowWidth, height=self.windowHeight, bg="#f6eee3", 
                                 borderwidth=30, relief=SOLID, 
                                 highlightbackground=borderColour, highlightcolor=borderColour)
        self.screenFrame.pack(fill="both", expand=True)
        
        font = Font(family="Lucida Handwriting", size=12)
        self.leftPage = Text(self.screenFrame, wrap="word", font=font, bg="#f6eee3", fg="black", state=DISABLED)
        self.leftPage.pack(side="left", fill="both", expand=True)
        self.rightPage = Text(self.screenFrame, wrap="word", font=font, bg="#f6eee3", fg="black", state=DISABLED)
        self.rightPage.pack(side="right", fill="both", expand=True)
        
        self.fillPages()
    
    
    def fillPages(self):
        numPages = len(self.pages)
        self.leftPage.config(state=NORMAL)
        self.rightPage.config(state=NORMAL)
        self.leftPage.delete("1.0", END)
        self.rightPage.delete("1.0", END)
        self.leftPage.insert("1.0", self.pages[self.currPage])
        self.rightPage.insert("1.0", self.pages[self.currPage + 1] if self.currPage + 1 < numPages else "")
        self.leftPage.config(state=DISABLED)
        self.rightPage.config(state=DISABLED)
    
        
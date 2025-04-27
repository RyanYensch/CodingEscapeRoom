from tkinter import *
from tkinter.font import *
from windowSetting import setCenter

class Book():
    windowHeight = 800
    windowWidth = 1200
    
    
    def __init__(self, title="Book", pagesText = [""], startPage = 0, borderColour ="maroon"):
        self.window = Toplevel()
        self.window.title(title)
        self.pages = pagesText
        self.currPage = max(min((startPage // 2) * 2, (len(pagesText) // 2) * 2 - 2), 0)
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
        
        self.screenFrame = Frame(self.window, width=self.windowWidth, height=self.windowHeight, bg="#f6eee3",
                                 highlightbackground=borderColour, highlightcolor=borderColour,
                                 highlightthickness=30)
        self.screenFrame.pack(fill="both", expand=True)
        
        self.screenFrame.columnconfigure(0, weight=1)
        self.screenFrame.columnconfigure(1, weight=1)
        self.screenFrame.rowconfigure(0, weight=1)
        
        font = Font(family="Lucida Handwriting", size=12)
        self.leftPage = Text(self.screenFrame, wrap="word", font=font, bg="#f6eee3", fg="black", state=DISABLED)
        self.rightPage = Text(self.screenFrame, wrap="word", font=font, bg="#f6eee3", fg="black", state=DISABLED)
        self.leftPage.grid(row=0, column=0, sticky="nsew")
        self.rightPage.grid(row=0, column=1, sticky="nsew")
        
        
        small = Font(family="Lucida Handwriting", size=10)
        self.leftNum = Label(self.screenFrame, text="", font=small, bg="#f6eee3", anchor="w")
        self.rightNum = Label(self.screenFrame, text="", font=small, bg="#f6eee3", anchor="e")
        self.leftNum.grid(row=1, column=0, sticky="sw", padx=10, pady=5)
        self.rightNum.grid(row=1, column=1, sticky="se", padx=10, pady=5)
        
        self.leftPage.bind("<Button-1>", self.flipLeft)
        self.rightPage.bind("<Button-1>", self.flipRight)
        
        self.fillPages()
    
    def updateDisabledText(self, obj, text):
        obj.config(state=NORMAL)
        obj.delete("1.0", END)
        obj.insert("1.0", text)
        obj.config(state=DISABLED)
    
    def fillPages(self):
        numPages = len(self.pages)
        self.updateDisabledText(self.leftPage, self.pages[self.currPage])
        self.updateDisabledText(self.rightPage, self.pages[self.currPage + 1] if self.currPage + 1 < numPages else "")
        
        self.leftNum.config(text=str(self.currPage + 1))
        self.rightNum.config(text= str(self.currPage + 2) if self.currPage + 1 < numPages else "")
    
    def flipLeft(self, event=None):
        self.currPage = max(self.currPage - 2, 0)
        self.fillPages()
    
    def flipRight(self, event=None):
        numPages = len(self.pages)
        self.currPage = min(self.currPage + 2, numPages - 1 if numPages % 2 else numPages - 2)
        self.fillPages()
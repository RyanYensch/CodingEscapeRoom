from tkinter import *
from tkinter.font import *
from windowSetting import setCenter

def openFile(file, window):
    fileWindow= file.openFile()
    window.wait_window(fileWindow)
    

class FileScreen():
    windowWidth = 250
    windowHeight = 400
    
    def __init__(self, title = "File", text = ""):
        self.title = title
        self.text = text
    
    def openFile(self):
        self.window = Toplevel()
        self.window.title(self.title)
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
        
        font = Font(family="Arial", size=12)
        self.textScrollFrame = Frame(self.window)
        self.textScrollFrame.pack(side="right", fill="both", expand=True)

        self.textBox = Text(self.textScrollFrame, wrap="none", font=font, bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4")
        self.textBox.pack(side="left", fill="both", expand=True)

        self.scroll = Scrollbar(self.textScrollFrame, command=self.textBox.yview)
        self.scroll.pack(side="right", fill="y")
        
        self.textBox.delete("1.0", END)
        self.textBox.insert("1.0", self.text)
        self.textBox.bind("<KeyRelease>", lambda e: self.updateText())

        return self.window
    
    def updateText(self):
        self.text = self.textBox.get("1.0", END)

        
if __name__ == "__main__":
    window = Tk()
    
    file = FileScreen(text="Test\nTesting\nTest")
    
    window.mainloop()
from tkinter import *
from tkinter.font import *
from windowSetting import setCenter # type: ignore
import subprocess

class Editor():
    windowHeight = 700
    windowWidth = 700
    
    def __init__(self, title, filePath):
        self.window = Toplevel()
        self.window.title(title)
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
        self.filePath = filePath
        
        font = Font(family="Courier New", size=12)
        self.textBox = Text(self.window, wrap="none", font=font, bg="#1e1e1e", fg="#d4d4d4")
        self.textBox.pack(padx=10,pady=10)
        
        self.buttonFrame = Frame(self.window, width=self.windowWidth, height=self.windowHeight)
        self.buttonFrame.pack(padx=10, pady=10)
        
        self.compileButton = Button(self.buttonFrame, text="Compile", font=font, bg="#1e1e1e", fg="#d4d4d4", command=lambda: self.compileCode())
        self.saveButton = Button(self.buttonFrame, text="Save", font=font, bg="#1e1e1e", fg="#d4d4d4", command=lambda: self.saveFile())
        self.compileButton.grid(row=0, column=0)
        self.saveButton.grid(row=0, column=1)
        
        self.window.update()
        
    def getWindow(self):
        return self.window
    
    def setFile(self, imports, returnType, funcName, params):
        text = ""
        
        for imp in imports:
            text += f"#include <{imp}>\n"
        
        text += "using namespace std;\n\n"
        text += "\nclass Solution {\npublic:\n"
        text += f"    {returnType} {funcName}({params})"
        text += " {\n\n    }\n};"
        
        
        try:
            with open(self.filePath, 'w') as file:
                file.write(text)
        except:
            print(f"Failed to open file {self.filePath}")
    
    
    def readFile(self):
        with open(self.filePath, "r") as file:
            content = file.read()
            self.textBox.delete("1.0", END)
            self.textBox.insert("1.0", content)
            
    def saveFile(self):
        with open(self.filePath, "w") as file:
            file.write(self.textBox.get("1.0", END))
            
    def compileCode(self):
        self.saveFile()
        
        compileResults = subprocess.run(["g++", self.filePath])
        
        if (compileResults.returncode != 0):
            print("Compilation Failed")
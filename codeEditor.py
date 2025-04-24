from tkinter import *
from tkinter.font import *
from windowSetting import setCenter # type: ignore

class Editor():
    def __init__(self, title, filePath):
        self.window = Toplevel()
        self.window.title(title)
        
        setCenter(self.window, 700, 700)
        self.filePath = filePath
        
        font = Font(family="Courier New", size=12)
        self.textBox = Text(self.window, wrap="none", font=font, bg="#1e1e1e", fg="#d4d4d4")
        self.textBox.pack(padx=10,pady=10)
        
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
            
    def complieCode(self):
        pro
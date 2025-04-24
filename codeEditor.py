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
        
        self.testButton = Button(self.buttonFrame, text="Run Tests", font=font, bg="#1e1e1e", fg="#d4d4d4", command=lambda: self.runTests())
        self.saveButton = Button(self.buttonFrame, text="Save", font=font, bg="#1e1e1e", fg="#d4d4d4", command=lambda: self.saveFile())
        self.testButton.grid(row=0, column=0)
        self.saveButton.grid(row=0, column=1)
        
        self.outputTextBox = Text(self.window, wrap="word", font=font, bg="#1e1e1e", fg="#d4d4d4", state=DISABLED)
        self.outputTextBox.pack(padx=10,pady=10)
        
        self.window.update()
        
    def getWindow(self):
        return self.window
    
    def generateMain(self, className, funcName, returnType, tests):
        text = "int main(void) {\n"
        text += f"   {className} solution;\n"
        text += f"   {returnType} res;\n\n"
        
        for input, output in tests:
            text += f"   res = solution.{funcName}({input});\n"
            text += f"   if (res != {output}) "
            text += "{\n        cout << \"Input: \" << " + f"{input} << endl;\n"
            text += "        cout << \"Your Output: \" << res << endl;\n"
            text += "\n        cout << \"Expected Output: \" " + f"{output} << endl;\n"
            text += "       return -1;\n"
            text += "   }\n\n"
        
        text += "   return 0;\n}"
        
        return text

    
    def setFile(self, className, returnType, funcName, params, tests):
        text = ""
        self.main = self.generateMain(className, funcName, returnType, tests)
        
        text += "#include \"ALL_H_FILES.h\"\n"
        
        text += "using namespace std;\n\n"
        text += f"\nclass {className} "
        text += "{\npublic:\n"
        text += f"    {returnType} {funcName}({params})"
        text += " {\n\n    }\n};"
        
        
        try:
            with open(self.filePath, 'w') as file:
                file.write(text)
                file.write("\n\n" + self.main)
        except:
            print(f"Failed to open file {self.filePath}")
    
    
    def readFile(self):
        with open(self.filePath, "r") as file:
            content = file.read()
            mainIndex = content.find("int main")
            if mainIndex != -1:
                self.main = content[mainIndex:]
                content = content[:mainIndex]
            
            self.textBox.delete("1.0", END)
            self.textBox.insert("1.0", content)
            
    def saveFile(self):
        with open(self.filePath, "w") as file:
            file.write(self.textBox.get("1.0", END))
            file.write("\n\n" + self.main)
            
    def compileCode(self):
        self.saveFile()
        
        compileResults = subprocess.run(["g++", "-Wall", "-Werror", self.filePath, "-o", f"{self.filePath[:-4]}.o"],
                                        capture_output=True,
                                        text=True)
        
        if (compileResults.returncode != 0):
            return compileResults.stderr
        
        return None
    
    def updateOutputText(self, text):
        self.outputTextBox.config(state=NORMAL)
        self.outputTextBox.delete("1.0", END)
        self.outputTextBox.insert("1.0", text)
        self.outputTextBox.config(state=DISABLED)
    
    
    def runTests(self):
        compRes = self.compileCode()
        if compRes:
            self.updateOutputText(compRes)
            return False
        
        testResults = subprocess.run(f"./{self.filePath[:-4]}.o",
                                     capture_output=True,
                                     text=True)
        
        if testResults.stdout:
            self.updateOutputText("Test Failed:\n" + testResults.stdout)
            return False
        
        self.updateOutputText("All Tests Passed!")
        return True
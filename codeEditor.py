from tkinter import *
from tkinter.font import *
from windowSetting import setCenter # type: ignore
import subprocess
import re

def openEditor(editor, window):
    editorWindow= editor.openEditor()
    window.withdraw()
    window.wait_window(editorWindow)
    
    window.deiconify()

class Editor():
    windowHeight = 700
    windowWidth = 700
    completed = False
    numFailCompile = 0
    numFailTests = 0
    numRunTests = 0
    
    def __init__(self, title, filePath, passedMessage = ""):
        self.title = title
        self.filePath = filePath
        self.passedMessage = passedMessage
        
        
    def openEditor(self):
        self.window = Toplevel()
        self.window.title(self.title)
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
        self.filePath = self.filePath
        
        
        # Text editor features
        self.textEditorFrame = Frame(self.window, width=self.windowWidth, height=self.windowHeight)
        self.textEditorFrame.pack(fill="both", expand=True)
        
        font = Font(family="Courier New", size=12)
        
    
        self.lineNumbers = Text(self.textEditorFrame, width=4, bg="#2e2e2e", fg="#858585", font=font, state='disabled')
        self.lineNumbers.pack(side="left", fill="y")
        
        self.textScrollFrame = Frame(self.textEditorFrame)
        self.textScrollFrame.pack(side="right", fill="both", expand=True)

        self.textBox = Text(self.textScrollFrame, wrap="none", font=font, bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4")
        self.textBox.pack(side="left", fill="both", expand=True)
        tabWidth = font.measure(" " * 4)
        self.textBox.config(tabs=tabWidth)

        self.scroll = Scrollbar(self.textScrollFrame, command=self.textBox.yview)
        self.scroll.pack(side="right", fill="y")
        
        self.scroll.config(command=self.onScroll)
        self.textBox.config(yscrollcommand=self.onTextScroll)  
        
        
        self.textBox.bind("<KeyRelease>", self.onKeyRelease)
        self.textBox.bind("<MouseWheel>", self.updateLineNumbers)
        self.textBox.bind("<Button-1>", self.updateLineNumbers)
        self.textBox.bind("<Configure>", self.updateLineNumbers)
        self.updateLineNumbers()
        self.highlightSyntax()
        self.readFile()
        
        
        # Buttons
        self.buttonFrame = Frame(self.window, width=self.windowWidth, height=self.windowHeight // 10)
        self.buttonFrame.pack(padx=10, pady=10)
        
        self.testButton = Button(self.buttonFrame, text="Run Tests", font=font, bg="#1e1e1e", fg="#d4d4d4", command=lambda: self.runTests())
        self.saveButton = Button(self.buttonFrame, text="Save", font=font, bg="#1e1e1e", fg="#d4d4d4", command=lambda: self.saveFile())
        self.testButton.grid(row=0, column=0)
        self.saveButton.grid(row=0, column=1)
        
        
        # Output
        self.outputTextBox = Text(self.window, wrap="word", font=font, bg="#1e1e1e", fg="#d4d4d4", state=DISABLED)
        self.outputTextBox.pack(padx=10,pady=10, fill="both", expand=True)
        
        return self.window
    
    def generateMain(self, className, funcName, returnType, tests):
        text = "int main(void) {\n"
        text += f"   {className} solution;\n"
        text += f"   {returnType} res;\n\n"
        
        addQuotes = returnType != "string"
        
        for input, output in tests:
            text += f"   res = solution.{funcName}({input});\n"
            text += f"   if (res != {output}) "
            text += "{\n        cout << \"Input: \" << " + ('\"' if addQuotes else "") + f"{input}" + ('\"' if addQuotes else "") + "<< endl;\n"
            text += "        cout << \"Your Output: \" << res << endl;\n"
            text += "\n        cout << \"Expected Output: \" << "  + ('\"' if addQuotes else "") + f"{output}" + ('\"' if addQuotes else "") + "<< endl;\n"
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
        self.numRunTests += 1
        compRes = self.compileCode()
        if compRes:
            self.numFailCompile += 1
            self.numFailTests += 1
            self.updateOutputText(compRes)
            return
        
        testResults = subprocess.run(f"./{self.filePath[:-4]}.o",
                                     capture_output=True,
                                     text=True)
        
        if testResults.stdout:
            self.numFailTests += 1
            self.updateOutputText("Test Failed:\n" + testResults.stdout)
            return
        
        self.updateOutputText("All Tests Passed!\n" + self.passedMessage)
        self.completed = True
    
    def completedTests(self):
        return self.completed
    
    def onKeyRelease(self, event=None):
        self.updateLineNumbers()
        self.highlightSyntax()
        
    def updateLineNumbers(self, event=None):
        self.lineNumbers.config(state="normal")
        self.lineNumbers.delete("1.0", "end")

        first_visible_line = int(self.textBox.index("@0,0").split(".")[0])
        last_visible_line = int(self.textBox.index("@0,%d" % self.textBox.winfo_height()).split(".")[0])

        line_number_text = "\n".join(str(i) for i in range(first_visible_line, last_visible_line + 1))
        self.lineNumbers.insert("1.0", line_number_text)
        self.lineNumbers.config(state="disabled")
        
    def highlightSyntax(self):
        self.textBox.tag_remove("keyword", "1.0", END)
        self.textBox.tag_remove("string", "1.0", END)
        self.textBox.tag_remove("comment", "1.0", END)
        self.textBox.tag_remove("preprocessor", "1.0", END)
        self.textBox.tag_remove("number", "1.0", END)
        self.textBox.tag_remove("function", "1.0", END)

        content = self.textBox.get("1.0", END)

        # blue Keywords
        keywords = [
            "int", "return", "else", "if", "void", "for", "while", "do",
            "class", "public", "private", "protected", "using", "namespace",
            "static", "const", "constexpr", "virtual", "override", "true", "false",
            "bool", "char", "double", "float", "long", "short", "signed", "unsigned",
            "switch", "case", "break", "continue", "new", "delete", "try", "catch", "throw", "string",
            "vector", "unordered_map", "deque", "queue", "set", "unordered_set", "map", self.filePath[:-4], "std"
        ]
        for kw in keywords:
            for match in re.finditer(rf'\b{kw}\b', content):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.textBox.tag_add("keyword", start, end)
        self.textBox.tag_config("keyword", foreground="#569CD6")

        # Purple Strings
        for match in re.finditer(r'"[^"\n]*"|\'[^\']*\'', content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.textBox.tag_add("string", start, end)
        self.textBox.tag_config("string", foreground="#C586C0")

        # Green Comments
        for match in re.finditer(r'//.*?$|/\*.*?\*/', content, re.MULTILINE | re.DOTALL):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.textBox.tag_add("comment", start, end)
        self.textBox.tag_config("comment", foreground="#6A9955")

        # Orange Preprocessor
        for match in re.finditer(r'#\s*\w+', content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.textBox.tag_add("preprocessor", start, end)
        self.textBox.tag_config("preprocessor", foreground="#CE9178")

        # Red Numbers
        for match in re.finditer(r'\b\d+(\.\d+)?\b', content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.textBox.tag_add("number", start, end)
        self.textBox.tag_config("number", foreground="#D16969")

        # Yellow Function names (basic guess: word followed by `(`)
        for match in re.finditer(r'\b\w+(?=\s*\()', content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.textBox.tag_add("function", start, end)
        self.textBox.tag_config("function", foreground="#DCDCAA")
    
    def onScroll(self, *args):
        self.textBox.yview(*args)
        self.lineNumbers.yview(*args)
    
    def onTextScroll(self, *args):
        self.lineNumbers.yview_moveto(args[0])
        self.scroll.set(*args)
        self.updateLineNumbers()
        
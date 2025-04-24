from tkinter import *
from codeEditor import Editor
from windowSetting import setCenter # type: ignore


challenges = [{"className": "Password", 
               "returnType": "string", "funcName": "passwordDecode", "params" : "string s",
               "tests": [("\"skibidi\"", "\"ski\""), ("\"Heyyy\"", "\"Hey\"")]}]


def initialiseChallenges():
    for c in challenges:
        fileName = c["className"] + ".cpp"
        editor = Editor("", fileName)
        editor.setFile(c["className"], c["returnType"], c["funcName"], c["params"], c["tests"])
        editor.getWindow().destroy()

def generateHeaderFile(fileName):
    pass

def openEditor(window, title, className):
    filePath = className + ".cpp"
    editor = Editor(title, filePath)
    editor.readFile()
    editorWindow = editor.getWindow()
    window.withdraw()
    window.wait_window(editorWindow)
    
    window.deiconify()
    
    
    return editor
    
    
if __name__ == "__main__":  
    window = Tk()
    window.title("Escape Room")
    setCenter(window, 1000, 1000)
    
    initialiseChallenges()
    editor = openEditor(window, "Code Editor", "Password")
    
    window.mainloop()
    
    
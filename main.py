from tkinter import *
from codeEditor import Editor
from windowSetting import setCenter # type: ignore


def openEditor(window, title, filePath, newFile):
    editor = Editor(title, filePath)
    if newFile:
        editor.setFile(imports=["iostream", "vector", "algorithm", "string"], 
                    returnType="string", funcName="TestFunc", 
                    params="vector<int>& arr, string s")
    
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
    
    
    editor = openEditor(window, "Code Editor", filePath="temp.cpp", newFile=True)
    
    window.mainloop()
    
    
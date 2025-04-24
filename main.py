from tkinter import *
from codeEditor import Editor
from windowSetting import setCenter


def openEditor(window, title):
    editor = Editor(title)
    editorWindow = editor.getWindow()
    
    window.withdraw()
    window.wait_window(editorWindow)
    
    window.deiconify()
    
    
if __name__ == "__main__":  
    window = Tk()
    window.title("Escape Room")
    setCenter(window, 1000, 1000)
    
    
    openEditor(window, "hey")
    
    window.mainloop()
    
    
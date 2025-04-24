from tkinter import *
from codeEditor import Editor, openEditor
from windowSetting import setCenter # type: ignore
from computerScreen import ComputerScreen
from bookWindow import Book # type: ignore


challenges = [{"className": "Password", 
               "returnType": "string", "funcName": "passwordDecode", "params" : "string s",
               "tests": [("\"skibidi\"", "\"ski\""), ("\"Heyyy\"", "\"Hey\"")]}]


def initialiseChallenges():
    for c in challenges:
        fileName = c["className"] + ".cpp"
        editor = Editor("", fileName)
        editor.setFile(c["className"], c["returnType"], c["funcName"], c["params"], c["tests"])
        editor.getWindow().destroy()


    
    
if __name__ == "__main__":  
    window = Tk()
    window.title("Escape Room")
    setCenter(window, 1000, 1000)
    
    initialiseChallenges()
    # editor = openEditor(window, "Code Editor", "Password")
    # screen = ComputerScreen()
    # screen.setLoginPage()
    
    book = Book(pagesText=["I love Fortnite", "Ligma\nBalls", "Hey..."])
    
    window.mainloop()
    
    
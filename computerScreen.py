from tkinter import *
from tkinter import messagebox
from windowSetting import setCenter # type: ignore
from codeEditor import Editor, openEditor
from fileScreen import FileScreen, openFile # type: ignore
import random

def openComputer(computer, window):
    computerWindow = computer.openComputer()
    window.withdraw()
    window.wait_window(computerWindow)
    
    window.deiconify()

class ComputerScreen():
    windowHeight = 610
    windowWidth = 1080
    incorrectAttempts = 0
    numIconsRow = 5
    numIconsCol = 10
    files = {}
    
    def __init__(self, title="Computer", username="User", loggedIn = False, editors = {}, textFiles = []):    
        self.title = title
        self.username = username
        self.loggedIn = loggedIn
        self.editors = editors
        self.textFiles = textFiles
    
    
    def openComputer(self):
        self.window = Toplevel()
        self.window.title(self.title)
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
        
        self.screenFrame = Frame(self.window, width=self.windowWidth, height=self.windowHeight, bg="#2ad4ff", borderwidth=30, relief=SOLID)
        self.screenFrame.pack(fill="both", expand=True)
        
        if self.loggedIn:
            self.setDesktop()
        else:
            self.setLoginPage()
        
        return self.window
    
    def getLoggedIn(self):
        return self.loggedIn
    
    def setLoginPage(self):
        self.loginFrame = Frame(self.screenFrame, width=self.windowWidth, height=self.windowHeight, bg="#2ad4ff")
        self.loginFrame.pack(fill="both", expand=True)
        
        self.centerFrame = Frame(self.loginFrame, bg="#2ad4ff")
        self.centerFrame.place(relx=0.5, rely=0.5, anchor="center")

        self.usernameLabel = Label(self.centerFrame, text="Username:", font=("Arial", 14), bg="#2ad4ff")
        self.usernameLabel.grid(row=0, column=0, pady=10, sticky="e")
        self.usernameEntry = Entry(self.centerFrame, font=("Arial", 14), width=30)
        self.usernameEntry.grid(row=0, column=1, pady=10)

        self.passwordLabel = Label(self.centerFrame, text="Password:", font=("Arial", 14), bg="#2ad4ff")
        self.passwordLabel.grid(row=1, column=0, pady=10, sticky="e")
        self.passwordEntry = Entry(self.centerFrame, font=("Arial", 14), width=30, show="*")
        self.passwordEntry.grid(row=1, column=1, pady=10)

        self.loginButton = Button(self.centerFrame, text="Login", font=("Arial", 14), command=self.loginAction)
        self.loginButton.grid(row=2, column=0, columnspan=2, pady=20)
        
        
        
    def loginAction(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        
        if username != self.username:
            messagebox.showerror("Login Failed", "Incorrect Username")
            return
        
        if self.incorrectAttempts < 3:
            messagebox.showerror("Login Failed", "Incorrect Password")
            self.incorrectAttempts += 1
        
        if self.incorrectAttempts == 3:
            self.hackButton = Button(self.centerFrame, text="Hack Login", font=("Arial", 20), command=self.enableHack)
            self.hackButton.grid(row=3, column=0, columnspan=3, pady=30)

    def enableHack(self):
        editor = self.editors["Password"]
        openEditor(editor, self.window)
        self.loggedIn = editor.completedTests()
        if self.loggedIn:
            self.setDesktop()
    
    def clearFrame(self, frame):
        for w in frame.winfo_children():
            w.destroy()
    
    def setDesktop(self):
        self.clearFrame(self.screenFrame)
        self.canvas = Canvas(self.screenFrame, bg="#2ad4ff", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        fileDrawing = []
        
        
        for className in self.editors:
            if (className != "Password"):
                fileDrawing.append({"fileName": f"{className}.cpp", "isEditor" : True, "text" : ""})

        for fileName, text in self.textFiles:
            fileDrawing.append({"fileName": fileName, "isEditor" : False, "text" : text})
            
        fileDrawing += [None] * (self.numIconsCol * self.numIconsRow - len(fileDrawing))
        random.shuffle(fileDrawing)
        
        for i in range(len(fileDrawing)):
            if (not fileDrawing[i]):
                continue
            
            file = fileDrawing[i]
            
            self.drawFile(fileName=file["fileName"], 
                          row= i // self.numIconsCol, 
                          col = i % self.numIconsRow, 
                          isEditor=file["isEditor"], text=file["text"])
        
    def drawFile(self, fileName = "file.txt", row=0, col=0, text="", isEditor = False):
        screenL = 30
        screenR = self.windowWidth - 30
        screenB = self.windowHeight - 30
        screenT = 30
        
        fileW = (screenR - screenL) // (self.numIconsCol + 1)
        fileH = (screenB - screenT) // (self.numIconsRow + 1)
        gapX = ((screenR - screenL) - (fileW * self.numIconsCol)) // (self.numIconsCol + 1)
        gapY = ((screenB - screenT) - (fileH * self.numIconsRow)) // (self.numIconsRow + 1)
        
        fileX = screenL + gapX *(col + 1) + fileW * col
        fileY = screenT + gapY *(row + 1) + fileH * row
        
        tag = fileName[:-4] if isEditor else fileName
        
        self.canvas.create_rectangle(
            fileX + fileW // 6, fileY,
            fileX + fileW * 5 // 6, fileY + fileH * 3 // 4,
            fill="white", outline="black", tags=(tag))
        
        
        
        self.canvas.create_text(
                (fileX + fileW // 2), fileY + fileH * 7 // 8,
                text=fileName,
                anchor="center",
                tags=(tag)
            )
        
        if isEditor:
            self.canvas.tag_bind(tag, "<Button-1>", lambda e: openEditor(editor= self.editors[tag], window=self.window))
        else:
            self.files[tag] = FileScreen(title=fileName, text=text)
            self.canvas.tag_bind(tag, "<Button-1>", lambda e: openFile(file=self.files[tag], window=self.window))
        

if __name__ == "__main__":
    root = Tk()
    screen = ComputerScreen(loggedIn=True)
    screen.openComputer()
    screen.drawFile("fortnite.txt", 2, 2, "Man\nI\nLove\nFortnite")
    screen.drawFile(fileName="Password.cpp", row = 2, col=3)
        
    root.mainloop()
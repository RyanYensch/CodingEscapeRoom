from tkinter import *
from tkinter import messagebox
from tkinter.font import *
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
        self.clearFrame(self.screenFrame)
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
        
        for idx, slot in enumerate(fileDrawing):
            if slot is None:
                continue
            row = idx // self.numIconsCol
            col = idx %  self.numIconsCol
            self.drawFile(
                fileName=slot["fileName"],
                row=row,
                col=col,
                isEditor=slot["isEditor"],
                text=slot["text"]
            )
    
    def logout(self):
        self.loggedIn = False
        self.setLoginPage()
    
    def shuffle(self):
        self.setDesktop()
    
    def fitFontToWidth(self, text, fontFamily, maxWidth, maxSize):
        size = maxSize
        font = Font(family=fontFamily, size=size)
        while size > 1 and font.measure(text) > maxWidth:
            size -= 1
            font.configure(size=size)
        return font
    
    def drawFile(self, fileName = "file.txt", row=0, col=0, text="", isEditor = False):
        screenL = 50
        screenR = self.windowWidth - 80
        screenB = self.windowHeight - 80
        screenT = 10
        
        fileW = (screenR - screenL) // (self.numIconsCol + 2)
        fileH = (screenB - screenT) // (self.numIconsRow + 2)
        gapX = ((screenR - screenL) - (fileW * self.numIconsCol)) // (self.numIconsCol)
        gapY = ((screenB - screenT) - (fileH * self.numIconsRow)) // (self.numIconsRow)
        
        fileX = screenL + gapX *(col + 1) + fileW * col
        fileY = screenT + gapY *(row + 1) + fileH * row
        
        tag = fileName[:-4] if isEditor else fileName
        
        self.canvas.create_rectangle(
            fileX + fileW // 6, fileY,
            fileX + fileW * 5 // 6, fileY + fileH * 3 // 4,
            fill="white", outline="black", tags=(tag))
        
        
        font = self.fitFontToWidth(fileName, "Arial", fileW + gapX, 12)
        self.canvas.create_text(
                (fileX + fileW // 2), fileY + fileH * 7 // 8,
                text=fileName,
                font= font,
                anchor="center",
                tags=(tag)
            )
        
        fontLogo = Font(family="Arial", size=20)
        if isEditor:
            self.canvas.create_text(
                    (fileX + fileW // 2), fileY + fileH * 3 // 8,
                    text="{ }",
                    font= fontLogo,
                    anchor="center",
                    tags=(tag)
                )
            self.canvas.tag_bind(tag, "<Button-1>", lambda e: openEditor(editor= self.editors[tag], window=self.window))
        elif ".exe" in fileName:
            self.canvas.create_text(
                    (fileX + fileW // 2), fileY + fileH * 3 // 8,
                    text="X",
                    font= fontLogo,
                    anchor="center",
                    tags=(tag)
                )
            if ("Logout" in fileName):
                self.canvas.tag_bind(tag, "<Button-1>", lambda e: self.logout())
            else:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e: self.shuffle())
        else:
            txt = "P" if ".pdf" in fileName else "__\n__\n"
            self.canvas.create_text(
                    (fileX + fileW // 2), fileY + fileH * 3 // 8,
                    text=txt,
                    font= fontLogo,
                    anchor="center",
                    tags=(tag)
                )
            self.files[tag] = FileScreen(title=fileName, text=text)
            self.canvas.tag_bind(tag, "<Button-1>", lambda e: openFile(file=self.files[tag], window=self.window))
    

if __name__ == "__main__":
    root = Tk()
    screen = ComputerScreen(loggedIn=True)
    screen.openComputer()
    screen.drawFile("fortnite.txt", 2, 2, "Man\nI\nLove\nFortnite")
    screen.drawFile(fileName="Password.cpp", row = 2, col=3)
        
    root.mainloop()
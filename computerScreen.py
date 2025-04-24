from tkinter import *
from tkinter import messagebox
from windowSetting import setCenter # type: ignore
from main import openEditor


class ComputerScreen():
    windowHeight = 610
    windowWidth = 1080
    incorrectAttempts = 0
    
    def __init__(self, title="Computer", username="User"):    
        self.window = Toplevel()
        self.window.title(title)
        self.username = username
        
        setCenter(self.window, self.windowWidth, self.windowHeight)
    
    
    def setLoginPage(self):
        self.loginFrame = Frame(self.window, width=self.windowWidth, height=self.windowHeight, bg="#2ad4ff", borderwidth=30, relief=SOLID)
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
        editor = openEditor(self.window, "Code Editor", "Password")

if __name__ == "__main__":
    root = Tk()
    screen = ComputerScreen()
    screen.setLoginPage()
    root.mainloop()
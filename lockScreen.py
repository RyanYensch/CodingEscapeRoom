from tkinter import *
from windowSetting import setCenter


class LockInterface():
    windowHeight = 200
    windowWidth = 300
    
    
    def __init__(self, title = "Door Lock", numRows = 4, code = [1,2,3,4], locked = True):
        self.numRows = numRows
        self.title = title
        self.numRows = numRows
        self.code = code
        self.currCode = [0] * numRows
        self.locked = locked
    
    def openWindow(self):
        self.window = Toplevel()
        self.window.title(self.title)
        setCenter(self.window, self.windowWidth, self.windowHeight)
        
        self.canvas = Canvas(self.window, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.drawLock()
    
    def isLocked(self):
        return self.locked
    
    def getWindow(self):
        return self.window
    
    def drawLock(self):
        lockLeft = self.windowWidth // 8
        lockRight = (self.windowWidth * 7) // 8
        lockY = self.windowHeight - 10
        lockH = self.windowHeight // 2
        
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(
        lockLeft, lockY,
        lockRight, lockY - lockH,
        fill="#c3a55b", outline="black")
        
        pinwidth = (lockRight - lockLeft) // (self.numRows + 1)
        gap = ((lockRight - lockLeft) - (pinwidth * self.numRows)) // (self.numRows + 1)
        
        self.canvas.create_line(lockRight - gap // 3, lockY - lockH // 2, 
                                lockLeft + gap // 3, lockY - lockH // 2 + 1, 
                                fill="white", width=10)
        
        latchW = 15
        latchBottom = lockY - lockH
        connectorLeftX = lockLeft + latchW
        connectorRightX = lockRight - latchW
        diff = lockH // 5 if not self.locked else 0
        self.canvas.create_arc(connectorLeftX, latchBottom + lockH // 3 - diff, 
                               connectorRightX, latchBottom - lockH // 3 - diff, 
                               start= 0, extent=180, style="arc", width=latchW, 
                               outline="silver", tags=("latch")) 
        
        if not self.locked:
            self.canvas.create_line(connectorLeftX, latchBottom, 
                                    connectorLeftX, latchBottom - diff, 
                                    fill="silver", width=latchW, tags=("latch"))
        
        self.canvas.tag_bind(f"latch", "<Button-1>", lambda e: self.lock())
        
        for i in range(self.numRows):
            numLeft = lockLeft + gap * (i + 1) + pinwidth * i
            numRight = numLeft + pinwidth
            numY = lockY - 5
            numH = lockH - 5
            
            self.canvas.create_rectangle(
                numLeft, numY,
                numRight, numY - numH,
                fill="gray", outline="black")
            
            self.canvas.create_text(
                (numLeft + numRight) // 2, (2 * numY  - 1.5 *numH) // 2,
                text=f"    {(self.currCode[i] + 9) % 10}    ",
                anchor="center",
                tags=(f"prevNum{i}")
            )
            
            self.canvas.create_text(
                (numLeft + numRight) // 2, ((2 * numY  - 0.5 *numH))  // 2,
                text=f"    {(self.currCode[i] + 1) % 10}    ",
                anchor="center",
                tags=(f"nextNum{i}")
            )
            
            self.canvas.create_text(
                (numLeft + numRight) // 2, ((2 * numY  - numH))  // 2,
                text=f"    {self.currCode[i]}    ",
                anchor="center",
                tags=(f"number{i}")
            )
            
            self.canvas.tag_bind(f"number{i}", "<Button-1>", lambda e, i=i: self.increaseNum(i))
            self.canvas.tag_bind(f"number{i}", "<Button-3>", lambda e, i=i: self.decreaseNum(i))
            self.canvas.tag_bind(f"prevNum{i}", "<Button-1>", lambda e, i=i: self.decreaseNum(i))
            self.canvas.tag_bind(f"nextNum{i}", "<Button-1>", lambda e, i=i: self.increaseNum(i))

    def increaseNum(self, i):
        self.currCode[i] = (self.currCode[i] + 1) % 10
        self.drawLock()
    
    def decreaseNum(self, i):
        self.currCode[i] = (self.currCode[i] + 9) % 10
        self.drawLock()
        
    def lock(self):
        if not self.locked:
            self.locked = True
            self.drawLock()
            return
        
        for i in range(self.numRows):
            if (self.currCode[i] != self.code[i]):
                return
        
        self.locked = False
        self.drawLock()

if __name__ == "__main__":
    lock = LockInterface()
    lock.openWindow()
    lock.getWindow().mainloop()
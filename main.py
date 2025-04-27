from tkinter import *
from tkinter import messagebox
from codeEditor import Editor
from windowSetting import setCenter # type: ignore
from computerScreen import ComputerScreen, openComputer
from bookWindow import Book # type: ignore
from lockScreen import LockInterface # type: ignore
import random
import json
import time
import webbrowser
import os

with open('library.json', 'r', encoding='utf-8') as f:
    library = json.load(f)

with open('challenges.json', 'r', encoding='utf-8') as f:
    challenges = json.load(f)

with open('desktopFiles.json', 'r', encoding='utf-8') as f:
    desktopFiles = json.load(f)



lockCode = [random.randint(0, 9) for _ in range(len(challenges) - 1)]
lock = LockInterface(code=lockCode)


editors = {}
computer = None

startTime = time.time()
endTime = None



def openBook(idx):
    b = library[idx]
    Book(title=b["title"], pagesText=b["pages"], borderColour=b["colour"], startPage= b["startPage"] if "startPage" in b else 0)

def onComputerClick():
    openComputer(computer=computer, window=window)


def onDoorClick():
    if lock.isLocked():
        messagebox.showerror("Door", "The Door appears to be locked\nTry Opening by the Handle")
        return
    
    numTestsRun = 0
    numTestsFailed = 0
    numCompilesFailed = 0
    for editor in editors.values():
        stats = editor.getStats()
        numTestsRun += stats[0]
        numTestsFailed += stats[1]
        numCompilesFailed += stats[2]
    
    endTime = time.time()
    
    messagebox.showinfo("CONGRATS", "YOU MANAGED TO ESCAPE!!!!!")

    
    elapsedTime = endTime - startTime
    filePath = os.path.abspath('results.html')
    url = (
        f'file://{filePath}'
        f'?time={elapsedTime:.2f}'
        f'&testsRun={numTestsRun}'
        f'&testsFailed={numTestsFailed}'
        f'&compilesFailed={numCompilesFailed}'
    )
    
    webbrowser.open(url)
    window.destroy()
    quit()
    
def onDoorKnobClick():
    lock.openWindow()

def initialiseChallenges():
    for c in challenges:
        fileName = c["className"] + ".cpp"
        editor = Editor(title=fileName, filePath=fileName, 
                        passedMessage= f"Secret Code {c['codeId'] + 1}: {lockCode[c['codeId']]}" if c["codeId"] != -1 else "Password Cracked.\nWelcome Hacker")
        editor.setFile(c["className"], c["returnType"], c["funcName"], c["params"], c["tests"])
        
        editors[c["className"]] = editor
    
    global computer
    computer = ComputerScreen(title="Laptop",username="dave_pc", loggedIn=False, editors=editors, textFiles=desktopFiles)

def drawBookshelf(canvas, library, shelfLeft, shelfRight,
                   shelfTop, shelfHeight, numShelves = 1,
                   gap = 10, shelfMargin = 20):
    total_books = len(library)
    slots_per_shelf = (total_books + numShelves - 1) // numShelves
    total_slots = slots_per_shelf * numShelves

    slots = library[:] + [None] * (total_slots - total_books)
    random.shuffle(slots)

    shelf_width = shelfRight - shelfLeft
    bookW = int((shelf_width - gap * (slots_per_shelf - 1)) / slots_per_shelf)
    bookH = shelfHeight

    for sh in range(numShelves):
        y1 = shelfTop + sh * (shelfHeight + shelfMargin)
        y2 = y1 + bookH
        
        plankTh = 5
        canvas.create_rectangle(
            shelfLeft, y2,
            shelfRight, y2 + plankTh,
            fill="sienna", outline=""
        )


        for slot_idx in range(slots_per_shelf):
            book_info = slots[sh * slots_per_shelf + slot_idx]
            if book_info is None:
                continue 

            x1 = shelfLeft + slot_idx * (bookW + gap)
            x2 = x1 + bookW

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=book_info["colour"], outline="black",
                tags=(f"book_{sh}_{slot_idx}",)
            )
            
            canvas.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=book_info["title"],
                angle=90,
                anchor="center",
                font=("Lucida Handwriting", 10),
                tags=(f"book_{sh}_{slot_idx}",)
            )

            libIdx = library.index(book_info)
            canvas.tag_bind(f"book_{sh}_{slot_idx}", "<Button-1>", lambda e, idx = libIdx: openBook(idx))


def drawComputer(canvas, tableLeft, tableRight, tableY):
    tableTh = 20
    
    canvas.create_rectangle(
        tableLeft, tableY,
        tableRight, tableY + tableTh,
        fill="black", outline=""
    )
    
    monW, monH = 200, 120
    mx1 = (tableLeft + tableRight) // 2 - monW // 2
    my2 = tableY
    mx2 = mx1 + monW
    my1 = my2 - monH
    canvas.create_rectangle(
        mx1, my1, mx2, my2,
        fill="#2ad4ff", outline="black",
        tags=("computer",)
    )
    canvas.tag_bind("computer", "<Button-1>", lambda e: onComputerClick())
    
    
def drawDoor(canvas, doorLeft, doorTop, doorW, doorH):
    canvas.create_rectangle(
        doorLeft, doorTop,
        doorLeft + doorW, doorTop + doorH,
        fill="peru", outline="black",
        tags=("door",)
    )
    
    knob_r = 6
    kx = doorLeft + doorW - 15
    ky = doorTop + doorH // 2
    canvas.create_oval(
        kx - knob_r, ky - knob_r,
        kx + knob_r, ky + knob_r,
        fill="gold", outline="black",
        tags=("doorKnob",)
    )
    canvas.tag_bind("door", "<Button-1>", lambda e: onDoorClick())
    canvas.tag_bind("doorKnob", "<Button-1>", lambda e: onDoorKnobClick())    
    
    
    
    
    
if __name__ == "__main__":
    global window
    window = Tk()
    window.title("Escape Room")
    W, H = 1000, 500
    setCenter(window, W, H)
    window.resizable(False, False)
    window.minsize(W, H)
    window.maxsize(W, H)
    window.attributes("-fullscreen", False)

    initialiseChallenges()
    loggedIn = False

    canvas = Canvas(window, bg="#c3a55b", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    shelfMargin = 20
    shelfTop = 50
    shelfLeft = 20
    shelfRight = 600
    shelfHeight = 120
    numShelves = 3
    gap = 10

    drawBookshelf(canvas, library,
                   shelfLeft, shelfRight,
                   shelfTop, shelfHeight,
                   numShelves=numShelves,
                   gap=gap, shelfMargin=shelfMargin)

    tableY = shelfTop + numShelves * (shelfHeight + shelfMargin) + 20
    drawComputer(canvas, tableLeft=650, tableRight=950, tableY=tableY)

    drawDoor(canvas, doorLeft=920, doorTop=50, doorW=80, doorH=200)

    window.mainloop()
from tkinter import *
from codeEditor import Editor, openEditor
from windowSetting import setCenter # type: ignore
from computerScreen import ComputerScreen, openComputer
from bookWindow import Book # type: ignore
import random

challenges = [{"className": "Password", 
               "returnType": "string", "funcName": "passwordDecode", "params" : "string s",
               "tests": [("\"skibidi\"", "\"ski\""), ("\"Heyyy\"", "\"Hey\"")]}]


library = [
    {"title": "Fortnite", "pages": ["I love Fortnite"], "color": "skyblue"},
    {"title": "Ligma",     "pages": ["Ligma", "Balls", "sigma"],  "color": "lightgreen"},
    {"title": "Diary",     "pages": ["Dear Diary..."],    "color": "pink"},
    {"title": "Python",    "pages": ["import this"],      "color": "gold"},
    {"title": "Skibidi",   "pages": ["Skibidi Toilet!"],  "color": "coral"},
]

def openBook(idx):
    b = library[idx]
    Book(title=b["title"], pagesText=b["pages"], borderColour=b["color"])

def onComputerClick():
    global loggedIn
    computer = openComputer(window, title="Computer",username="Username", loggedIn=loggedIn)
    loggedIn = computer.getLoggedIn()

def onDoorClick():
    print("Door clicked!")
    
def onDoorKnobClick():
    print("Door Knob Clicked")

def initialiseChallenges():
    for c in challenges:
        fileName = c["className"] + ".cpp"
        editor = Editor("", fileName)
        editor.setFile(c["className"], c["returnType"], c["funcName"], c["params"], c["tests"])
        editor.getWindow().destroy()

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
        
        plank_th = 5
        canvas.create_rectangle(
            shelfLeft, y2,
            shelfRight, y2 + plank_th,
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
                fill=book_info["color"], outline="black",
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
        fill="sienna", outline=""
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
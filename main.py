from tkinter import *
from codeEditor import Editor, openEditor
from windowSetting import setCenter # type: ignore
from computerScreen import ComputerScreen, openComputer
from bookWindow import Book # type: ignore

challenges = [{"className": "Password", 
               "returnType": "string", "funcName": "passwordDecode", "params" : "string s",
               "tests": [("\"skibidi\"", "\"ski\""), ("\"Heyyy\"", "\"Hey\"")]}]


library = [
    {"title": "Fortnite", "pages": ["I love Fortnite"], "color": "skyblue"},
    {"title": "Ligma",     "pages": ["Ligma", "Balls"],  "color": "lightgreen"},
    {"title": "Diary",     "pages": ["Dear Diary..."],    "color": "pink"},
    {"title": "Python",    "pages": ["import this"],      "color": "gold"},
    {"title": "Skibidi",   "pages": ["Skibidi Toilet!"],  "color": "coral"},
]

def open_book(idx):
    b = library[idx]
    Book(title=b["title"], pagesText=b["pages"], borderColour=b["color"])

def on_computer_click():
    global loggedIn
    computer = openComputer(window, title="Computer",username="Username", loggedIn=loggedIn)
    loggedIn = computer.getLoggedIn()

def on_door_click():
    print("Door clicked!")

def initialiseChallenges():
    for c in challenges:
        fileName = c["className"] + ".cpp"
        editor = Editor("", fileName)
        editor.setFile(c["className"], c["returnType"], c["funcName"], c["params"], c["tests"])
        editor.getWindow().destroy()


    
    
if __name__ == "__main__":
    global window
    window = Tk()
    window.title("Escape Room")
    W, H = 1000, 300
    setCenter(window, W, H)
    window.resizable(False, False)
    window.minsize(W, H)
    window.maxsize(W, H)
    window.attributes("-fullscreen", False)

    initialiseChallenges()
    
    loggedIn = False

    # Create our drawing canvas
    canvas = Canvas(window, bg="#c3a55b", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # 1) Draw the bookshelf + books
    shelf_margin = 20
    shelf_top    = 50
    shelf_left   = shelf_margin
    shelf_right  = 600
    shelf_width  = shelf_right - shelf_left
    shelf_height = 180

    n_books = len(library)
    gap     = 10
    # compute each book's width so they fit evenly
    book_w = int((shelf_width - gap*(n_books-1)) / n_books)
    book_h = shelf_height

    for i, info in enumerate(library):
        x1 = shelf_left + i * (book_w + gap)
        y1 = shelf_top
        x2 = x1 + book_w
        y2 = y1 + book_h

        # the book rectangle
        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=info["color"], outline="black",
            tags=(f"book_{i}",)
        )
        # vertical (rotated) title
        canvas.create_text(
            (x1 + x2)//2, (y1 + y2)//2,
            text=info["title"],
            angle=90,
            anchor="center",
            font=("Lucida Handwriting",  ten:=10),
            tags=(f"book_{i}",)
        )
        # bind click
        canvas.tag_bind(
            f"book_{i}", "<Button-1>",
            lambda e, idx=i: open_book(idx)
        )

    # 2) Draw the computer on a table
    table_y    = shelf_top + shelf_height + 40
    table_left = 650
    table_right= 950
    table_th   = 20

    # table top
    canvas.create_rectangle(
        table_left, table_y,
        table_right, table_y + table_th,
        fill="sienna", outline=""
    )
    # monitor
    mon_w, mon_h = 200, 120
    mx1 = (table_left + table_right)//2 - mon_w//2
    my2 = table_y      # bottom of monitor
    mx2 = mx1 + mon_w
    my1 = my2 - mon_h
    canvas.create_rectangle(
        mx1, my1, mx2, my2,
        fill="#2ad4ff", outline="black",
        tags=("computer",)
    )
    canvas.tag_bind("computer", "<Button-1>", lambda e: on_computer_click())

    # 3) Draw the door on the far right
    door_left  = 920
    door_top   = 50
    door_w     = 80
    door_h     = 200

    canvas.create_rectangle(
        door_left, door_top,
        door_left+door_w, door_top+door_h,
        fill="peru", outline="black",
        tags=("door",)
    )
    # simple knob
    knob_r = 6
    kx = door_left + door_w - 15
    ky = door_top + door_h//2
    canvas.create_oval(
        kx-knob_r, ky-knob_r,
        kx+knob_r, ky+knob_r,
        fill="gold", outline="black",
        tags=("door",)
    )
    canvas.tag_bind("door", "<Button-1>", lambda e: on_door_click())

    window.mainloop()
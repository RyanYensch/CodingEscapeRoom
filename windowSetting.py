from tkinter import *


def setCenter(window, window_width, window_height):
    screen_height = window.winfo_screenheight()
    screen_width = window.winfo_screenwidth()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
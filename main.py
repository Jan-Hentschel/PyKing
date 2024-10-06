from tkinter import *
from tkinter import ttk
import os
import sys

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()
root.title("PyKing")

root.iconbitmap(resource_path(".\\dist\\Assets\\Icon.ico"))

frame = ttk.Frame(root, padding=10)
frame.grid()


root.mainloop()
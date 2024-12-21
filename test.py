import os
import sys
from tkinter import *
import tkinter as tk
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
root = Tk()
canvas = Canvas(root, width = 300, height = 300)
canvas.pack()
img = tk.PhotoImage(file=resource_path('.\\dist\\Assets\\LogoV1.3.png'))
canvas.create_image(0,0, anchor=NW, image=img)
mainloop()
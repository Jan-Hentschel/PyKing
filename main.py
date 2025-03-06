import tkinter as tk
from tkinter import *
from tkinter import ttk
from gui import root

from code_execution import executeCode
from virtual_environment import *
from filetree import loadTestFile, saveTestFile

if __name__ == "__main__":
    root.bind("<Control-z>", executeCode)
    root.bind("<Control-x>", change_grid_man)
    root.bind("<Control-w>", spawn_grid_elements)
    root.bind("<Control-b>", loadTestFile)
    root.bind("<Control-s>", saveTestFile)
    root.mainloop()


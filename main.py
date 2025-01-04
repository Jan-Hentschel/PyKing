import tkinter as tk
from tkinter import *
from tkinter import ttk
from gui import root

from code_execution import executeCode
from virtual_environment import *

if __name__ == "__main__":
    root.bind("z", executeCode)
    root.bind("x", change_grid_man)
    root.bind("w", spawn_grid_elements)
    root.mainloop()


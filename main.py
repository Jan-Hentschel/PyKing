import tkinter as tk
from tkinter import *
from tkinter import ttk
from gui import root

from code_execution import executeCode

if __name__ == "__main__":
    root.bind("z", executeCode)
    root.mainloop()


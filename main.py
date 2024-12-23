import tkinter as tk
from tkinter import *
from tkinter import ttk
from gui import root

from code_execution import executeCode
from virtual_environment import *

if __name__ == "__main__":
    root.bind("z", executeCode)
    root.bind("<Up>", forward_test)
    root.bind("<Right>", turn_right_test)
    root.bind("<Down>", eat_test)
    root.bind("<Left>", spit_test)
    root.mainloop()


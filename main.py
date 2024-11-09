import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys
from gui import root
from tests_and_debugging import debugPrints
from code_execution import executeCode



if __name__ == "__main__":
    root.bind("z", executeCode)
    #debugPrints()
    root.mainloop()


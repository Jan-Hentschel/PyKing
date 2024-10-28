import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import vertically_pained_window

# Terminal Textfeld erstellen (unten rechts)
terminal_widget = Text(vertically_pained_window, bg="#3F3F3F", fg="white", bd=0)

terminal_widget.insert(tk.END, "Terminal")
import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import vertically_pained_window

# Terminal Textfeld erstellen (unten rechts)
terminal_widget = Text(vertically_pained_window, bg="#3F3F3F", fg="white", bd=0, wrap="none")

#scrollbars
vertical_scrollbar = Scrollbar(terminal_widget, orient="vertical", cursor="arrow")
vertical_scrollbar.pack(side = RIGHT, fill=Y)
vertical_scrollbar.config(command = terminal_widget.yview)
terminal_widget["yscrollcommand"] = vertical_scrollbar.set


horizontal_scrollbar = Scrollbar(terminal_widget, orient="horizontal", cursor="arrow")
horizontal_scrollbar.pack(side = BOTTOM, fill=X)
horizontal_scrollbar.config(command = terminal_widget.xview)
terminal_widget["xscrollcommand"] = horizontal_scrollbar.set

terminal_widget.insert(tk.END, "Terminal")
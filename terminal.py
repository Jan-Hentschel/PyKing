import tkinter as tk
from tkinter import *
from tkinter import ttk
from utility import autoHiddenScrollbar

from gui import vertically_pained_window

terminal_frame = Frame(vertically_pained_window, bg="#3F3F3F", bd=0,)
terminal_frame.pack(fill=BOTH, expand=True)

terminal_and_horizontal_scrollbar_frame = Frame(terminal_frame, bg="#3F3F3F", bd=0,)
terminal_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)

# Terminal Textfeld erstellen (unten rechts)
terminal_widget = Text(terminal_and_horizontal_scrollbar_frame, bg="#3F3F3F", fg="white", bd=0, wrap="none")
terminal_widget.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)
#scrollbars
vertical_scrollbar = autoHiddenScrollbar(terminal_frame, terminal_widget, orient=VERTICAL, cursor="arrow")
vertical_scrollbar.pack(side = RIGHT, fill=Y)

horizontal_scrollbar = autoHiddenScrollbar(terminal_and_horizontal_scrollbar_frame, terminal_widget, orient=HORIZONTAL, cursor="arrow")
horizontal_scrollbar.pack(side = BOTTOM, fill=X)

vertical_scrollbar.config(command = terminal_widget.yview)
horizontal_scrollbar.config(command = terminal_widget.xview)

terminal_widget["xscrollcommand"] = horizontal_scrollbar.set
terminal_widget["yscrollcommand"] = vertical_scrollbar.set

terminal_widget.insert(tk.END, "Terminal")
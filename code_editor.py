import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import horizontally_paned_window, root

# Text-Feld für den Code Editor erstellen (mitte)
code_editor_widget = Text(horizontally_paned_window, bg="#3F3F3F", fg="white", bd=0, wrap="none")

#scrollbars
vertical_scrollbar = Scrollbar(code_editor_widget, orient="vertical", cursor="arrow")
vertical_scrollbar.pack(side = RIGHT, fill=Y)
vertical_scrollbar.config(command = code_editor_widget.yview)
code_editor_widget["yscrollcommand"] = vertical_scrollbar.set


horizontal_scrollbar = Scrollbar(code_editor_widget, orient="horizontal", cursor="arrow")
horizontal_scrollbar.pack(side = BOTTOM, fill=X)
horizontal_scrollbar.config(command = code_editor_widget.xview)
code_editor_widget["xscrollcommand"] = horizontal_scrollbar.set

code_editor_widget.insert(tk.END, "Code Editor")
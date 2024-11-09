import tkinter as tk
from tkinter import *
from tkinter import ttk


from gui import horizontally_paned_window, root


code_editor_frame = Frame(horizontally_paned_window, bg="#3F3F3F", bd=0,)
code_editor_frame.pack(fill=BOTH, expand=True)

code_editor_and_horizontal_scrollbar_frame = Frame(code_editor_frame, bg="#3F3F3F", bd=0,)
code_editor_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)

# Text-Feld für den Code Editor erstellen (mitte)
code_editor_widget = Text(code_editor_and_horizontal_scrollbar_frame, bg="#3F3F3F", fg="white", bd=0, wrap="none")
code_editor_widget.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)

from utility import autoHiddenScrollbar
#scrollbars
vertical_scrollbar = autoHiddenScrollbar(code_editor_frame, code_editor_widget, orient=VERTICAL, cursor="arrow")
vertical_scrollbar.pack(side = RIGHT, fill=Y)

horizontal_scrollbar = autoHiddenScrollbar(code_editor_and_horizontal_scrollbar_frame, code_editor_widget, orient=HORIZONTAL, cursor="arrow")
horizontal_scrollbar.pack(side = BOTTOM, fill=X)

horizontal_scrollbar.config(command = code_editor_widget.xview)
vertical_scrollbar.config(command = code_editor_widget.yview)

code_editor_widget["xscrollcommand"] = horizontal_scrollbar.set
code_editor_widget["yscrollcommand"] = vertical_scrollbar.set




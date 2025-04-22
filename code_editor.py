import tkinter as tk
from tkinter import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

from utility import AutoHiddenScrollbar

from gui import root

class CodeEditor:
    def __init__(self):
        self.frame = Frame(root.horizontally_paned_window, bg="#3F3F3F", bd=0,)
        self.frame.pack(fill=BOTH, expand=True)

        self.code_editor_and_horizontal_scrollbar_frame = Frame(self.frame, bg="#3F3F3F", bd=0,)
        self.code_editor_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Text-Feld für den Code Editor erstellen (mitte)
        self.text_widget = Text(self.code_editor_and_horizontal_scrollbar_frame, bg="#3F3F3F", fg="white", bd=0, wrap="none", insertbackground="#FFFFFF", selectbackground="#6F6F6F", tabs="40")
        self.text_widget.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)


        #scrollbars
        self.vertical_scrollbar = AutoHiddenScrollbar(self.frame, self.text_widget, orient=VERTICAL, cursor="arrow")
        self.vertical_scrollbar.pack(side = RIGHT, fill=Y)

        self.horizontal_scrollbar = AutoHiddenScrollbar(self.code_editor_and_horizontal_scrollbar_frame, self.text_widget, orient=HORIZONTAL, cursor="arrow")
        self.horizontal_scrollbar.pack(side = BOTTOM, fill=X)

        self.horizontal_scrollbar.config(command = self.text_widget.xview)
        self.vertical_scrollbar.config(command = self.text_widget.yview)

        self.text_widget["xscrollcommand"] = self.horizontal_scrollbar.set
        self.text_widget["yscrollcommand"] = self.vertical_scrollbar.set

    def load_into_editor(self, content):
        self.text_widget.delete(1.0,END)
        self.text_widget.insert(tk.END, content)

    def get_text_widget_content(self):
        return self.text_widget.get("1.0",END)
    
code_editor = CodeEditor()
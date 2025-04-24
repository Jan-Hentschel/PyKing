import tkinter as tk
from tkinter import ttk
from tkinter import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

from utility import *



class CodeEditor:
    def __init__(self, root):
        self.frame = DefaultTextFrame(root.horizontally_paned_window, line_numbers=TRUE, bg=root.primary_color, bd=0,)
        self.frame.pack(fill=BOTH, expand=True)

        self.percolator = Percolator(self.frame.text_widget)
        self.percolator.insertfilter(root.color_delegator)

    def load_into_editor(self, content):
        self.frame.text_widget.delete(1.0,END)
        self.frame.text_widget.insert(tk.END, content)

    def get_text_widget_content(self):
        return self.frame.text_widget.get("1.0",END)
    

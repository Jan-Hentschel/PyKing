import tkinter as tk
from tkinter import ttk
from tkinter import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

from utility import *



class CodeEditor:
    def __init__(self, root):
        self.frame = DefaultFrame(root.horizontally_paned_window, bg=root.primary_color, bd=0,)
        self.frame.pack(fill=BOTH, expand=True)

        self.code_editor_and_horizontal_scrollbar_frame = DefaultFrame(self.frame, bg=root.primary_color, bd=0,)
        self.code_editor_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)


        # Text-Feld für den Code Editor erstellen (mitte)
        self.text_widget = Text(self.code_editor_and_horizontal_scrollbar_frame, bg=root.primary_color, fg=root.foreground_color, bd=0, wrap="none", insertbackground=root.foreground_color, selectbackground="#6F6F6F", tabs="40")
        self.text_widget.pack(fill=BOTH, expand=True, side=TOP)
        
        #self.style.map("Scrollbar", background=[("selected", "#3F3F3F")])

        self.vertical_scrollbar = AutoHiddenScrollbar(self.frame, self.text_widget, style="My.Vertical.TScrollbar", orient=VERTICAL, cursor="arrow")
        self.vertical_scrollbar.pack(side = RIGHT, fill=Y)

        self.horizontal_scrollbar = AutoHiddenScrollbar(self.code_editor_and_horizontal_scrollbar_frame, self.text_widget, style="My.Horizontal.TScrollbar", orient=HORIZONTAL, cursor="arrow")
        self.horizontal_scrollbar.pack(side = BOTTOM, fill=X)

        self.horizontal_scrollbar.config(command = self.text_widget.xview)
        self.vertical_scrollbar.config(command = self.text_widget.yview)

        self.text_widget["xscrollcommand"] = self.horizontal_scrollbar.set
        self.text_widget["yscrollcommand"] = self.vertical_scrollbar.set

        self.percolator = Percolator(self.text_widget)
        self.percolator.insertfilter(root.color_delegator)

    def load_into_editor(self, content):
        self.text_widget.delete(1.0,END)
        self.text_widget.insert(tk.END, content)

    def get_text_widget_content(self):
        return self.text_widget.get("1.0",END)
    

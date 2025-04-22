import tkinter as tk
from tkinter import *
from utility import AutoHiddenScrollbar

from gui import vertically_pained_window
from options_handler import options_handler


class Terminal:

    def __init__(self):
        self.frame = Frame(vertically_pained_window, bg="#3F3F3F", bd=0,)
        self.frame.pack(fill=BOTH, expand=True)

        self.terminal_and_horizontal_scrollbar_frame = Frame(self.frame, bg="#3F3F3F", bd=0,)
        self.terminal_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Terminal Textfeld erstellen (unten rechts)
        self.text_widget = Text(self.terminal_and_horizontal_scrollbar_frame, bg="#3F3F3F", fg="white", bd=0, wrap="none")
        self.text_widget.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)
        #scrollbars
        self.vertical_scrollbar = AutoHiddenScrollbar(self.frame, self.text_widget, orient=VERTICAL, cursor="arrow")
        self.vertical_scrollbar.pack(side = RIGHT, fill=Y)

        self.horizontal_scrollbar = AutoHiddenScrollbar(self.terminal_and_horizontal_scrollbar_frame, self.text_widget, orient=HORIZONTAL, cursor="arrow")
        self.horizontal_scrollbar.pack(side = BOTTOM, fill=X)

        self.vertical_scrollbar.config(command = self.text_widget.yview)
        self.horizontal_scrollbar.config(command = self.text_widget.xview)

        self.text_widget["xscrollcommand"] = self.horizontal_scrollbar.set
        self.text_widget["yscrollcommand"] = self.vertical_scrollbar.set

    def show_current_directories(self, status ):
        self.text_widget.delete('1.0', END)
        self.text_widget.insert(tk.END, f"{status}\nFile: {options_handler.get_variable("current_file_directory")}\nGrid: {options_handler.get_variable("current_grid_directory")}\n")

    def print(self, string):
        self.text_widget.insert(tk.END, string + "\n")   
    
terminal = Terminal()
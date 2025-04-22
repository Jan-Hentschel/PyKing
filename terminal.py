import tkinter as tk
from tkinter import *
from utility import autoHiddenScrollbar

from gui import vertically_pained_window
from options_handler import get_variable


class Terminal:

    def __init__(self):
        self.terminal_frame = Frame(vertically_pained_window, bg="#3F3F3F", bd=0,)
        self.terminal_frame.pack(fill=BOTH, expand=True)

        self.terminal_and_horizontal_scrollbar_frame = Frame(self.terminal_frame, bg="#3F3F3F", bd=0,)
        self.terminal_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Terminal Textfeld erstellen (unten rechts)
        self.terminal_widget = Text(self.terminal_and_horizontal_scrollbar_frame, bg="#3F3F3F", fg="white", bd=0, wrap="none")
        self.terminal_widget.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)
        #scrollbars
        self.vertical_scrollbar = autoHiddenScrollbar(self.terminal_frame, self.terminal_widget, orient=VERTICAL, cursor="arrow")
        self.vertical_scrollbar.pack(side = RIGHT, fill=Y)

        self.horizontal_scrollbar = autoHiddenScrollbar(self.terminal_and_horizontal_scrollbar_frame, self.terminal_widget, orient=HORIZONTAL, cursor="arrow")
        self.horizontal_scrollbar.pack(side = BOTTOM, fill=X)

        self.vertical_scrollbar.config(command = self.terminal_widget.yview)
        self.horizontal_scrollbar.config(command = self.terminal_widget.xview)

        self.terminal_widget["xscrollcommand"] = self.horizontal_scrollbar.set
        self.terminal_widget["yscrollcommand"] = self.vertical_scrollbar.set

    def show_current_directories(self):
        self.terminal_widget.delete('1.0', END)
        self.terminal_widget.insert(tk.END, f"Excecuting\nFile: {get_variable("current_file_directory")}\nGrid: {get_variable("current_grid_directory")}\n")

    def print(self, string):
        self.terminal_widget.insert(tk.END, string + "\n")   
    
terminal = Terminal()
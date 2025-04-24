import tkinter as tk
from tkinter import *
from utility import AutoHiddenScrollbar

from options_handler import options_handler


class Terminal:

    def __init__(self, root):
        self.status_seperator = "_"
        self.frame = Frame(root.vertically_pained_window, bg=root.primary_color, bd=0,)
        self.frame.pack(fill=BOTH, expand=True)

        self.terminal_and_horizontal_scrollbar_frame = Frame(self.frame, bg=root.primary_color, bd=0,)
        self.terminal_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Terminal Textfeld erstellen (unten rechts)
        self.text_widget = Text(self.terminal_and_horizontal_scrollbar_frame, bg=root.primary_color, fg=root.foreground_color, bd=0, wrap="none", insertbackground=root.foreground_color, selectbackground="#6F6F6F", tabs="40")
        self.text_widget.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)
        # scrollbars
        self.vertical_scrollbar = AutoHiddenScrollbar(self.frame, self.text_widget, style="My.Vertical.TScrollbar", orient=VERTICAL, cursor="arrow")
        self.vertical_scrollbar.pack(side = RIGHT, fill=Y)

        self.horizontal_scrollbar = AutoHiddenScrollbar(self.terminal_and_horizontal_scrollbar_frame, self.text_widget, style="My.Horizontal.TScrollbar", orient=HORIZONTAL, cursor="arrow")
        self.horizontal_scrollbar.pack(side = BOTTOM, fill=X)

        self.vertical_scrollbar.config(command = self.text_widget.yview)
        self.horizontal_scrollbar.config(command = self.text_widget.xview)

        self.text_widget["xscrollcommand"] = self.horizontal_scrollbar.set
        self.text_widget["yscrollcommand"] = self.vertical_scrollbar.set

    def calculate_seperator_length(self, status):
        longest_line = len(status)
        if len(status.splitlines()) > 1:
            longest_line = max(len(line) for line in status.splitlines())

        longest_line = max(longest_line, len(f"File: {options_handler.get_variable("current_file_directory")} "), len(f"Grid: {options_handler.get_variable("current_grid_directory")} "))

        return longest_line

    def show_current_directories(self, status ):
        seperator = self.status_seperator * self.calculate_seperator_length(status)
        self.text_widget.delete('1.0', END)
        self.text_widget.insert(tk.END, 
                    f"{status}\n"
                    f"{seperator}\n\n"
                    f"File: {options_handler.get_variable('current_file_directory')}\n"
                    f"Grid: {options_handler.get_variable('current_grid_directory')}\n"
                    f"{seperator}\n\n")

    def print(self, string):
        self.text_widget.insert(tk.END, string + "\n")   

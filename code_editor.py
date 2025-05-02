import tkinter as tk
from tkinter import ttk
from tkinter import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

from utility import *
from settings_handler import *


class CodeEditor:
    def __init__(self, root, master):
        current_file = settings_handler.get_variable("current_file_directory")
        current_file = current_file.split("/")[-1]

        self.first_frame = DefaultFrame(master)
        self.first_frame.pack(side=LEFT, fill=Y)

        self.spacer = Canvas(self.first_frame, height=22, width=60, bg=root.secondary_color, highlightbackground=root.secondary_color)
        self.spacer.pack(anchor=NW)

        self.file_label = DefaultLabel(master, text=current_file, bg=root.primary_color)
        self.file_label.pack(anchor=NW)

        self.line_number_frame = DefaultFrame(self.first_frame, bg=secondary_color, padx=2, highlightbackground=primary_color)
        self.line_number_frame.pack(side=LEFT, fill=Y)

        
        self.frame = DefaultTextFrame(master, bg=root.primary_color, bd=0,)
        self.frame.text_widget.configure(undo=True, maxundo=-1, autoseparators=True)
        self.frame.text_widget.bind("<Control-Shift-Z>", lambda event: self.frame.text_widget.edit_redo())




        #help from ChatGPT
        


        self.line_number_text_widget = Text(
            self.line_number_frame,
            state="disabled",
            padx=10,
            width=4,
            bg=primary_color,
            fg=foreground_color,
            bd=0,
            wrap="none",
            insertbackground=foreground_color,
            selectbackground="#6F6F6F",
            tabs="40"
        )
        self.line_number_text_widget.tag_configure("right", justify='right')
        self.line_number_text_widget.pack(fill=Y, side=LEFT)

        # Prevent interaction with line number widget
        self.line_number_text_widget.bind("<MouseWheel>", lambda e: "break")
        self.line_number_text_widget.bind("<Key>", lambda e: "break")
        self.line_number_text_widget.bind("<Button-1>", lambda e: "break")
        self.line_number_text_widget.configure(takefocus=0)



        self.frame.pack(fill=BOTH, side=RIGHT, expand=True)

        self.frame.text_widget.bind("<Configure>", self.update_line_numbers)
        self.frame.text_widget.configure(yscrollcommand=self.on_textscroll)
        # Sync scrolling from all input methods
        self.frame.text_widget.bind("<Button-4>", self.on_mousewheel)  # For Linux
        self.frame.text_widget.bind("<Button-5>", self.on_mousewheel)
        self.frame.text_widget.bind("<KeyRelease-Up>", self.update_line_numbers)
        self.frame.text_widget.bind("<KeyRelease-Down>", self.update_line_numbers)
        self.frame.text_widget.bind("<Return>", self.update_line_numbers)
        self.frame.text_widget.bind("<BackSpace>", self.update_line_numbers)
        self.frame.text_widget.bind("<KeyRelease>", self.update_line_numbers)
        self.frame.text_widget.bind("<MouseWheel>", self.handle_mousewheel_and_update)
        self.frame.text_widget.bind("<ButtonRelease>", self.update_line_numbers)
        self.frame.text_widget.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)
        
        self.percolator = Percolator(self.frame.text_widget)
        self.percolator.insertfilter(root.color_delegator)

    def load_into_editor(self, content):
        self.frame.text_widget.configure(undo=False) #clears the undo stack
        self.frame.text_widget.delete(1.0,END)
        self.frame.text_widget.insert(tk.END, content)
        self.update_line_numbers()
        self.frame.text_widget.configure(undo=True)

    def get_text_widget_content(self):
        return self.frame.text_widget.get("1.0",END)
    
    def update_line_numbers(self, event=None):
        self.frame.after_idle(self._sync_line_numbers)

    def on_textscroll(self, *args):
        try:
            first = float(args[0])
            if 0.0 <= first <= 1.0:
                self.line_number_text_widget.yview_moveto(args[0])
        except (ValueError, IndexError):
            pass
        self.frame.vertical_scrollbar.set(*args)


    def on_mousewheel(self, event):
        # This scrolls the main text
        self.frame.text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Manually sync the line number widget
        self.line_number_text_widget.yview_moveto(self.frame.text_widget.yview()[0])
        
        return "break"  # Prevent default scrolling from duplicating
    
    def on_shift_mousewheel(self, event):
        self.frame.text_widget.xview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
            
    def handle_mousewheel_and_update(self, event):
        self.on_mousewheel(event)
        self.update_line_numbers()
        return "break"

        
    def _sync_line_numbers(self):
        self.line_number_text_widget.configure(state="normal")
        self.line_number_text_widget.delete("1.0", "end")

        num_lines = int(self.frame.text_widget.index("end-1c").split(".")[0])
        for i in range(1, num_lines + 1):
            self.line_number_text_widget.insert("end", f"{i}\n", "right")

        self.line_number_text_widget.yview_moveto(self.frame.text_widget.yview()[0])
        self.line_number_text_widget.configure(state="disabled")

    def update_file_label(self):
        current_file = settings_handler.get_variable("current_file_directory")
        current_file = current_file.split("/")[-1]
        self.file_label.configure(text=current_file)
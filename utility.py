import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.font import Font
import os
import sys

button_list = []

#https://www.geeksforgeeks.org/autohiding-scrollbars-using-python-tkinter/
#https://stackoverflow.com/questions/41095385/autohide-tkinter-canvas-scrollbar-with-pack-geometry 


class AutoHiddenScrollbar(ttk.Scrollbar):
    def __init__(self, master, target_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.target_widget = target_widget
        self.grid_info_cache = None  # Store grid options for reuse

    def set(self, low, high):
        is_horizontal = self.cget("orient") == "horizontal"

        if is_horizontal:
            if self.has_horizontal_overflow():
                self.restore_grid()
            else:
                self.grid_remove()
        else:
            if float(low) <= 0.0 and float(high) >= 1.0:
                self.grid_remove()
            else:
                self.restore_grid()

        Scrollbar.set(self, low, high)

    def has_horizontal_overflow(self):
        widget_width = self.target_widget.winfo_width()
        font = Font(font=self.target_widget["font"])

        num_lines = int(self.target_widget.index("end-1c").split(".")[0])
        for i in range(1, num_lines + 1):
            line_text = self.target_widget.get(f"{i}.0", f"{i}.end")
            if font.measure(line_text) > widget_width:
                return True
        return False

    def grid(self, **kwargs):
        # Store the grid info once for reuse in restore_grid
        self.grid_info_cache = kwargs
        super().grid(**kwargs)

    def restore_grid(self):
        if self.grid_info_cache:
            super().grid(**self.grid_info_cache)
    
class DefaultButton(Button):
    def __init__(self, master, bd=2, bg="#3F3F3F", activebackground="#333333", fg="#FFFFFF", activeforeground="#FFFFFF", height=2, **kwargs):
        super().__init__(master, bd=bd, bg=bg, activebackground=activebackground, fg=fg, activeforeground=activeforeground, **kwargs)
        if not self.cget("image"):
            self.configure(height=height)

    def pack(self, side="left", **kwargs):
        super().pack(side=side, **kwargs)
        global button_list
        button_list.append(self)

class DefaultLabel(Label):
    def __init__(self, master, bg="#333333", fg="#FFFFFF", activeforeground="#FFFFFF", **kwargs):
        super().__init__(master, bg=bg, fg=fg, activeforeground=activeforeground, **kwargs)

class DefaultEntry(Entry):
    def __init__(self, master, bg="#3F3F3F", fg="#FFFFFF", **kwargs):
        super().__init__(master, bg=bg, fg=fg, **kwargs)

class DefaultToplevel(Toplevel):
    def __init__(self, master, bg="#333333", **kwargs):
        super().__init__(master, bg=bg, **kwargs)

class DefaultFrame(Frame):
    def __init__(self, master, bg="#3F3F3F", **kwargs):
        super().__init__(master, bg=bg, **kwargs)

class DefaultTextFrame(Frame):
    def __init__(self, master, line_numbers=FALSE, bg="#3F3F3F", **kwargs):
        super().__init__(master, bg=bg, **kwargs)
        if line_numbers:
            self.line_number_frame = DefaultFrame(self, bg="#333333", padx=2, highlightbackground = "#3F3F3F")
            self.line_number_frame.pack(side=LEFT, fill=Y)

            self.line_number_text_widget = Text(self.line_number_frame, state="disabled", padx=10, width=4, bg="#3F3F3F", fg="#FFFFFF", bd=0, wrap="none", insertbackground="#FFFFFF", selectbackground="#6F6F6F", tabs="40")
            self.line_number_text_widget.tag_configure("right", justify='right')
            self.line_number_text_widget.pack(fill=Y, side=LEFT)



        # Text + Scrollbars Frame
        self.plus_scrollbar_frame = DefaultFrame(self, bg="#3F3F3F")
        self.plus_scrollbar_frame.pack(side=TOP, fill=BOTH, expand=True)

        # Text widget
        self.text_widget = Text(self.plus_scrollbar_frame, padx=10, bg="#3F3F3F", fg="#FFFFFF", bd=0,
                                wrap="none", insertbackground="#FFFFFF", selectbackground="#6F6F6F", tabs="40")
        self.text_widget.grid(row=0, column=0, sticky="nsew")

        if line_numbers:
            self.text_widget.bind("<KeyRelease>", self.update_line_numbers)
            self.text_widget.bind("<MouseWheel>", self.update_line_numbers)
            self.text_widget.bind("<ButtonRelease>", self.update_line_numbers)


        # Vertical scrollbar
        self.vertical_scrollbar = AutoHiddenScrollbar(self.plus_scrollbar_frame, self.text_widget,
                                                    style="My.Vertical.TScrollbar", orient=VERTICAL, cursor="arrow")
        self.vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar
        self.horizontal_scrollbar = AutoHiddenScrollbar(self.plus_scrollbar_frame, self.text_widget,
                                                        style="My.Horizontal.TScrollbar", orient=HORIZONTAL, cursor="arrow")
        self.horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        # Grid weight for resizing
        self.plus_scrollbar_frame.grid_rowconfigure(0, weight=1)
        self.plus_scrollbar_frame.grid_columnconfigure(0, weight=1)


        self.vertical_scrollbar.config(command = self.text_widget.yview)
        self.horizontal_scrollbar.config(command = self.text_widget.xview)

        self.text_widget["xscrollcommand"] = self.horizontal_scrollbar.set
        self.text_widget["yscrollcommand"] = self.vertical_scrollbar.set

    def update_line_numbers(self, event=None):
        self.line_number_text_widget.configure(state="normal")
        self.line_number_text_widget.delete("1.0", "end")
        num_lines = int(self.text_widget.index("end-1c").split(".")[0])
        for i in range(1, num_lines + 1):
            self.line_number_text_widget.insert("end", f"{i}\n", "right")
        self.line_number_text_widget.configure(state="disabled")



        

        


        
        






#https://www.youtube.com/watch?v=p3tSLatmGvU
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
#vor jeden relative path diese funktion setzen um pyinstaller zu helfen alle dateien zu finden


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def path_from_relative_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
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


        
    def set(self, low, high):
        if self.cget("style") == "My.Horizontal.TScrollbar":
            if self.has_horizontal_overflow():
                self.pack(side=BOTTOM, fill=X)
            else:
                self.pack_forget()
        elif self.cget("style") == "My.Vertical.TScrollbar":
            if float(low) <= 0.0 and float(high) >= 1.0:
                self.pack_forget()
            else:
                self.pack(side=RIGHT, fill=Y)
        Scrollbar.set(self, low, high)

    #hilfe von Chatgpt klappt aber immernoch nicht so wie gewollt
    def has_horizontal_overflow(self):
        
        widget_width = self.target_widget.winfo_width()
        font = Font(font=self.target_widget["font"])
        
        num_lines = int(self.target_widget.index("end-1c").split(".")[0])
        for i in range(1, num_lines + 1):
            line_text = self.target_widget.get(f"{i}.0", f"{i}.end")
            line_width = font.measure(line_text)
            if line_width > widget_width:
                return True
        return False
    
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
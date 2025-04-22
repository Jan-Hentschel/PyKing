import tkinter as tk
from tkinter import *
from tkinter.font import Font
import os
import sys


#https://www.geeksforgeeks.org/autohiding-scrollbars-using-python-tkinter/
#https://stackoverflow.com/questions/41095385/autohide-tkinter-canvas-scrollbar-with-pack-geometry 


class AutoHiddenScrollbar(Scrollbar):
    def __init__(self, master, target_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.target_widget = target_widget  

        
    def set(self, low, high):
        if self.cget("orient") == HORIZONTAL:
            if self.has_horizontal_overflow():
                self.pack(side = BOTTOM, fill=X)
            else:
                self.pack_forget()   
        else:
            if float(low) <= 0.0 and float(high) >= 1.0:
                self.pack_forget()
            else:
                self.pack(side = RIGHT, fill=Y)
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
    
class ToolbarButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, bd=2, bg="#3F3F3F", activebackground="#333333", fg="#FFFFFF", activeforeground="#FFFFFF", height=2, **kwargs)

    def pack(self, side="left", **kwargs):
        super().pack(side=side, **kwargs)

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
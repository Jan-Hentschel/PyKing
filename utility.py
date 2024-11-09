import tkinter as tk
from gui import root
from tkinter import *
from tkinter.font import Font

#https://www.geeksforgeeks.org/autohiding-scrollbars-using-python-tkinter/
#https://stackoverflow.com/questions/41095385/autohide-tkinter-canvas-scrollbar-with-pack-geometry 

# class autoHiddenScrollbar(Scrollbar):
#     def set(self, low, high):
#         if self.cget("orient") == HORIZONTAL:
#             print(self.has_horizontal_overflow())
#             if self.has_horizontal_overflow():
#                 self.pack(side = BOTTOM, fill=X)
                
#             else:
#                 self.pack_forget()
                
#         else:
#             if float(low) <= 0.0 and float(high) >= 1.0:
#                 self.pack_forget()
#             else:
#                 self.pack(side = RIGHT, fill=Y)
#         Scrollbar.set(self, low, high)


#     #chatgpt
#     def has_horizontal_overflow(self):
#         widget_width = code_editor_widget.winfo_width()
#         font = Font(font=code_editor_widget["font"])
        
#         num_lines = int(code_editor_widget.index("end-1c").split(".")[0])
#         for i in range(1, num_lines + 1):
#             line_text = code_editor_widget.get(f"{i}.0", f"{i}.end")
#             line_width = font.measure(line_text)
#             print(line_width)
#             if line_width > widget_width:
#                 return True
#         return False

class autoHiddenScrollbar(Scrollbar):
    def __init__(self, master, target_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.target_widget = target_widget  # Target widget for overflow checking

        
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
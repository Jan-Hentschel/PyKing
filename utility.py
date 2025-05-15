import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.font import Font
import os
import sys

from settings_handler import settings_handler


button_list = []

foreground_color = settings_handler.get_variable("foreground_color")
primary_color = settings_handler.get_variable("primary_color")
secondary_color = settings_handler.get_variable("secondary_color")

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
    def __init__(self, master, bd=2, bg=primary_color, activebackground=secondary_color, fg=foreground_color, activeforeground=foreground_color, height=2, **kwargs):
        super().__init__(master, bd=bd, bg=bg, activebackground=activebackground, fg=fg, activeforeground=activeforeground, **kwargs)
        if not self.cget("image"):
            self.configure(height=height)
        self.pack()

    def pack(self, side="left", **kwargs):
        super().pack(side=side, **kwargs)
        global button_list
        button_list.append(self)

class DefaultMenuButton(Button):
    def __init__(self, master, bd=0, bg=secondary_color, activebackground=primary_color, fg=foreground_color, activeforeground=foreground_color, height=2, **kwargs):
        super().__init__(master, bd=bd, bg=bg, activebackground=activebackground, fg=fg, activeforeground=activeforeground, **kwargs)
        if not self.cget("image"):
            self.configure(height=height)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.pack()

    def pack(self, side="left", **kwargs):
        super().pack(side=side, **kwargs)
        global button_list
        button_list.append(self)

    def on_enter(self, e):
        self['background'] = primary_color

    def on_leave(self, e):
        self['background'] = secondary_color

class DefaultLabel(Label):
    def __init__(self, master, bg=secondary_color, fg=foreground_color, activeforeground=foreground_color, **kwargs):
        super().__init__(master, bg=bg, fg=fg, activeforeground=activeforeground, **kwargs)
        self.pack()

class DefaultEntry(Entry):
    def __init__(self, master, bg=primary_color, fg=foreground_color, **kwargs):
        super().__init__(master, bg=bg, fg=fg, **kwargs)
        self.pack()

class DefaultToplevel(Toplevel):
    def __init__(self, master, bg=secondary_color, **kwargs):
        super().__init__(master, bg=bg, **kwargs)

class DefaultFrame(Frame):
    def __init__(self, master, bg=primary_color, **kwargs):
        super().__init__(master, bg=bg, **kwargs)

class DefaultTextFrame(Frame):
    def __init__(self, master, bg=primary_color, **kwargs):
        super().__init__(master, bg=bg, **kwargs)


        # Frame containing Text + Scrollbars
        self.plus_scrollbar_frame = DefaultFrame(self, bg=primary_color)
        self.plus_scrollbar_frame.pack(side=TOP, fill=BOTH, expand=True)

        # Text widget
        self.text_widget = Text(
            self.plus_scrollbar_frame,
            padx=10,
            bg=primary_color,
            fg=foreground_color,
            bd=0,
            wrap="none",
            insertbackground=foreground_color,
            selectbackground="#6F6F6F",
            tabs="40",


        )
        
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.text_widget.bind("<Control-BackSpace>", lambda event: self.on_control_backspace())
        self.text_widget.bind("<Control-Delete>", lambda event: self.on_control_delete())


        # Grid weight for resizing
        self.plus_scrollbar_frame.grid_rowconfigure(0, weight=1)
        self.plus_scrollbar_frame.grid_columnconfigure(0, weight=1)

        # Vertical scrollbar
        self.vertical_scrollbar = AutoHiddenScrollbar(
            self.plus_scrollbar_frame,
            self.text_widget,
            style="My.Vertical.TScrollbar",
            orient=VERTICAL,
            cursor="arrow",
            command=self.on_scrollbar_scroll
        )
        self.vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar
        self.horizontal_scrollbar = AutoHiddenScrollbar(
            self.plus_scrollbar_frame,
            self.text_widget,
            style="My.Horizontal.TScrollbar",
            orient=HORIZONTAL,
            cursor="arrow",
            command=self.text_widget.xview
        )
        self.horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        # Scrollbar <-> text widget communication
        self.text_widget.configure(xscrollcommand=self.horizontal_scrollbar.set)
        self.text_widget.configure(yscrollcommand=self.vertical_scrollbar.set)

    def on_control_backspace(self):
        #CHATGPT HELP (VIBE CODED)
        cursor_index = self.text_widget.index(tk.INSERT)
        prev_index = self.text_widget.index(f"{cursor_index} -1c")

        if self.text_widget.compare(prev_index, "<", "1.0"):
            return "break"  # Already at start of text

        char = self.text_widget.get(prev_index)

        break_chars = set(" \n\t()[]{}:;.,'\"#=+-*/%<>!&|^~\\")

        # If previous character is a break character, delete just one
        if char in break_chars:
            self.text_widget.delete(prev_index, cursor_index)
            return "break"

        # Otherwise, delete until a break character is found
        index = cursor_index
        while True:
            prev_index = self.text_widget.index(f"{index} -1c")
            if self.text_widget.compare(prev_index, "<", "1.0"):
                break
            char = self.text_widget.get(prev_index)
            if char in break_chars:
                break
            index = prev_index

        self.text_widget.delete(index, cursor_index)
        return "break"

    def on_control_delete(self):
        cursor_index = self.text_widget.index(tk.INSERT)
        next_index = self.text_widget.index(f"{cursor_index} +1c")

        if self.text_widget.compare(next_index, ">", tk.END):
            return "break"  # Already at end of text

        char = self.text_widget.get(cursor_index)

        break_chars = set(" \n\t()[]{}:;.,'\"#=+-*/%<>!&|^~\\")

        # If next character is a break character, delete just one
        if char in break_chars:
            self.text_widget.delete(cursor_index, next_index)
            return "break"

        # Otherwise, delete until a break character is found
        index = cursor_index
        while True:
            char = self.text_widget.get(index)
            if char in break_chars or self.text_widget.compare(index, ">=", tk.END):
                break
            index = self.text_widget.index(f"{index} +1c")

        self.text_widget.delete(cursor_index, index)
        return "break"

    def on_scrollbar_scroll(self, *args):
        self.text_widget.yview(*args)
        try: 
            if self.line_numbers:
                self.line_number_text_widget.yview(*args)
        except AttributeError:
            pass

            
class DefaultCheckbutton(Checkbutton):
    def __init__(self, master, bg=secondary_color, selectcolor=primary_color, fg=foreground_color, activebackground=secondary_color, activeforeground=foreground_color, onvalue = 1, offvalue = 0,  **kwargs):
        super().__init__(master, bg=bg, selectcolor=selectcolor,fg=fg, activebackground=activebackground, activeforeground=activeforeground, onvalue = onvalue, offvalue = offvalue, **kwargs)
        
class SettingsCheckbutton(Checkbutton):
    def __init__(self, master, root_var_name, bg=secondary_color, selectcolor=primary_color, fg=foreground_color, activebackground=secondary_color, activeforeground=foreground_color, onvalue = 1, offvalue = 0,  **kwargs):
        self.root_var_name = root_var_name
        from gui import root
        self.root = root

        self.var= IntVar()

        self.root_var = self.root.settings_variables[self.root_var_name]
        if self.root_var == "True":
            self.var.set(1)
        else:
            self.var.set(0)
        super().__init__(master, bg=bg, variable=self.var, selectcolor=selectcolor,fg=fg, activebackground=activebackground, activeforeground=activeforeground, onvalue = onvalue, offvalue = offvalue, **kwargs)
        self.pack()

    def apply(self):
        if self.var.get() == 1:
            settings_handler.set_variable(self.root_var_name, True)
            self.root.settings_variables[self.root_var_name] = "True"
        else:
            settings_handler.set_variable(self.root_var_name, False)
            self.root.settings_variables[self.root_var_name] = "False"        

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


class FileLabel(DefaultLabel):
    def __init__(self, master, directory, padx=10, pady=5, bg=secondary_color, fg=foreground_color, activeforeground=foreground_color, **kwargs):
        super().__init__(master, bg=bg, fg=fg, padx=padx, pady=pady,activeforeground=activeforeground, **kwargs)
        self.directory = directory
        self.pack()

    def pack(self, side="left", **kwargs):
        super().pack(side=side, **kwargs)

class DefaultMenu(Menu):
    def __init__(self, master, bd=0, activebackground=primary_color, activeborderwidth=0, bg=secondary_color, fg=foreground_color, activeforeground=foreground_color, **kwargs):
        super().__init__(master, bd=bd, activebackground=activebackground, activeborderwidth=activeborderwidth, bg=bg, fg=fg, activeforeground=activeforeground, **kwargs)
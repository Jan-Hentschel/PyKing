import tkinter as tk
from tkinter import ttk
from tkinter import Widget, Button, Label, Entry, Toplevel, Frame, Text, Checkbutton, IntVar, HORIZONTAL, VERTICAL, N, E, S, W, END, BOTH, RIGHT, LEFT, Y, X, TOP, Canvas, NW, Menu, Scale, Scrollbar, PhotoImage, PanedWindow #type: ignore
from tkinter.font import Font
import os
import sys
from typing import Any, ClassVar, Literal, cast

from settings_handler import settings_handler

#https://www.youtube.com/watch?v=p3tSLatmGvU
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
#vor jeden relative path diese funktion setzen um pyinstaller zu helfen alle dateien zu finden

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def path_from_relative_path(relative_path: str) -> str:
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



#https://www.geeksforgeeks.org/autohiding-scrollbars-using-python-tkinter/
#https://stackoverflow.com/questions/41095385/autohide-tkinter-canvas-scrollbar-with-pack-geometry 

class CustomWidgetMixin:
    widget_list: ClassVar[list['CustomWidgetMixin']] = []

    def build_style(self) -> dict[str, Any]:
        return {}

    @staticmethod
    def print_widgets():
        for widget in CustomWidgetMixin.widget_list:
            print(widget.__class__.__name__)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)  
        CustomWidgetMixin.widget_list.append(self)
        widget = cast(Widget, self)
        try:
            widget.pack()
        except Exception:
            pass

    @property
    def foreground_color(self):
        return settings_handler.get_variable("foreground_color")

    @property
    def primary_color(self):
        return settings_handler.get_variable("primary_color")

    @property
    def secondary_color(self):
        return settings_handler.get_variable("secondary_color")

    def update_color(self):
        widget = cast(Widget, self)
        style = self.build_style()
        if widget.winfo_exists():
            widget.configure(**style) 
    
            

class AutoHiddenScrollbar(CustomWidgetMixin, ttk.Scrollbar):
    def __init__(self, master: Widget, target_widget: Text, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)
        self.target_widget = target_widget
        self.grid_info_cache = None  # Store grid options for reuse
        

    def set(self, first: float | str, last: float | str):
        is_horizontal = self.cget("orient") == "horizontal"

        if is_horizontal:
            if self.has_horizontal_overflow():
                self.restore_grid()
            else:
                self.grid_remove()
        else:
            if float(first) <= 0.0 and float(last) >= 1.0:
                self.grid_remove()
            else:
                self.restore_grid()

        Scrollbar.set(self, first, last)

    def has_horizontal_overflow(self):
        widget_width = self.target_widget.winfo_width()
        font = Font(font=self.target_widget["font"])

        num_lines = int(self.target_widget.index("end-1c").split(".")[0])
        for i in range(1, num_lines + 1):
            line_text = self.target_widget.get(f"{i}.0", f"{i}.end")
            if font.measure(line_text) > widget_width:
                return True
        return False

    def grid(self, **kwargs: Any):
        # Store the grid info once for reuse in restore_grid
        self.grid_info_cache = kwargs
        super().grid(**kwargs)

    def restore_grid(self):
        if self.grid_info_cache:
            super().grid(**self.grid_info_cache)

    def build_style(self) -> dict[str, Any]:
        return {}


class DefaultButton(CustomWidgetMixin, Button):
    def __init__(self, master: Any,**kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)
        if not self.cget("image"):
            self.configure(height=2)

    def build_style(self) -> dict[str, Any]:
        return {
            'bd': 2,
            'bg': self.primary_color,
            'activebackground': self.secondary_color,
            'fg': self.foreground_color,
            'activeforeground': self.foreground_color,
        }
    
    def pack(self, side: Literal["left", "right", "top", "bottom"]="left", **kwargs: Any) -> None:
        super().pack(side=side, **kwargs)


class DefaultMenuButton(CustomWidgetMixin, Button):
    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)
        if not self.cget("image"):
            self.configure(height=2)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def build_style(self) -> dict[str, Any]:
        return {
            'bd':               0,
            'bg':               self.secondary_color,
            'activebackground': self.primary_color,
            'fg':               self.foreground_color,
            'activeforeground': self.foreground_color,
        }
    


    def pack(self, side: Literal["left", "right", "top", "bottom"]="left", **kwargs: Any):
        super().pack(side=side, **kwargs)

    def on_enter(self, e: Any):
        self['background'] = self.primary_color

    def on_leave(self, e: Any):
        self['background'] = self.secondary_color


class DefaultLabel(CustomWidgetMixin, Label):
    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.secondary_color,
            'fg': self.foreground_color,
            'activeforeground': self.foreground_color
        }

    def __init__(self, master: Any, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)


class DefaultEntry(CustomWidgetMixin, Entry):
    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.primary_color,
            'fg': self.foreground_color
        }

    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)


class DefaultToplevel(CustomWidgetMixin, Toplevel):
    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.secondary_color
        }

    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)


class DefaultPrimaryFrame(CustomWidgetMixin, Frame):
    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.primary_color
        }

    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)


class DefaultSecondaryFrame(CustomWidgetMixin, Frame):
    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.secondary_color
        }

    def __init__(self, master: Any, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)


class DefaultTextFrame(CustomWidgetMixin, Frame):
    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)


        # Frame containing Text + Scrollbars
        self.plus_scrollbar_frame = DefaultPrimaryFrame(self, bg=self.primary_color)
        self.plus_scrollbar_frame.pack(side="top", fill="both", expand=True)

        # Text widget
        self.text_widget = Text(
            self.plus_scrollbar_frame,
            padx=10,
            bg=self.primary_color,
            fg=self.foreground_color,
            bd=0,
            wrap="none",
            insertbackground=self.foreground_color,
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
            command=self.text_widget.xview # type: ignore
        )
        self.horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        # Scrollbar <-> text widget communication
        self.text_widget.configure(xscrollcommand=self.horizontal_scrollbar.set)
        self.text_widget.configure(yscrollcommand=self.vertical_scrollbar.set)

    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.primary_color
        }

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

    def on_scrollbar_scroll(self, *args: Any) -> None:
        self.text_widget.yview(*args) # type: ignore

            
class DefaultCheckbutton(CustomWidgetMixin, Checkbutton):
    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)

    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.secondary_color,
            'selectcolor': self.primary_color,
            'fg': self.foreground_color,
            'activebackground': self.secondary_color,
            'activeforeground': self.foreground_color,
            'onvalue': 1,
            'offvalue': 0
        }


class SettingsCheckbutton(CustomWidgetMixin, Checkbutton):
    def __init__(self, master: Widget, root_var_name: str, **kwargs: Any):
        self.root_var_name: str = root_var_name

        from gui import root, Root
        self.root: Root = root

        self.var = IntVar()

        self.root_var = self.root.settings_variables[self.root_var_name]

        if self.root_var == "True":
            self.var.set(1)
        else:
            self.var.set(0)
        style = self.build_style()
        for k, v in style.items():
            kwargs.setdefault(k, v)
        kwargs["variable"] = self.var
        super().__init__(master, **kwargs)


    def apply(self):
        if self.var.get() == 1:
            settings_handler.set_variable(self.root_var_name, "True")
            self.root.settings_variables[self.root_var_name] = "True"
        else:
            settings_handler.set_variable(self.root_var_name, "False")
            self.root.settings_variables[self.root_var_name] = "False"        

    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.secondary_color,
            'selectcolor': self.primary_color,
            'fg': self.foreground_color,
            'activebackground': self.secondary_color,
            'activeforeground': self.foreground_color,
            'onvalue': 1,
            'offvalue': 0
        }


class FileLabel(DefaultLabel):
    def __init__(self, master: Widget, directory: str, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)
        self.directory: str = directory

    def build_style(self) -> dict[str, Any]:
        return {
            'padx': 10,
            'pady': 5,
            'bg': self.secondary_color,
            'fg': self.foreground_color,
            'activeforeground': self.foreground_color
        }

    def pack(self, side: Literal["left", "right", "top", "bottom"]="left", **kwargs: Any):
        DefaultLabel.pack(self, side=side, **kwargs)


class DefaultMenu(CustomWidgetMixin, Menu):
    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)

    def build_style(self) -> dict[str, Any]:
        return {
            'bd': 0,
            'activebackground': self.primary_color,
            'activeborderwidth': 0,
            'bg': self.secondary_color,
            'fg': self.foreground_color,
            'activeforeground': self.foreground_color
        }


class DefaultScale(CustomWidgetMixin, Scale):
    def __init__(self, master: Widget, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)

    def build_style(self) -> dict[str, Any]:
        return {
            'from_': 1,
            'to': 100,
            'orient': HORIZONTAL,
            'length': 200,
            'bg': self.secondary_color,
            'activebackground': self.secondary_color,
            'highlightbackground': self.secondary_color,
            'fg': self.foreground_color,
            'troughcolor': self.primary_color
        }
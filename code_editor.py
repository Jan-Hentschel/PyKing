import tkinter as tk
from tkinter import ttk
from tkinter import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

from utility import AutoHiddenScrollbar



class CodeEditor:
    def __init__(self, root):
        self.frame = Frame(root.horizontally_paned_window, bg=root.primary_color, bd=0,)
        self.frame.pack(fill=BOTH, expand=True)

        self.code_editor_and_horizontal_scrollbar_frame = Frame(self.frame, bg=root.primary_color, bd=0,)
        self.code_editor_and_horizontal_scrollbar_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Text-Feld für den Code Editor erstellen (mitte)
        self.text_widget = Text(self.code_editor_and_horizontal_scrollbar_frame, bg=root.primary_color, fg="white", bd=0, wrap="none", insertbackground="#FFFFFF", selectbackground="#6F6F6F", tabs="40")
        self.text_widget.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)


        #scrollbars
        self.style = ttk.Style()
        self.style.theme_use("default")# Define a vertical scrollbar style

        self.style.element_create("My.Vertical.Scrollbar.trough", "from", "default")
        self.style.layout("My.Vertical.TScrollbar",
            [('My.Vertical.Scrollbar.trough', {'children':
                [('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}),
                ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}),
                ('Vertical.Scrollbar.thumb', {'unit': '1', 'children':
                    [('Vertical.Scrollbar.grip', {'sticky': ''})],
                'sticky': 'nswe'})],
            'sticky': 'ns'})])
        self.style.configure("My.Vertical.TScrollbar", troughcolor="#333333")

        self.style.element_create("My.Horizontal.Scrollbar.trough", "from", "default")
        self.style.layout("My.Horizontal.TScrollbar",
            [('My.Horizontal.Scrollbar.trough', {'children':
                [('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}),
                ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}),
                ('Horizontal.Scrollbar.thumb', {'unit': '1', 'children':
                    [('Horizontal.Scrollbar.grip', {'sticky': ''})],
                'sticky': 'nswe'})],
            'sticky': 'we'})])
        
        self.style.configure("My.Horizontal.TScrollbar", troughcolor="#333333")
        self.style.configure("My.Vertical.TScrollbar", troughcolor="#333333")
 
        
        #self.style.map("Scrollbar", background=[("selected", "#3F3F3F")])

        self.vertical_scrollbar = AutoHiddenScrollbar(self.frame, self.text_widget, style="My.Vertical.TScrollbar", orient=VERTICAL, cursor="arrow")
        self.vertical_scrollbar.pack(side = RIGHT, fill=Y)

        self.horizontal_scrollbar = AutoHiddenScrollbar(self.code_editor_and_horizontal_scrollbar_frame, self.text_widget, style="My.Horizontal.TScrollbar", orient=HORIZONTAL, cursor="arrow")
        self.horizontal_scrollbar.pack(side = BOTTOM, fill=X)

        self.horizontal_scrollbar.config(command = self.text_widget.xview)
        self.vertical_scrollbar.config(command = self.text_widget.yview)

        self.text_widget["xscrollcommand"] = self.horizontal_scrollbar.set
        self.text_widget["yscrollcommand"] = self.vertical_scrollbar.set

        color_delegator = ColorDelegator()
        color_delegator.tagdefs['COMMENT'] = {'foreground': '#AAAAAA', 'background': root.primary_color} #example: #, """, '''
        color_delegator.tagdefs['KEYWORD'] = {'foreground': '#D67CBC', 'background': root.primary_color} #example: def, class, if, else, etc.
        color_delegator.tagdefs['BUILTIN'] = {'foreground': '#71BFFF', 'background': root.primary_color} #example: print, len, etc.
        color_delegator.tagdefs['STRING'] = {'foreground': '#A8D37E', 'background': root.primary_color} #example: "string", 'string', """string""", '''string'''
        color_delegator.tagdefs['DEFINITION'] = {'foreground': '#71BFFF', 'background': root.primary_color} #example: def function_name, class ClassName, etc.
        
        Percolator(self.text_widget).insertfilter(color_delegator)

    def load_into_editor(self, content):
        self.text_widget.delete(1.0,END)
        self.text_widget.insert(tk.END, content)

    def get_text_widget_content(self):
        return self.text_widget.get("1.0",END)
    

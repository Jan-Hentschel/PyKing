import tkinter as tk
from tkinter import *
from ctypes import windll
from tkinter import ttk
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

from utility import *
from settings_handler import settings_handler



class Root(tk.Tk):
    def __init__(self, *args, **kwargs):

        windll.shcore.SetProcessDpiAwareness(2) #damit text nicht blurry ist

        super().__init__(*args, **kwargs)

        self.title("PyKing")
        self.iconbitmap(resource_path("Assets\\Icon.ico"))

        self.screen_height = self.winfo_screenheight()
        self.screen_width = self.winfo_screenwidth()
        self.geometry(f"{self.screen_width}x{self.screen_height}")

        self.state('zoomed')


        #settings variables
        self.remember_last_file = settings_handler.get_variable("remember_last_file")
        self.remember_last_grid = settings_handler.get_variable("remember_last_grid")
        self.remember_last_directory = settings_handler.get_variable("remember_last_directory")
        
        self.show_snake_actions_in_terminal = settings_handler.get_variable("show_snake_actions_in_terminal")

        self.foreground_color = settings_handler.get_variable("foreground_color")
        self.primary_color = settings_handler.get_variable("primary_color")
        self.secondary_color = settings_handler.get_variable("secondary_color")




        #scrollbars
        self.style = ttk.Style()
        self.style.theme_use("default")# Define a vertical scrollbar style

        self.style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})  # removes borders
        ])

        self.style.configure("Treeview", background=self.secondary_color, foreground=self.foreground_color, fieldbackground=self.secondary_color, )
        self.style.map("Treeview", background=[("selected", self.primary_color)])

        self.style.element_create("My.Vertical.Scrollbar.trough", "from", "default")
        self.style.layout("My.Vertical.TScrollbar",
            [('My.Vertical.Scrollbar.trough', {'children':
                [('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}),
                ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}),
                ('Vertical.Scrollbar.thumb', {'unit': '1', 'children':
                    [('Vertical.Scrollbar.grip', {'sticky': ''})],
                'sticky': 'nswe'})],
            'sticky': 'ns'})])


        self.style.element_create("My.Horizontal.Scrollbar.trough", "from", "default")
        self.style.layout("My.Horizontal.TScrollbar",
            [('My.Horizontal.Scrollbar.trough', {'children':
                [('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}),
                ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}),
                ('Horizontal.Scrollbar.thumb', {'unit': '1', 'children':
                    [('Horizontal.Scrollbar.grip', {'sticky': ''})],
                'sticky': 'nswe'})],
            'sticky': 'we'})])
        
        self.style.configure("My.Horizontal.TScrollbar", troughcolor=self.secondary_color, background=self.primary_color, width=20, bordercolor =self.secondary_color, arrowsize="20")#, arrowcolor="FFFFFF") 
        self.style.configure("My.Vertical.TScrollbar", troughcolor=self.secondary_color, background=self.primary_color, width=20, bordercolor=self.secondary_color, arrowsize="20")#, arrowcolor="FFFFFF")
 
        self.color_delegator = ColorDelegator()
        self.color_delegator.tagdefs['COMMENT'] = {'foreground': '#AAAAAA', 'background': self.primary_color} #example: #, """, '''
        self.color_delegator.tagdefs['KEYWORD'] = {'foreground': '#D67CBC', 'background': self.primary_color} #example: def, class, if, else, etc.
        self.color_delegator.tagdefs['BUILTIN'] = {'foreground': '#71BFFF', 'background': self.primary_color} #example: print, len, etc.
        self.color_delegator.tagdefs['STRING'] = {'foreground': '#A8D37E', 'background': self.primary_color} #example: "string", 'string', """string""", '''string'''
        self.color_delegator.tagdefs['DEFINITION'] = {'foreground': '#71BFFF', 'background': self.primary_color} #example: def function_name, class ClassName, etc.

        self.configure(bg=self.secondary_color)
        self.horizontally_paned_window = PanedWindow(self, orient=tk.HORIZONTAL, bg=self.secondary_color, sashwidth = 10)
        


        self.vertically_pained_window = PanedWindow(self.horizontally_paned_window, orient=tk.VERTICAL, bg=self.secondary_color, sashwidth=10)

        self.top_right_frame = Frame(self.vertically_pained_window, bg=self.secondary_color)
        self.grid_frame = Frame(self.top_right_frame, bg=self.secondary_color)
        

        from terminal import Terminal # needs nothing
        self.terminal = Terminal(self)

        from code_editor import CodeEditor # needs nothing
        self.code_editor = CodeEditor(self)

        from virtual_environment import GridManager # NEEDS Terminal, grid_frame
        self.grid_manager = GridManager(self, 0, 0)

        from file_management import FileManager # NEEDS GRID-MANAGER, code_editor, terminal
        self.file_manager = FileManager(self)

        from code_execution import CodeExecution 
        self.code_executor = CodeExecution(self)

        from settings import Settings
        self.settings = Settings(self)

        from toolbar import Toolbar # NEEDS GRID-MAN AND FILE-MANAGER AND CODE-EXECUTION AND SETTINGS
        self.toolbar = Toolbar(self) 

        from filetree import Filetree # NEEDS FILE-MANAGER
        self.filetree = Filetree(self) 



        self.toolbar.frame.pack(side="top", fill="x")
        self.horizontally_paned_window.pack(side="bottom", fill="both", expand=1)
        self.grid_frame.pack(anchor=NE)

        self.horizontally_paned_window.add(self.filetree.frame)
        self.horizontally_paned_window.add(self.code_editor.frame)  
        self.horizontally_paned_window.add(self.vertically_pained_window)

        self.vertically_pained_window.add(self.top_right_frame)  
        self.vertically_pained_window.add(self.terminal.frame)  


        # Alle widgets updaten, um die screen_width/screen_height zu updaten
        self.update_idletasks()
        # Seperatoren von den Pained Windows placen
        self.horizontally_paned_window.sash_place(0, int(self.screen_width*.125), 0)
        self.horizontally_paned_window.sash_place(1, int(self.screen_width*0.5625), 0)
        self.vertically_pained_window.sash_place(0, 0, int((self.vertically_pained_window.winfo_height())/2)-1)

        self.file_manager.open_python_file_and_grid_from_options()
        self.code_editor.frame.update_line_numbers()        
        self.bind("<Control-s>", lambda event: self.file_manager.save_python_file_and_grid())

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def update_colors(self):
        self.configure(bg=self.secondary_color)
        self.horizontally_paned_window.configure(bg=self.secondary_color)
        self.vertically_pained_window.configure(bg=self.secondary_color)
        self.top_right_frame.configure(bg=self.secondary_color)
        self.grid_frame.configure(bg=self.secondary_color)

        self.style.configure("Treeview", background=self.secondary_color, foreground=self.foreground_color, fieldbackground=self.secondary_color)
        self.style.map("Treeview", background=[("selected", self.primary_color)])

        self.style.configure("My.Horizontal.TScrollbar", troughcolor=self.secondary_color, background=self.primary_color, width=20, bordercolor =self.secondary_color, arrowsize="20")#, arrowcolor="FFFFFF") 
        self.style.configure("My.Vertical.TScrollbar", troughcolor=self.secondary_color, background=self.primary_color, width=20, bordercolor=self.secondary_color, arrowsize="20")#, arrowcolor="FFFFFF")

        self.code_editor.frame.configure(bg=self.primary_color)
        self.code_editor.frame.plus_scrollbar_frame.configure(bg=self.primary_color)
        self.code_editor.frame.text_widget.configure(bg=self.primary_color, fg=self.foreground_color, insertbackground=self.foreground_color, selectbackground="#6F6F6F")
        self.code_editor.frame.line_number_text_widget.configure(bg=self.primary_color, fg=self.foreground_color, insertbackground=self.foreground_color, selectbackground="#6F6F6F")
        self.code_editor.frame.line_number_frame.configure(bg=self.secondary_color, highlightbackground=self.primary_color)

 
        self.terminal.frame.configure(bg=self.primary_color)
        self.terminal.frame.plus_scrollbar_frame.configure(bg=self.primary_color)
        self.terminal.frame.text_widget.configure(bg=self.primary_color, fg=self.foreground_color, insertbackground=self.foreground_color, selectbackground="#6F6F6F")

        self.filetree.frame.configure(bg=self.secondary_color)

        self.toolbar.frame.configure(bg=self.secondary_color)

        self.toolbar.tick_rate_slider.configure(bg=self.secondary_color, activebackground=self.secondary_color, highlightbackground=self.secondary_color, fg=self.foreground_color, troughcolor=self.primary_color)

        for button in button_list:
            try:
                button.configure(bg=self.primary_color, activebackground=self.secondary_color, fg=self.foreground_color, activeforeground=self.foreground_color)
            except tk.TclError:
                pass
        for cell in self.grid_manager.cells:
            if cell.type == "hamster" or cell.type == "empty":
                cell.canvas.configure(bg=self.primary_color)
            if cell.type == "wall":
                cell.canvas.configure(bg=self.secondary_color)

        

        self.color_delegator.tagdefs.update({
            'COMMENT': {'foreground': '#AAAAAA', 'background': self.primary_color},
            'KEYWORD': {'foreground': '#D67CBC', 'background': self.primary_color},
            'BUILTIN': {'foreground': '#71BFFF', 'background': self.primary_color},
            'STRING': {'foreground': '#A8D37E', 'background': self.primary_color},
            'DEFINITION': {'foreground': '#71BFFF', 'background': self.primary_color},
        })
        self.code_editor.percolator.removefilter(self.color_delegator)
        self.code_editor.percolator.insertfilter(self.color_delegator) 

    def on_closing(self):
        #check if the user wants to save the current file and grid before closing
        if self.remember_last_file == "False":
            settings_handler.set_variable("current_file_directory", "")
        if self.remember_last_grid == "False":
            settings_handler.set_variable("current_grid_directory", "")
        if self.remember_last_directory == "False":
            settings_handler.set_variable("current_filetree_directory", "")
        self.destroy()
           

root = Root()








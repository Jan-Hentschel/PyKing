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
        self.settings_variables = {
            "ask_to_save_on_close" : settings_handler.get_variable("ask_to_save_on_close"),

            "remember_last_file" : settings_handler.get_variable("remember_last_file"),
            "remember_last_grid" : settings_handler.get_variable("remember_last_grid"),
            "remember_last_directory" : settings_handler.get_variable("remember_last_directory"),
            
            "show_snake_actions_in_terminal" : settings_handler.get_variable("show_snake_actions_in_terminal"),
            "show_debugger_prints" : settings_handler.get_variable("show_debugger_prints"),

            "gore" : settings_handler.get_variable("gore")

        }



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
        self.bottom_right_frame = Frame(self.vertically_pained_window, bg=self.secondary_color)
        self.leftest_frame = Frame(self.horizontally_paned_window, bg=self.secondary_color)
        self.left_frame = Frame(self.horizontally_paned_window, bg=self.secondary_color)
        

        from terminal import Terminal # needs nothing
        self.terminal: Terminal = Terminal(self, self.bottom_right_frame)

        from code_editor import CodeEditor # needs nothing
        self.code_editor: CodeEditor = CodeEditor(self, self.left_frame)

        from settings import Settings # needs nothing
        self.settings: Settings = Settings(self)

        from virtual_environment import GridManager # NEEDS terminal
        self.grid_manager: GridManager = GridManager(self, self.top_right_frame, 0, 0)

        from file_management import FileManager # NEEDS grid_manager, code_editor, terminal
        self.file_manager: FileManager = FileManager(self)

        from filetree import Filetree # NEEDS file_manager
        self.filetree: Filetree = Filetree(self, self.leftest_frame) 

        from code_execution import CodeExecution #NEEDS Snake 
        self.code_executor: CodeExecution = CodeExecution(self)

        from toolbar import Toolbar # NEEDS grid_manager AND file_manager AND code_executor AND settings
        self.toolbar: Toolbar = Toolbar(self) 
        self.toolbar.frame.pack(side="top", fill="x")


        
        self.horizontally_paned_window.pack(side="bottom", fill="both", expand=1)

        self.horizontally_paned_window.add(self.leftest_frame)
        self.horizontally_paned_window.add(self.left_frame)  
        self.horizontally_paned_window.add(self.vertically_pained_window)

        self.vertically_pained_window.add(self.top_right_frame)  
        self.vertically_pained_window.add(self.bottom_right_frame)  


        # Alle widgets updaten, um die screen_width/screen_height zu updaten
        self.update_idletasks()
        # Seperatoren von den Pained Windows placen
        self.horizontally_paned_window.sash_place(0, int(self.screen_width*.125), 0)
        self.horizontally_paned_window.sash_place(1, int(self.screen_width*0.5625), 0)
        self.vertically_pained_window.sash_place(0, 0, int((self.vertically_pained_window.winfo_height())/2)-1)

        self.file_manager.open_python_file_and_grid_from_options()
        self.code_editor.update_line_numbers()        
        self.bind("<Control-s>", lambda event: self.file_manager.save_python_file_and_grid())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #CustomWidget.print_widgets()

        
    def update_colors(self):
        self.configure(bg=self.secondary_color)
        self.horizontally_paned_window.configure(bg=self.secondary_color)
        self.vertically_pained_window.configure(bg=self.secondary_color)
        self.top_right_frame.configure(bg=self.secondary_color)

        self.style.configure("Treeview", background=self.secondary_color, foreground=self.foreground_color, fieldbackground=self.secondary_color)
        self.style.map("Treeview", background=[("selected", self.primary_color)])

        self.style.configure("My.Horizontal.TScrollbar", troughcolor=self.secondary_color, background=self.primary_color, width=20, bordercolor =self.secondary_color, arrowsize="20")#, arrowcolor="FFFFFF") 
        self.style.configure("My.Vertical.TScrollbar", troughcolor=self.secondary_color, background=self.primary_color, width=20, bordercolor=self.secondary_color, arrowsize="20")#, arrowcolor="FFFFFF")

        #CustomWidget.print_widgets()
        for widget in CustomWidget.widget_list:
            try:
                widget.update_color()
            except AttributeError:
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
        if self.settings_variables["ask_to_save_on_close"] == "True":
            self.ask_if_save_on_close()
        else:
            self.close()

    def ask_if_save_on_close(self):
        self.popup = DefaultToplevel(self, padx=10, pady=10)
        self.popup.geometry("325x120")
        self.popup.title("Are you sure?")
        self.popup.iconbitmap(resource_path("Assets\\Icon.ico"))

        self.popup.are_you_sure_label = DefaultLabel(self.popup, text="Are you sure you want to close?\nDo you want to save the current file and grid?")
        
        self.popup.save_button = DefaultButton(self.popup, text="Save", command=lambda: self.save_before_closing(), padx=50)
        self.popup.save_button.pack()

        self.popup.dont_save_button = DefaultButton(self.popup, text="Don't Save", command=lambda: self.close(), padx=10)
        self.popup.dont_save_button.pack()

        self.popup.cancel_button = DefaultButton(self.popup, text="Cancel", command= lambda: self.cancel_closing(), padx=10)
        self.popup.cancel_button.pack()

    def save_before_closing(self):
        self.file_manager.save_python_file_and_grid()
        self.destroy()
           
    def close(self):
        if self.settings_variables["remember_last_file"] == "False":
            settings_handler.set_variable("current_file_directory", "")
        if self.settings_variables["remember_last_grid"] == "False":
            settings_handler.set_variable("current_grid_directory", "")
        if self.settings_variables["remember_last_directory"] == "False":
            settings_handler.set_variable("current_filetree_directory", "")
        self.destroy()

    def cancel_closing(self):
        self.popup.destroy()
        

root: Root = Root()








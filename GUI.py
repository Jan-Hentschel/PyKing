import tkinter as tk
from tkinter import *
from ctypes import windll
from tkinter import ttk

from utility import resource_path
#damit text nicht blurry ist



class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        windll.shcore.SetProcessDpiAwareness(2)
        super().__init__(*args, **kwargs)
        self.title("PyKing")
        self.iconbitmap(resource_path("Assets\\Icon.ico"))

        self.screen_height = self.winfo_screenheight()
        self.screen_width = self.winfo_screenwidth()
        self.geometry(f"{self.screen_width}x{self.screen_height}")

        self.state('zoomed')

        self.primary_color = "#3F3F3F"
        self.secondary_color = "#333333"

        #scrollbars
        self.style = ttk.Style()
        self.style.theme_use("default")# Define a vertical scrollbar style

        self.style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333")
        self.style.map("Treeview", background=[("selected", "#3F3F3F")])

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
        
        self.style.configure("My.Horizontal.TScrollbar", troughcolor="#333333", background="#3F3F3F", width=20, bordercolor ="#333333", arrowsize="20")#, arrowcolor="FFFFFF") 
        self.style.configure("My.Vertical.TScrollbar", troughcolor="#333333", background="#3F3F3F", width=20, bordercolor="#333333", arrowsize="20")#, arrowcolor="FFFFFF")
 



        self.configure(bg=self.secondary_color)
        self.horizontally_paned_window = PanedWindow(self, orient=tk.HORIZONTAL, bg=self.secondary_color, sashwidth = 10)
        self.horizontally_paned_window.pack(side="bottom", fill="both", expand=1)


        self.vertically_pained_window = PanedWindow(self.horizontally_paned_window, orient=tk.VERTICAL, bg=self.secondary_color, sashwidth=10)

        self.top_right_frame = Frame(self.vertically_pained_window, bg=self.secondary_color)
        self.grid_frame = Frame(self.top_right_frame, bg=self.secondary_color)
        self.grid_frame.pack(anchor=NE)

        from terminal import Terminal # needs nothing
        self.terminal = Terminal(self)

        from code_editor import CodeEditor # needs nothing
        self.code_editor = CodeEditor(self)

        from virtual_environment import GridManager # NEEDS Terminal, grid_frame
        self.grid_manager = GridManager(self, 9, 5)

        from file_management import FileManager # NEEDS GRID-MANAGER, code_editor, terminal
        self.file_manager = FileManager(self)

        from code_execution import CodeExecution 
        self.code_executor = CodeExecution(self)

        from settings import Settings
        self.settings = Settings(self)

        from toolbar import Toolbar # NEEDS GRID-MAN AND FILE-MANAGER AND CODE-EXECUTION AND SETTINGS
        self.toolbar = Toolbar(self) 

        from filetree import Filetree # NEEDS FILE-MANAGER
        self.file_tree = Filetree(self) 



        self.toolbar.frame.pack(side="top", fill="x")

        self.horizontally_paned_window.add(self.file_tree.frame)
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
        self.bind("<Control-s>", lambda event: self.file_manager.save_python_file_and_grid())
        
    def update_colors(self):
        self.configure(bg=self.secondary_color)
        self.horizontally_paned_window.configure(bg=self.secondary_color)
        self.vertically_pained_window.configure(bg=self.secondary_color)
        self.top_right_frame.configure(bg=self.secondary_color)
        self.grid_frame.configure(bg=self.secondary_color)


root = Root()



# from terminal import terminal
# from toolbar import toolbar
# from filetree import file_tree
# from code_editor import code_editor

# toolbar.frame.pack(side="top", fill="x")

# root.horizontally_paned_window.add(file_tree.frame)
# root.horizontally_paned_window.add(code_editor.frame)  
# root.horizontally_paned_window.add(root.vertically_pained_window)

# root.vertically_pained_window.add(root.top_right_frame)  
# root.vertically_pained_window.add(terminal.frame)  


# # Alle widgets updaten, um die screen_width/screen_height zu updaten
# root.update_idletasks()
# # Seperatoren von den Pained Windows placen
# root.horizontally_paned_window.sash_place(0, int(root.screen_width*.125), 0)
# root.horizontally_paned_window.sash_place(1, int(root.screen_width*0.5625), 0)
# root.vertically_pained_window.sash_place(0, 0, int((root.vertically_pained_window.winfo_height())/2)-1)







import tkinter as tk
from tkinter import *
from ctypes import windll

from utility import resource_path
#damit text nicht blurry ist

windll.shcore.SetProcessDpiAwareness(2)

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("PyKing")
        self.iconbitmap(resource_path("Assets\\Icon.ico"))

        self.screen_height = self.winfo_screenheight()
        self.screen_width = self.winfo_screenwidth()
        self.geometry(f"{self.screen_width}x{self.screen_height}")

        self.state('zoomed')

        self.configure(bg="#333333")
        self.horizontally_paned_window = PanedWindow(self, orient=tk.HORIZONTAL, bg="#333333", sashwidth = 10)
        self.horizontally_paned_window.pack(side="bottom", fill="both", expand=1)


        self.vertically_pained_window = PanedWindow(self.horizontally_paned_window, orient=tk.VERTICAL, bg="#333333", sashwidth=10)

        self.top_right_frame = Frame(self.vertically_pained_window, bg="#333333")
        self.grid_frame = Frame(self.top_right_frame, bg="#333333")
        self.grid_frame.pack(anchor=NE)

        from terminal import Terminal # needs nothing
        self.terminal = Terminal(self)

        from code_editor import CodeEditor # needs nothing
        self.code_editor = CodeEditor(self)

        from virtual_environment import GridManager # NEEDS Terminal, grid_frame
        self.grid_manager = GridManager(self, 9, 5)

        from file_management import FileManager # NEEDS GRID-MANAGER, code_editor, terminal
        self.file_manager = FileManager(self)

        from toolbar import Toolbar # NEEDS GRID-MAN AND FILE-MANAGER
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







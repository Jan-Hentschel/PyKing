import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(2)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# Initialisierung des Windows
root = Tk()
root.title("PyKing")
root.iconbitmap(resource_path(".\\dist\\Assets\\Icon.ico"))

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x{screen_height}")

root.state('zoomed')

root.configure(background='black')
# print(screenHeight)
# print(screenWidth)

# alle modules importieren nachdem root erstellt wurde (sonst circular dependency)
from toolbar import *





#toolbar in das window packen
toolbar.pack(fill="x")


# Horizontales Pained Window erstellen
horizontally_paned_window = PanedWindow(root, orient=tk.HORIZONTAL)
horizontally_paned_window.pack(fill="both", expand=1)


from filetree import *
horizontally_paned_window.add(file_tree_widget)

from code_editor import *  
horizontally_paned_window.add(code_editor_widget)  


# Vertikales Pained Window im Horizontalen Pained Window erstellen (rechts)
vertically_pained_window = PanedWindow(horizontally_paned_window, orient=tk.VERTICAL)
horizontally_paned_window.add(vertically_pained_window)  

from virtual_environment import *
vertically_pained_window.add(virtual_environment_widget)  

from terminal import *
vertically_pained_window.add(terminal_widget)  



# Alle widgets updaten, um die screen_width/screen_height zu updaten
root.update_idletasks()

# Seperatoren von den Pained Windows placen
horizontally_paned_window.sash_place(0, int(screen_width*.125), 0)
horizontally_paned_window.sash_place(1, int(screen_width*0.5625), 0)
vertically_pained_window.sash_place(0, 2000, int((vertically_pained_window.winfo_height())/2)-1)






import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys
from ctypes import windll

#damit text nicht blurry ist
windll.shcore.SetProcessDpiAwareness(2)

#https://www.youtube.com/watch?v=p3tSLatmGvU
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
#vor jeden relative path diese funktion setzen um pyinstaller zu helfen alle dateien zu finden
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#https://tkdocs.com/
#https://www.geeksforgeeks.org/python-gui-tkinter/
# Initialisierung des Windows als root
root = Tk()
root.title("PyKing")
root.iconbitmap(resource_path(".\\dist\\Assets\\Icon.ico"))

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x{screen_height}")

root.state('zoomed')

root.configure(bg="#333333")

# Horizontales Pained Window erstellen
horizontally_paned_window = PanedWindow(root, orient=tk.HORIZONTAL, bg="#333333", sashwidth = 10)
horizontally_paned_window.pack(side="bottom", fill="both", expand=1)

# filetree importieren und in das paned window einfügen
from filetree import *
horizontally_paned_window.add(file_tree_widget)

# code editor importieren und in das paned window einfügen
from code_editor import *  
horizontally_paned_window.add(code_editor_frame)  


# Vertikales Pained Window im Horizontalen Pained Window erstellen (rechts)
vertically_pained_window = PanedWindow(horizontally_paned_window, orient=tk.VERTICAL, bg="#333333", sashwidth=10)
horizontally_paned_window.add(vertically_pained_window)  
# toolbar importieren und in das window packen

# virtual environment importieren und in das paned window einfügen
from virtual_environment import virtual_environment_frame
vertically_pained_window.add(virtual_environment_frame)  

# terminal importieren und in das paned window einfügen
from terminal import *
vertically_pained_window.add(terminal_frame)  

from toolbar import toolbar_frame
toolbar_frame.pack(side="top", fill="x")



# Alle widgets updaten, um die screen_width/screen_height zu updaten
root.update_idletasks()
# Seperatoren von den Pained Windows placen
horizontally_paned_window.sash_place(0, int(screen_width*.125), 0)
horizontally_paned_window.sash_place(1, int(screen_width*0.5625), 0)
vertically_pained_window.sash_place(0, 0, int((vertically_pained_window.winfo_height())/2)-1)






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



toolbar = Frame(root, height=68)
toolbar.pack(fill="x")



# Horizontales Pained Window erstellen
horizontally_paned_window = PanedWindow(root, orient=tk.HORIZONTAL)
horizontally_paned_window.pack(fill="both", expand=1)


# Frame für den Filetree erstellen (links)
file_tree_widget = Frame(horizontally_paned_window, bg="blue")
horizontally_paned_window.add(file_tree_widget)




# Text-Feld für den Code Editor erstellen (mitte)
code_editor_widget = Text(horizontally_paned_window)  
horizontally_paned_window.add(code_editor_widget)  



# Vertikales Pained Window im Horizontalen Pained Window erstellen (rechts)
vertically_pained_window = PanedWindow(horizontally_paned_window, orient=tk.VERTICAL)
horizontally_paned_window.add(vertically_pained_window)  



# Das Grid erstellen (oben rechts)
grid_widget = Frame(vertically_pained_window, bg="green")  
vertically_pained_window.add(grid_widget)  
grid_label = Label(grid_widget, text="Game Grid", bg="lightblue")
grid_label.pack(expand=True)


# Terminal Textfeld erstellen (unten rechts)
terminal_widget = Text(vertically_pained_window, bg="black", fg="white")  # Create a Text widget as a terminal
terminal_widget.insert(tk.END, "Terminal output here...\n")
vertically_pained_window.add(terminal_widget)  # Add the terminal to the vertical PanedWindow


# Alle widgets updaten, um die screen_width/screen_height zu updaten
root.update_idletasks()

# Seperatoren von den Pained Windows placen
horizontally_paned_window.sash_place(0, int(screen_width*.125), 0)
horizontally_paned_window.sash_place(1, int(screen_width*0.5625), 0)
vertically_pained_window.sash_place(0, 2000, int((vertically_pained_window.winfo_height())/2)-1)






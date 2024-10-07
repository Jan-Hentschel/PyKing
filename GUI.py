import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys



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
frame = ttk.Frame(root, padding=100)



# Create a PanedWindow with horizontal orientation
horizontallyPanedWindow = PanedWindow(root, orient=tk.HORIZONTAL)
horizontallyPanedWindow.pack(fill=tk.BOTH, expand=1)

# Create the first pane (left) for the code editor
codeEditorWidget = Text(horizontallyPanedWindow, width=40, height=20, wrap="none")  # Create a Text widget as a code editor
horizontallyPanedWindow.add(codeEditorWidget)  # Add the code editor to the horizontal PanedWindow

# Create another PanedWindow inside the right pane (this time vertical)
verticallyPainedWindow = PanedWindow(horizontallyPanedWindow, orient=tk.VERTICAL)
horizontallyPanedWindow.add(verticallyPainedWindow)  # Add the vertical PanedWindow to the horizontal one

# Create the third pane (top-right) for the playing grid
grid_frame = Frame(verticallyPainedWindow, bg="green", width=300, height=300)  # A placeholder frame for the playing grid
verticallyPainedWindow.add(grid_frame)  # Add the playing grid to the vertical PanedWindow

# Create the second pane (botto,-right) for the terminal
terminalWidget = Text(verticallyPainedWindow, width=40, height=10, bg="black", fg="white")  # Create a Text widget as a terminal
terminalWidget.insert(tk.END, "Terminal output here...\n")
verticallyPainedWindow.add(terminalWidget)  # Add the terminal to the vertical PanedWindow

# Example content in the grid (can be replaced with your actual game grid)
grid_label = Label(grid_frame, text="Game Grid", bg="lightblue")
grid_label.pack(expand=True)
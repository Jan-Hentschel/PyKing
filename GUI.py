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

screenHeight = root.winfo_screenheight()
screenWidth = root.winfo_screenwidth()
root.geometry(f"{screenWidth}x{screenHeight}")

root.state('zoomed')

root.configure(background='black')
# print(screenHeight)
# print(screenWidth)
totalWidthPadding = 8



toolbar = Frame(root, height=68)
toolbar.pack(fill="x")



# Create a PanedWindow with horizontal orientation
horizontallyPanedWindow = PanedWindow(root, orient=tk.HORIZONTAL)
horizontallyPanedWindow.pack(fill="both", expand=1)



fileTreeWidget = Frame(horizontallyPanedWindow, bg="blue")
horizontallyPanedWindow.add(fileTreeWidget)




# Create the first pane (left) for the code editor
codeEditorWidget = Text(horizontallyPanedWindow)  # Create a Text widget as a code editor
horizontallyPanedWindow.add(codeEditorWidget)  # Add the code editor to the horizontal PanedWindow



# Create another PanedWindow inside the right pane (this time vertical)
verticallyPainedWindow = PanedWindow(horizontallyPanedWindow, orient=tk.VERTICAL)
horizontallyPanedWindow.add(verticallyPainedWindow)  # Add the vertical PanedWindow to the horizontal one



# Create the third pane (top-right) for the playing grid
gridFrame = Frame(verticallyPainedWindow, bg="green")  # A placeholder frame for the playing grid
verticallyPainedWindow.add(gridFrame)  # Add the playing grid to the vertical PanedWindow
grid_label = Label(gridFrame, text="Game Grid", bg="lightblue")
grid_label.pack(expand=True)


# Create the second pane (bottom-right) for the terminal
terminalWidget = Text(verticallyPainedWindow, bg="black", fg="white")  # Create a Text widget as a terminal
terminalWidget.insert(tk.END, "Terminal output here...\n")
verticallyPainedWindow.add(terminalWidget)  # Add the terminal to the vertical PanedWindow

root.update_idletasks()

horizontallyPanedWindow.sash_place(0, int(screenWidth*.125), 0)
horizontallyPanedWindow.sash_place(1, int(screenWidth*0.5625), 0)
verticallyPainedWindow.sash_place(0, 2000, int((verticallyPainedWindow.winfo_height())/2)-1)



# root.update_idletasks()
# print(verticallyPainedWindow.winfo_height())
# print(gridFrame.winfo_height())
# print(terminalWidget.winfo_height())
# print(fileTreeWidget.winfo_width()+codeEditorWidget.winfo_width()+verticallyPainedWindow.winfo_width())


import tkinter as tk
from tkinter import Text, PanedWindow, Label, Frame

# Create the main window
root = tk.Tk()
root.title("Resizable Layout")

# Create a PanedWindow with horizontal orientation
h_paned = PanedWindow(root, orient=tk.HORIZONTAL)
h_paned.pack(fill=tk.BOTH, expand=1)

# Create the first pane (left) for the code editor
code_editor = Text(h_paned, width=40, height=20, wrap="none")  # Create a Text widget as a code editor
h_paned.add(code_editor)  # Add the code editor to the horizontal PanedWindow

# Create another PanedWindow inside the right pane (this time vertical)
v_paned = PanedWindow(h_paned, orient=tk.VERTICAL)
h_paned.add(v_paned)  # Add the vertical PanedWindow to the horizontal one

# Create the second pane (top-right) for the terminal
terminal = Text(v_paned, width=40, height=10, bg="black", fg="white")  # Create a Text widget as a terminal
terminal.insert(tk.END, "Terminal output here...\n")
v_paned.add(terminal)  # Add the terminal to the vertical PanedWindow

# Create the third pane (bottom-right) for the playing grid
grid_frame = Frame(v_paned, bg="green", width=300, height=300)  # A placeholder frame for the playing grid
v_paned.add(grid_frame)  # Add the playing grid to the vertical PanedWindow

# Example content in the grid (can be replaced with your actual game grid)
grid_label = Label(grid_frame, text="Game Grid", bg="lightblue")
grid_label.pack(expand=True)

# Run the Tkinter event loop
root.mainloop()
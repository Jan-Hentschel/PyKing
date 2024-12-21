import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import vertically_pained_window, resource_path
 
# Das Virtual Environment erstellen (oben rechts)
virtual_environment_frame = Frame(vertically_pained_window, bg="#333333")
grid_frame = Frame(virtual_environment_frame, bg="#333333")
grid_frame.pack(expand=True, anchor=CENTER)

grid_height = 5
grid_width = 7

# Load the .gif image file.
gif1 = tk.PhotoImage(file=resource_path('.\\dist\\Assets\\LogoV1.3.png'))
# test = Canvas(grid_frame, width=100, height=100, background="#3F3F3F", highlightthickness=0)
# test.pack(side=TOP)
# test.create_image(50, 50, image=gif1, anchor=SW)
# Put gif image on canvas.
# Pic's upper-left corner (NW) on the canvas is at x=50 y=10.


for y in range(grid_height):
    for x in range(grid_width):
        if x==1 and y == 1:
            yo = Canvas(grid_frame, width=100, height=100, background="#3F3F3F", highlightthickness=0)
            yo.grid(row=grid_height-y, column=x, padx=5, pady=5, sticky=SW)
            yo.create_image(18, 18, image=gif1, anchor=NW)
        else:
            Canvas(grid_frame, width=100, height=100, background="#3F3F3F", highlightthickness=0).grid(row=grid_height-y, column=x, padx=5, pady=5, sticky=SW)
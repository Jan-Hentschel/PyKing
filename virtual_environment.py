import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import vertically_pained_window, resource_path
 
# Das Virtual Environment erstellen (oben rechts)
virtual_environment_frame = Frame(vertically_pained_window, bg="#333333")
grid_frame = Frame(virtual_environment_frame, bg="#333333")
grid_frame.pack(expand=True, anchor=CENTER)


logo = tk.PhotoImage(file=resource_path('.\\dist\\Assets\\LogoV1.3.png'))

class GridManager:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cells = []
    
    def create_cells(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                current_cell = GridCell(x, y)
                current_cell.append_to_cells()

    def add_cells_to_grid(self):
        for cell in self.cells:
            cell.add_to_grid()

    def display_image_at_position(self, image, x, y):
        for cell in self.cells:
            if cell.x==x and cell.y == y:
                cell.display_image(image)
class GridCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.canvas = Canvas(grid_frame, width=100, height=100, background="#3F3F3F", highlightthickness=0)

    def add_to_grid(self):
        self.canvas.create_text(50, 50, text=f"x={self.x}, y={self.y}", fill="white")
        self.canvas.grid(row=grid_man.grid_height - self.y, column=self.x, padx=5, pady=5, sticky=SW)

    def append_to_cells(self):
        grid_man.cells.append(self)

    def display_image(self, image):
        self.canvas.create_image(18, 18, image=image, anchor=NW)

grid_man = GridManager(7, 5)
grid_man.create_cells()
grid_man.add_cells_to_grid()
grid_man.display_image_at_position(logo, 1, 1)







        
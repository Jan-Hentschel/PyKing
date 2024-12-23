import tkinter as tk
from tkinter import *
from tkinter import ttk

from terminal import terminal_widget
from gui import vertically_pained_window, resource_path
 
# Das Virtual Environment erstellen (oben rechts)
virtual_environment_frame = Frame(vertically_pained_window, bg="#333333")
grid_frame = Frame(virtual_environment_frame, bg="#333333")
grid_frame.pack(anchor=NE)

def throw_error_to_terminal(string):
    terminal_widget.insert(tk.END, string + "\n")

logo = tk.PhotoImage(file=resource_path('.\\dist\\Assets\\LogoV1.3.png'))
up_image = tk.PhotoImage(file=resource_path('.\\dist\\Assets\\Up.png'))
down_image = tk.PhotoImage(file=resource_path('.\\dist\\Assets\\Down.png'))
left_image= tk.PhotoImage(file=resource_path('.\\dist\\Assets\\Left.png'))
right_image = tk.PhotoImage(file=resource_path('.\\dist\\Assets\\Right.png'))

class GridManager:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cells = []
    
    def create_cells(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                current_cell = GridCell(x, y, "empty")
                current_cell.append_to_cells()

    def add_cells_to_grid(self):
        for cell in self.cells:
            cell.add_to_grid()

    def display_image_at_position(self, image, x, y):
        for cell in self.cells:
            if cell.x==x and cell.y == y:
                cell.display_image(image)

    def clear_all_cells(self):
        for cell in self.cells:
            cell.clear_cell()

class GridCell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.canvas = Canvas(grid_frame, width=100, height=100, background="#3F3F3F", highlightthickness=0)

    def add_to_grid(self):
        #self.canvas.create_text(50, 50, text=f"x={self.x}, y={self.y}", fill="white")
        self.canvas.grid(row=grid_man.grid_height - self.y, column=self.x, padx=5, pady=5, sticky=N+E+S+W)

    def append_to_cells(self):
        grid_man.cells.append(self)

    def display_image(self, image):
        self.canvas_image = self.canvas.create_image(18, 18, image=image, anchor=NW)

    def clear_cell(self):
        self.canvas.delete("all")

    def change_cell_type(self, new_type):
        self.type = new_type



class Snake:

    def is_outside_grid(self):
        if self.y < grid_man.grid_height and self.x < grid_man.grid_width and self.y >= 0 and self.x >= 0:
            return False
        else:
            return True
        
    def update_cell(self):
        for cell in grid_man.cells:
            if cell.x == self.x and cell.y == self.y:
                self.cell = cell

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        if self.is_outside_grid():
            del self
            raise Exception("you tried to put a snake outside of the grid... fucking looser, now it killed itself")

        
        self.update_cell()

        self.direction = direction

        match self.direction:
            case "N":
                self.image = up_image                
            case "E":
                self.image = right_image                
            case "S":
                self.image = down_image
            case "W":
                self.image = left_image

        self.cell.display_image(self.image)



    def forward(self):
        self.delete_snake_image()
        match self.direction:
            case "N":
                if self.y+1 < grid_man.grid_height:
                    self.y +=1
                else:
                    throw_error_to_terminal("your ran into a wall... fucking idiot")                  
            case "E":
                if self.x+1 < grid_man.grid_width:
                    self.x +=1
                else:
                    throw_error_to_terminal("your ran into a wall... fucking idiot")   
            case "S":
                if self.y-1 >= 0:
                    self.y -=1
                else:
                    throw_error_to_terminal("your ran into a wall... fucking idiot")                   
            case "W":
                if self.x-1 >= 0:
                    self.x -=1
                else:
                    throw_error_to_terminal("your ran into a wall... fucking idiot")                    
        self.update_cell()
        self.show_snake()

    def turn_right(self):
        self.delete_snake_image()
        match self.direction:
            case "N":
                self.direction="E"
                self.image = right_image
            case "E":
                self.direction="S"
                self.image = down_image

            case "S":
                self.direction="W"
                self.image = left_image

            case "W":
                self.direction="N"
                self.image = up_image
        self.cell.canvas.itemconfig(self.cell.canvas_image, image=self.image)
        self.show_snake()


    def eat(self):
        terminal_widget.insert(tk.END, "ate")

    def spit(self):
        terminal_widget.insert(tk.END, "spat")

    def show_snake(self):
        self.cell.display_image(self.image)
    
    def delete_snake_image(self):
        self.cell.clear_cell()




grid_man = GridManager(10, 4)
grid_man.create_cells()
grid_man.add_cells_to_grid()

#snake = Snake(0, 0, "N")



# def forward_test(event):
#     snake.forward()

# def turn_right_test(event):
#     snake.turn_right()

# def eat_test(event):
#     snake.eat()

# def spit_test(event):
#     snake.spit()
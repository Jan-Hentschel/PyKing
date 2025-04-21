import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
from terminal import terminal_widget
from gui import vertically_pained_window, resource_path, root
import time


# Das Virtual Environment erstellen (oben rechts)
virtual_environment_frame = Frame(vertically_pained_window, bg="#333333")
grid_frame = Frame(virtual_environment_frame, bg="#333333")
grid_frame.pack(anchor=NE)

def throw_error_to_terminal(string):
    terminal_widget.insert(tk.END, string + "\n")

logo = PhotoImage(file=resource_path('Assets\\LogoV1.3.png'))
up_image = PhotoImage(file=resource_path('Assets\\Up.png'))
down_image = PhotoImage(file=resource_path('Assets\\Down.png'))
left_image= PhotoImage(file=resource_path('Assets\\Left.png'))
right_image = PhotoImage(file=resource_path('Assets\\Right.png'))
hamster_image = PhotoImage(file=resource_path('Assets\\Hamster.png'))



def wait_time():
    from toolbar import tick_rate_slider
    return 1/tick_rate_slider.get()


class GridManager:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cells = []
        self.create_cells()
        self.add_cells_to_grid()

    def create_cells(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.cells.append(GridCell(x, y, "empty"))
                
    def add_all_clickables(self):
        for cell in self.cells:
            cell.add_clickable()

    def delete_all_clickables(self):
        for cell in self.cells:
            if cell.type != "hamster":
                cell.canvas.delete(tk.ALL)


    def add_cells_to_grid(self):
        for cell in self.cells:
            cell.canvas.grid(row=self.grid_height - cell.y, column=cell.x, padx=5, pady=5, sticky=N+E+S+W)


    def clear_all_cells(self):
        for cell in self.cells:
            cell.clear()

    def reset_grid_to_start(self):
        for cell in self.cells:
            if cell.type == "empty":
                cell.clear()
            elif cell.type == "hamster":
                cell.clear()
                cell.type = "hamster"
                cell.display_image(hamster_image)

    def remove_all_cells(self):
        for cell in self.cells:
            cell.canvas.grid_remove()
            del cell
        self.cells = []
            


class GridCell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.canvas = Canvas(grid_frame, width=100, height=100, background="#3F3F3F", highlightthickness=0)
        self.hamsters = 0

    def edit(self):
        from toolbar import editing
        if editing == "add_hamster":
            self.add_hamster()
            self.add_clickable()
        elif editing == "subtract_hamster":
            if self.hamsters > 0:
                self.subtract_hamster()
                self.add_clickable()
            print(self.hamsters)
        elif editing == "make_wall":
            self.change_to_wall()
            self.canvas.delete(tk.ALL)
            self.add_clickable
        elif editing == "clear_cell":
            self.clear()
            self.canvas.delete(tk.ALL)
            self.add_clickable




    def add_clickable(self):
        if self.type == "empty":
            id = self.canvas.create_rectangle((0, 0, 101, 101), fill="#3F3F3F", outline="")
        elif self.type == "wall":
            id = self.canvas.create_rectangle((0, 0, 101, 101), fill="#333333", outline="")
        else:
            id = self.canvas_image
        self.canvas.tag_bind(id, "<Button-1>", lambda _: self.edit())

    def display_image(self, image):
        self.canvas_image = self.canvas.create_image(18, 18, image=image, anchor=NW)

    def change_to_wall(self):
        self.type = "wall"
        self.canvas.configure(background="#333333")

    def add_hamster(self):
        self.type = "hamster"
        self.display_image(hamster_image)
        self.hamsters += 1

    def subtract_hamster(self):
        self.hamsters -= 1
        if self.hamsters < 1:
            self.type = "empty"
            self.clear()

    def clear(self):
        self.type = "empty"
        self.canvas.delete("all")
        self.canvas.configure(background="#3F3F3F")

        

class Snake:

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        if self.is_outside_grid(self.x, self.y):
            del self
            raise Exception("you tried to put a snake outside of the grid... fucking looser, now it killed itself")
        self.hamsters = 0 #Einfügen dass man das voreinstellen kann

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
        root.update_idletasks()
        time.sleep(wait_time())


    def is_outside_grid(self, x, y):
        if y < grid_man.grid_height and x < grid_man.grid_width and y >= 0 and x >= 0:
            return False
        else:
            return True
        
    def update_cell(self):
        for cell in grid_man.cells:
            if cell.x == self.x and cell.y == self.y:
                self.cell = cell

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

        #self.cell.canvas.itemconfig(self.cell.canvas_image, image=self.image) <-- useless and breaks code (whyy?? just why)
        self.show_snake()
        root.update_idletasks()
        time.sleep(wait_time())

    def move(self):
        self.delete_snake_image()

        if not(self.can_move()):
            throw_error_to_terminal("you ran into a wall... fucking idiot")
            self.update_cell()
            self.show_snake()
            return
        
        match self.direction:
            case "N":
                if self.y+1 < grid_man.grid_height:
                    self.y +=1
                else:
                    throw_error_to_terminal("you ran into a wall... fucking idiot")
            case "E":
                if self.x+1 < grid_man.grid_width:
                    self.x +=1
                else:
                    throw_error_to_terminal("you ran into a wall... fucking idiot")
            case "S":
                if self.y-1 >= 0:
                    self.y -=1
                else:
                    throw_error_to_terminal("you ran into a wall... fucking idiot")
            case "W":
                if self.x-1 >= 0:
                    self.x -=1
                else:
                    throw_error_to_terminal("you ran into a wall... fucking idiot")
        self.update_cell()
        self.show_snake()
        root.update_idletasks()
        time.sleep(wait_time())



    def eat(self):
        if self.can_eat():
            self.hamsters += 1
            self.update_cell()
            self.cell.subtract_hamster()
            self.update_cell()
            self.show_snake()
        else:
            throw_error_to_terminal("what are you trying to eat dumbass?")
        root.update_idletasks()

        

    def spit(self):
        if self.can_spit():
            self.update_cell()
            self.cell.add_hamster()
        else:
            throw_error_to_terminal("spit what? your mouth is empty!")
            root.update_idletasks()

    def can_move(self):
        new_x = self.x
        new_y = self.y

        match self.direction:
            case "N":
                new_y+=1                 
            case "E":
                new_x+=1 
            case "S":
                new_y-=1  
            case "W":
                new_x-=1 
        
        for cell in grid_man.cells:
            if cell.x == new_x and cell.y == new_y:
                if cell.type == "wall":
                    return False
        if self.is_outside_grid(new_x, new_y):
            return False
        return True

    def can_eat(self):
        self.update_cell()
        if self.cell.type == "hamster":
            return True
        else: 
            return False

    def can_spit(self):
        self.update_cell()
        if self.hamsters > 0:
            return True
        else:
            return False
        
        

    def show_snake(self):
        self.cell.display_image(self.image)
    
    def delete_snake_image(self):
        if self.cell.type == "hamster":
            self.cell.clear()
            self.cell.type = "hamster"
            self.cell.display_image(hamster_image)
        else:
            self.cell.clear()




grid_man = GridManager(9, 5)

def change_grid_man(columns, rows):
    grid_man.remove_all_cells()
    grid_man.grid_width=columns
    grid_man.grid_height=rows
    grid_man.create_cells()
    grid_man.add_cells_to_grid()
    root.update_idletasks()

def change_grid(columns, rows, new_cells):
    change_grid_man(columns, rows)
    for i in range(len(new_cells)):
        old_cell = grid_man.cells[i]
        new_cell = new_cells[i]
        if new_cell == "empty":
            pass
        elif new_cell == "wall":
            old_cell.change_to_wall()
        else:
            cell_type, num_hamsters = new_cell.split()
            for i in range(int(num_hamsters)):
                old_cell.add_hamster()
        grid_man.delete_all_clickables()


def get_grid_dict():
    new_cells = []
    for cell in grid_man.cells:
        if cell.type == "wall":
            new_cells.append("wall")
        elif cell.type == "empty": 
            new_cells.append("empty")
        else:
            new_cells.append(f"hamster {cell.hamsters}")


    columns = grid_man.grid_width
    rows = grid_man.grid_height
    dictionary = {
        "columns": columns,
        "rows": rows,
        "cells": new_cells
    }
    return dictionary


from tkinter import *
import tkinter as tk
import time
import json

from utility import resource_path



class GridManager:
    def __init__(self, root, grid_width, grid_height):
        self.root = root
        self.grid_frame = Frame(self.root.top_right_frame, bg=self.root.secondary_color)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cells = []
        self.link = ""
        self.editing = None

        self.hamster_image = PhotoImage(file=resource_path('Assets\\Hamster.png'))
        self.up_image = PhotoImage(file=resource_path('Assets\\Up.png'))
        self.down_image = PhotoImage(file=resource_path('Assets\\Down.png'))
        self.left_image= PhotoImage(file=resource_path('Assets\\Left.png'))
        self.right_image = PhotoImage(file=resource_path('Assets\\Right.png'))

        self.create_cells()
        self.add_cells_to_grid()


    def create_cells(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.cells.append(GridCell(self.root, self, x, y, "empty"))
                
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
                cell.display_image(self.hamster_image)

    def remove_all_cells(self):
        for cell in self.cells:
            cell.canvas.grid_remove()
            del cell
            self.cells = []

    def change_grid_man(self, columns, rows):
        self.remove_all_cells()
        self.grid_width=columns
        self.grid_height=rows
        self.create_cells()
        self.add_cells_to_grid()
        self.root.update_idletasks()

    def change_grid(self, columns, rows, new_cells, link):
        self.link = link
        self.change_grid_man(columns, rows)
        for i in range(len(new_cells)):
            old_cell = self.cells[i]
            new_cell = new_cells[i]
            if new_cell == "empty":
                pass
            elif new_cell == "wall":
                old_cell.change_to_wall()
            else:
                cell_type, num_hamsters = new_cell.split()
                for i in range(int(num_hamsters)):
                    old_cell.add_hamster()
            self.delete_all_clickables()


    def get_grid_dict(self):
        new_cells = []
        for cell in self.cells:
            if cell.type == "wall":
                new_cells.append("wall")
            elif cell.type == "empty": 
                new_cells.append("empty")
            else:
                new_cells.append(f"hamster {cell.hamsters}")


        columns = self.grid_width
        rows = self.grid_height
        dictionary = {
            "link": self.link,
            "columns": columns,
            "rows": rows,
            "cells": new_cells
        }
        return json.dumps(dictionary, indent=4)
    
    def pick_add_hamster(self):
        self.editing = "add_hamster"
        self.add_all_clickables()
        self.root.terminal.show_current_directories(f"adding hamsters...")
        

    def pick_subtract_hamster(self):
        self.editing = "subtract_hamster"
        self.add_all_clickables()
        self.root.terminal.show_current_directories(f"subtracting hamsters...")

    def pick_make_wall(self):
        self.editing = "make_wall"
        self.add_all_clickables()
        self.root.terminal.show_current_directories(f"making walls...")

    def clear_cell(self):
        self.editing = "clear_cell"
        self.add_all_clickables()
        self.root.terminal.show_current_directories(f"clearing cells...")

    def edit_clear_all_cells(self):
        self.clear_all_cells()
        self.editing = None
        self.delete_all_clickables()
        self.root.terminal.show_current_directories(f"cleared all cells and cancelled editing grid")

    def cancel_editing_grid(self):
        self.editing = None
        self.delete_all_clickables()
        self.root.terminal.show_current_directories(f"cancelled editing grid")
        
        
    
class GridCell:
    def __init__(self, root, grid_manager,x, y, type):
        self.root = root
        self.hamster_image = PhotoImage(file=resource_path('Assets\\Hamster.png'))
        self.x = x
        self.y = y
        self.type = type
        self.canvas = Canvas(grid_manager.grid_frame, width=100, height=100, background=self.root.primary_color, highlightthickness=0)
        self.hamsters = 0
        self.canvas.hamster_number_text = None

    def edit(self):
        if self.root.grid_manager.editing == "add_hamster":
            self.add_hamster()
            self.add_clickable()
        elif self.root.grid_manager.editing == "subtract_hamster":
            if self.hamsters > 0:
                self.subtract_hamster()
                self.add_clickable()
        elif self.root.grid_manager.editing == "make_wall":
            self.change_to_wall()
            self.canvas.delete(tk.ALL)
            self.add_clickable
        elif self.root.grid_manager.editing == "clear_cell":
            self.clear()
            self.canvas.delete(tk.ALL)
            self.add_clickable




    def add_clickable(self):
        if self.type == "empty":
            id = self.canvas.create_rectangle((0, 0, 101, 101), fill=self.root.primary_color, outline="")
        elif self.type == "wall":
            id = self.canvas.create_rectangle((0, 0, 101, 101), fill=self.root.secondary_color, outline="")
        else:
            id = self.canvas_image
        self.canvas.tag_bind(id, "<Button-1>", lambda _: self.edit())

    def display_image(self, image):
        self.canvas_image = self.canvas.create_image(18, 18, image=image, anchor=NW)

    def change_to_wall(self):
        self.type = "wall"
        self.canvas.configure(background=self.root.secondary_color)

    def add_hamster(self):
        self.type = "hamster"
        self.display_image(self.hamster_image)
        self.hamsters += 1
        if self.canvas.hamster_number_text:
            self.canvas.itemconfigure(self.canvas.hamster_number_text, text=str(self.hamsters))
        else:
            self.canvas.hamster_number_text = self.canvas.create_text(
                91, 84,  # x, y position
                text=str(self.hamsters),
                fill="white",
                font=("Arial", 18, "bold")
            )


    def subtract_hamster(self):
        self.hamsters -= 1
        if self.hamsters < 1:
            self.type = "empty"
            self.clear()
            self.canvas.hamster_number_text = None
        else:
            self.canvas.itemconfigure(self.canvas.hamster_number_text, text=str(self.hamsters))

    def clear(self):
        self.type = "empty"
        self.canvas.delete("all")
        self.canvas.configure(background=self.root.primary_color)

class Snake:

    snakes = []

    def __init__(self, x=0, y=0, direction="N", name=None):
        from gui import root
        self.root = root
        try:
            self.x = int(x)
            self.y = int(y) 
        except ValueError:
            del self
            raise Exception("x and y are the first two parameters and must be integers")

        if name is not None:
            self.name = name
        else:
            self.name = f"Snake Nr.{len(Snake.snakes)+1}"
        Snake.snakes.append(self)

        if self.is_outside_grid(self.x, self.y):
            raise Exception(f"you tried to put {self.name} outside of the grid... it killed itself")

            
        self.hamsters = 0 #Einfügen dass man das voreinstellen kann

        self.update_cell()

        self.direction = direction

        match self.direction:
            case "N":
                self.image = root.grid_manager.up_image                
            case "E":
                self.image = root.grid_manager.right_image                
            case "S":
                self.image = root.grid_manager.down_image
            case "W":
                self.image = root.grid_manager.left_image

        self.cell.display_image(self.image)
        self.root.update_idletasks()
        time.sleep(self.wait_time())

    def wait_time(self):
        return 1/self.root.toolbar.tick_rate_slider.get()

    def is_outside_grid(self, x, y):
        from gui import root
        if y < root.grid_manager.grid_height and x < root.grid_manager.grid_width and y >= 0 and x >= 0:
            return False
        else:
            return True
        
    def update_cell(self):
        from gui import root
        for cell in root.grid_manager.cells:
            if cell.x == self.x and cell.y == self.y:
                self.cell = cell

    def turn_right(self):
        from gui import root
        self.delete_snake_image()

        match self.direction:
            case "N":
                self.direction="E"
                self.image = root.grid_manager.right_image
            case "E":
                self.direction="S"
                self.image = root.grid_manager.down_image

            case "S":
                self.direction="W"
                self.image = root.grid_manager.left_image

            case "W":
                self.direction="N"
                self.image = root.grid_manager.up_image

        #self.cell.canvas.itemconfig(self.cell.canvas_image, image=self.image) <-- useless and breaks code (whyy?? just why)
        self.show_snake()
        self.root.update_idletasks()
        if self.root.settings_variables["show_snake_actions_in_terminal"] == "True":
            self.root.terminal.print(f"{self.name}.turn_right()")
        time.sleep(self.wait_time())

    def move(self):
        from gui import root
        self.delete_snake_image()

        if not(self.can_move(False)):
            self.root.terminal.print(f"{self.name} ran into a wall...")
            self.update_cell()
            self.show_snake()
            return
        
        match self.direction:
            case "N":
                if self.y+1 < root.grid_manager.grid_height:
                    self.y +=1
                else:
                    self.root.terminal.print(f"{self.name} ran into a wall...")
            case "E":
                if self.x+1 < root.grid_manager.grid_width:
                    self.x +=1
                else:
                    self.root.terminal.print(f"{self.name} ran into a wall...")
            case "S":
                if self.y-1 >= 0:
                    self.y -=1
                else:
                    self.root.terminal.print(f"{self.name} ran into a wall...")
            case "W":
                if self.x-1 >= 0:
                    self.x -=1
                else:
                    self.root.terminal.print(f"{self.name} ran into a wall...")
        self.update_cell()
        self.show_snake()
        self.root.update_idletasks()
        if self.root.settings_variables["show_snake_actions_in_terminal"] == "True":
            self.root.terminal.print(f"{self.name}.move()")
        time.sleep(self.wait_time())



    def eat(self):
        if self.can_eat(False):
            self.hamsters += 1
            self.update_cell()
            self.cell.subtract_hamster()
            self.update_cell()
            self.show_snake()
            if self.root.settings_variables["show_snake_actions_in_terminal"] == "True":
                self.root.terminal.print(f"{self.name}.eat()")
        else:
            self.root.terminal.print(f"what is {self.name} trying to eat?")
        self.root.update_idletasks()
        time.sleep(self.wait_time())

        

    def spit(self):
        if self.can_spit(False):
            self.update_cell()
            self.delete_snake_image()
            self.cell.add_hamster()
            self.show_snake()
            if self.root.settings_variables["show_snake_actions_in_terminal"] == "True":
                self.root.terminal.print(f"{self.name}.spit()")
        else:
            self.root.terminal.print(f"what should {self.name} spit? their mouth is empty!")
            self.root.update_idletasks()
            time.sleep(self.wait_time())

    def can_move(self, show=True):
        from gui import root
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
        
        for cell in root.grid_manager.cells:
            if cell.x == new_x and cell.y == new_y:
                if cell.type == "wall":
                    if self.root.settings_variables["show_snake_actions_in_terminal"] == "True" and show:
                        self.root.terminal.print(f"{self.name}.can_move() - False")
                    return False
        if self.is_outside_grid(new_x, new_y):
            if self.root.settings_variables["show_snake_actions_in_terminal"] == "True" and show:
                self.root.terminal.print(f"{self.name}.can_move() - False")
            return False
        if self.root.settings_variables["show_snake_actions_in_terminal"] == "True" and show:
            self.root.terminal.print(f"{self.name}.can_move() - True")
        return True

    def can_eat(self, show=True):
        self.update_cell()
        if self.cell.type == "hamster":
            if self.root.settings_variables["show_snake_actions_in_terminal"] == "True" and show:
                self.root.terminal.print(f"{self.name}.can_eat() - True")
            return True
        else:
            if self.root.settings_variables["show_snake_actions_in_terminal"] == "True" and show:
                self.root.terminal.print(f"{self.name}.can_eat() - False")
            return False

    def can_spit(self, show=True):
        self.update_cell()
        if self.hamsters > 0:
            if self.root.settings_variables["show_snake_actions_in_terminal"] == "True" and show:
                self.root.terminal.print(f"{self.name}.can_spit() - True")
            return True
        else:
            if self.root.settings_variables["show_snake_actions_in_terminal"] == "True" and show:
                self.root.terminal.print(f"{self.name}.can_spit() - False")
            return False
        
        

    def show_snake(self):
        self.cell.display_image(self.image)
    
    def delete_snake_image(self):
        from gui import root
        if self.cell.type == "hamster":
            self.cell.clear()
            self.cell.type = "hamster"
            self.cell.display_image(root.grid_manager.hamster_image)
            self.cell.canvas.hamster_number_text = self.cell.canvas.create_text(
                91, 84,  # x, y position
                text=str(self.cell.hamsters),
                fill="white",
                font=("Arial", 18, "bold")
            )
        else:
            self.cell.clear()















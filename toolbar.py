import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import root



#toolbar als frame erstellen
toolbar_frame = Frame(root, height=68, bg="#333333")


from filetree import save_file, load_file, load_grid, save_grid, new_file, new_grid

new_file_button = Button(toolbar_frame, text ="New File", command = new_file)
new_file_button.pack(side="left")

save_button = Button(toolbar_frame, text ="Save File", command = save_file)
save_button.pack(side="left")

load_button = Button(toolbar_frame, text ="Load File", command = load_file)
load_button.pack(side="left")

new_grid_button = Button(toolbar_frame, text ="New Grid", command = new_grid)
new_grid_button.pack(side="left")

save_grid_button = Button(toolbar_frame, text ="Save Grid", command = save_grid)
save_grid_button.pack(side="left")

load_grid_button = Button(toolbar_frame, text ="Load Grid", command = load_grid)
load_grid_button.pack(side="left")



from code_execution import executeCode
excecute_code_button = Button(toolbar_frame, text ="Excecute Code", command = executeCode)
excecute_code_button.pack(side="left")


from options_handler import get_variable
tick_rate_slider = Scale(toolbar_frame, from_=1, to=100, orient=HORIZONTAL, length=200)
tick_rate_slider.set(get_variable("default_tick_rate"))
tick_rate_slider.pack(side="left")


editing = None

def pick_add_hamster():
    from virtual_environment import grid_man
    global editing 
    editing = "add_hamster"
    grid_man.add_all_clickables()
    

def pick_subtract_hamster():
    from virtual_environment import grid_man
    global editing 
    editing = "subtract_hamster"
    grid_man.add_all_clickables()

def pick_make_wall():
    from virtual_environment import grid_man
    global editing 
    editing = "make_wall"
    grid_man.add_all_clickables()

def clear_cell():
    from virtual_environment import grid_man
    global editing 
    editing = "clear_cell"
    grid_man.add_all_clickables()

def clear_all_cells():
    from virtual_environment import grid_man
    grid_man.clear_all_cells()
    global editing 
    editing = None
    grid_man.delete_all_clickables()

def cancel_editing_grid():
    from virtual_environment import grid_man
    global editing 
    editing = None
    grid_man.delete_all_clickables()

pick_add_hamster_button = Button(toolbar_frame, text ="Add Hamster", command = pick_add_hamster)
pick_add_hamster_button.pack(side="left")

pick_subtract_hamster_button = Button(toolbar_frame, text ="Subtract Hamster", command = pick_subtract_hamster)
pick_subtract_hamster_button.pack(side="left")

pick_make_wall_button = Button(toolbar_frame, text ="Make Wall", command = pick_make_wall)
pick_make_wall_button.pack(side="left")

pick_clear_cell_button = Button(toolbar_frame, text ="Clear Cell", command = clear_cell)
pick_clear_cell_button.pack(side="left")

pick_clear_all_cells_button = Button(toolbar_frame, text ="Clear All Cells", command = clear_all_cells)
pick_clear_all_cells_button.pack(side="left")

cancel_editing_grid_button = Button(toolbar_frame, text ="Cancel Editing Grid", command = cancel_editing_grid)
cancel_editing_grid_button.pack(side="left")
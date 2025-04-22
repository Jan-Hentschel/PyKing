import tkinter as tk
from tkinter import *

from utility import toolbar_button, resource_path
from options_handler import get_variable

from gui import root
from file_management import file_manager
from code_execution import start_execute_code_thread, stop_execute_code_thread
from virtual_environment import grid_man

excecute_code_icon = tk.PhotoImage(file=resource_path('Assets\\excecute_icon.png'))

editing = None

def pick_add_hamster():
    global editing 
    editing = "add_hamster"
    grid_man.add_all_clickables()
    

def pick_subtract_hamster():
    global editing 
    editing = "subtract_hamster"
    grid_man.add_all_clickables()

def pick_make_wall():
    global editing 
    editing = "make_wall"
    grid_man.add_all_clickables()

def clear_cell():
    global editing 
    editing = "clear_cell"
    grid_man.add_all_clickables()

def clear_all_cells():
    grid_man.clear_all_cells()
    global editing 
    editing = None
    grid_man.delete_all_clickables()

def cancel_editing_grid():
    global editing 
    editing = None
    grid_man.delete_all_clickables()

#toolbar als frame erstellen
toolbar_frame = Frame(root, height=68, bg="#333333", pady=5)


new_file_button = toolbar_button(toolbar_frame, text ="New File", command = file_manager.new_file)
new_file_button.pack(side="left")

save_file_as_button = toolbar_button(toolbar_frame, text ="Save File As", command = file_manager.save_file_as)
save_file_as_button.pack(side="left")

save_file_button = toolbar_button(toolbar_frame, text ="Save File", command = file_manager.save_file)
save_file_button.pack(side="left")

load_button = toolbar_button(toolbar_frame, text ="Load File", command = file_manager.load_file)
load_button.pack(side="left")

new_grid_button = toolbar_button(toolbar_frame, text ="New Grid", command = file_manager.new_grid)
new_grid_button.pack(side="left")

save_grid_button = toolbar_button(toolbar_frame, text ="Save Grid", command = file_manager.save_grid)
save_grid_button.pack(side="left")

load_grid_button = toolbar_button(toolbar_frame, text ="Load Grid", command = file_manager.load_grid)
load_grid_button.pack(side="left")

excecute_code_button = Button(toolbar_frame, image=excecute_code_icon, command = start_execute_code_thread, bg="#333333", activebackground="#3F3F3F")
excecute_code_button.pack(side="left")

stop_code_execution_button = toolbar_button(toolbar_frame, text ="Stop Execution", command = stop_execute_code_thread)
stop_code_execution_button.pack(side="left")


tick_rate_slider = Scale(toolbar_frame, from_=1, to=100, orient=HORIZONTAL, length=200, bg="#333333", activebackground="#333333", highlightbackground="#333333",fg="#FFFFFF", troughcolor="#3F3F3F")
tick_rate_slider.set(get_variable("default_tick_rate"))
tick_rate_slider.pack(side="left")


pick_add_hamster_button = toolbar_button(toolbar_frame, text ="Add Hamster", command = pick_add_hamster)
pick_add_hamster_button.pack(side="left")

pick_subtract_hamster_button = toolbar_button(toolbar_frame, text ="Subtract Hamster", command = pick_subtract_hamster)
pick_subtract_hamster_button.pack(side="left")

pick_make_wall_button = toolbar_button(toolbar_frame, text ="Make Wall", command = pick_make_wall)
pick_make_wall_button.pack(side="left")

pick_clear_cell_button = toolbar_button(toolbar_frame, text ="Clear Cell", command = clear_cell)
pick_clear_cell_button.pack(side="left")

pick_clear_all_cells_button = toolbar_button(toolbar_frame, text ="Clear All Cells", command = clear_all_cells)
pick_clear_all_cells_button.pack(side="left")

cancel_editing_grid_button = toolbar_button(toolbar_frame, text ="Cancel Editing Grid", command = cancel_editing_grid)
cancel_editing_grid_button.pack(side="left")


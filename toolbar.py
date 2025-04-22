import tkinter as tk
from tkinter import *

from utility import ToolbarButton, resource_path
from options_handler import get_variable

from gui import root
from file_management import file_manager
from code_execution import start_execute_code_thread, stop_execute_code_thread
from virtual_environment import grid_man

class Toolbar:
    def __init__(self):
        self.editing = None
        self.excecute_code_icon = tk.PhotoImage(file=resource_path('Assets\\excecute_icon.png'))

        self.frame = Frame(root, height=68, bg="#333333", pady=5)


        self.new_file_button = ToolbarButton(self.frame, text ="New File", command = file_manager.new_file)
        self.new_file_button.pack(side="left")

        self.save_file_as_button = ToolbarButton(self.frame, text ="Save File As", command = file_manager.save_file_as)
        self.save_file_as_button.pack(side="left")

        self.save_file_button = ToolbarButton(self.frame, text ="Save File", command = file_manager.save_file)
        self.save_file_button.pack(side="left")

        self.load_button = ToolbarButton(self.frame, text ="Load File", command = file_manager.load_file)
        self.load_button.pack(side="left")

        self.new_grid_button = ToolbarButton(self.frame, text ="New Grid", command = file_manager.new_grid)
        self.new_grid_button.pack(side="left")

        self.save_grid_button = ToolbarButton(self.frame, text ="Save Grid", command = file_manager.save_grid)
        self.save_grid_button.pack(side="left")

        self.load_grid_button = ToolbarButton(self.frame, text ="Load Grid", command = file_manager.load_grid)
        self.load_grid_button.pack(side="left")

        self.excecute_code_button = Button(self.frame, image=self.excecute_code_icon, command = start_execute_code_thread, bg="#333333", activebackground="#3F3F3F")
        self.excecute_code_button.pack(side="left")

        self.stop_code_execution_button = ToolbarButton(self.frame, text ="Stop Execution", command = stop_execute_code_thread)
        self.stop_code_execution_button.pack(side="left")


        self.tick_rate_slider = Scale(self.frame, from_=1, to=100, orient=HORIZONTAL, length=200, bg="#333333", activebackground="#333333", highlightbackground="#333333",fg="#FFFFFF", troughcolor="#3F3F3F")
        self.tick_rate_slider.set(get_variable("default_tick_rate"))
        self.tick_rate_slider.pack(side="left")


        self.pick_add_hamster_button = ToolbarButton(self.frame, text ="Add Hamster", command = self.pick_add_hamster)
        self.pick_add_hamster_button.pack(side="left")

        self.pick_subtract_hamster_button = ToolbarButton(self.frame, text ="Subtract Hamster", command = self.pick_subtract_hamster)
        self.pick_subtract_hamster_button.pack(side="left")

        self.pick_make_wall_button = ToolbarButton(self.frame, text ="Make Wall", command = self.pick_make_wall)
        self.pick_make_wall_button.pack(side="left")

        self.pick_clear_cell_button = ToolbarButton(self.frame, text ="Clear Cell", command = self.clear_cell)
        self.pick_clear_cell_button.pack(side="left")

        self.pick_clear_all_cells_button = ToolbarButton(self.frame, text ="Clear All Cells", command = self.clear_all_cells)
        self.pick_clear_all_cells_button.pack(side="left")

        self.cancel_editing_grid_button = ToolbarButton(self.frame, text ="Cancel Editing Grid", command = self.cancel_editing_grid)
        self.cancel_editing_grid_button.pack(side="left")



    def pick_add_hamster(self):
        global editing 
        editing = "add_hamster"
        grid_man.add_all_clickables()
        

    def pick_subtract_hamster(self):
        global editing 
        editing = "subtract_hamster"
        grid_man.add_all_clickables()

    def pick_make_wall(self):
        global editing 
        editing = "make_wall"
        grid_man.add_all_clickables()

    def clear_cell(self):
        global editing 
        editing = "clear_cell"
        grid_man.add_all_clickables()

    def clear_all_cells(self):
        grid_man.clear_all_cells()
        global editing 
        editing = None
        grid_man.delete_all_clickables()

    def cancel_editing_grid(self):
        global editing 
        editing = None
        grid_man.delete_all_clickables()

toolbar = Toolbar()
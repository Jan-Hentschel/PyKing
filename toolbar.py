import tkinter as tk
from tkinter import *

from utility import *
from settings_handler import settings_handler


class Toolbar:
    def __init__(self, root):
        
        self.excecute_code_icon = tk.PhotoImage(file=resource_path('Assets\\excecute_icon.png'))
        self.linked_false_image = tk.PhotoImage(file=resource_path('Assets\\linked_false_image.png'))
        self.linked_true_image = tk.PhotoImage(file=resource_path('Assets\\linked_true_image.png'))

        self.frame = Frame(root, height=68, bg=root.secondary_color, pady=5)


        self.new_file_button = DefaultButton(self.frame, text ="New File", command = root.file_manager.new_python_file)
        self.save_file_as_button = DefaultButton(self.frame, text ="Save File As", command = root.file_manager.save_python_file_as)
        self.save_file_button = DefaultButton(self.frame, text ="Save File", command = root.file_manager.save_python_file)
        self.load_button = DefaultButton(self.frame, text ="Load File", command = root.file_manager.open_python_file_dialog)
        self.new_grid_button = DefaultButton(self.frame, text ="New Grid", command = root.file_manager.new_grid)
        self.save_grid_as_button = DefaultButton(self.frame, text ="Save Grid As", command = root.file_manager.save_grid_as)
        self.save_grid_button = DefaultButton(self.frame, text ="Save Grid", command = root.file_manager.save_grid)
        self.load_grid_button = DefaultButton(self.frame, text ="Load Grid", command = root.file_manager.open_grid_dialog)
        self.excecute_code_button = DefaultButton(self.frame, image=self.excecute_code_icon, command = root.code_executor.start_execute_code_thread)
        self.stop_code_execution_button = DefaultButton(self.frame, text ="Stop Execution", command = root.code_executor.stop_execute_code_thread)
        self.tick_rate_slider = Scale(self.frame, from_=1, to=100, orient=HORIZONTAL, length=200, bg=root.secondary_color, activebackground=root.secondary_color, highlightbackground=root.secondary_color, fg=root.foreground_color, troughcolor=root.primary_color)
        self.tick_rate_slider.set(settings_handler.get_variable("default_tick_rate"))
        self.tick_rate_slider.pack(side="left")
        self.pick_add_hamster_button = DefaultButton(self.frame, text ="Add Hamster", command = root.grid_manager.pick_add_hamster)
        self.pick_subtract_hamster_button = DefaultButton(self.frame, text ="Subtract Hamster", command = root.grid_manager.pick_subtract_hamster)
        self.pick_make_wall_button = DefaultButton(self.frame, text ="Make Wall", command = root.grid_manager.pick_make_wall)
        self.pick_clear_cell_button = DefaultButton(self.frame, text ="Clear Cell", command = root.grid_manager.clear_cell)
        self.pick_clear_all_cells_button = DefaultButton(self.frame, text ="Clear All Cells", command = root.grid_manager.edit_clear_all_cells)
        self.cancel_editing_grid_button = DefaultButton(self.frame, text ="Cancel Editing Grid", command = root.grid_manager.cancel_editing_grid)
        self.link_grid_to_python_file = DefaultButton(self.frame, text ="Link Grid To Python File", command = root.file_manager.link_grid_to_python_file)
        self.is_linked = DefaultLabel(self.frame, text="Linked", image=self.linked_false_image, compound="left")
        self.is_linked.pack(side="left")
        self.settings_button = DefaultButton(self.frame, text ="Settings", command = root.settings.open_settings)
        self.settings_button.pack(side="right")

    def update_linked_status(self, linked):
        if linked:
            self.is_linked.configure(image=self.linked_true_image)
        else:
            self.is_linked.configure(image=self.linked_false_image)
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

        self.filemenu_button = DefaultButton(self.frame, text="File", command=lambda: self.open_filemenu(), padx=50)
        self.filemenu = Menu(self.frame, tearoff=0)
        self.filemenu.add_command(label="New", command=root.file_manager.new_python_file)
        self.filemenu.add_command(label="Save as", command=root.file_manager.save_python_file_as)
        self.filemenu.add_command(label="Save", command=root.file_manager.save_python_file)
        self.filemenu.add_command(label="Open", command=root.file_manager.open_python_file_dialog)
        

        self.gridmenu_button = DefaultButton(self.frame, text="Grid", command=lambda: self.open_gridmenu(), padx=50)
        self.gridmenu = Menu(self.frame, tearoff=0)
        self.gridmenu.add_command(label="New", command=root.file_manager.new_grid)
        self.gridmenu.add_command(label="Save as", command=root.file_manager.save_grid_as)
        self.gridmenu.add_command(label="Save", command=root.file_manager.save_grid)
        self.gridmenu.add_command(label="Open", command=root.file_manager.open_grid_dialog)
        


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

    def open_filemenu(self):
        x = self.filemenu_button.winfo_rootx()
        y = self.filemenu_button.winfo_rooty() + self.filemenu_button.winfo_height()
        self.filemenu.post(x, y)


    def open_gridmenu(self):
        x = self.gridmenu_button.winfo_rootx()
        y = self.gridmenu_button.winfo_rooty() + self.gridmenu_button.winfo_height()
        print(x, y)
        self.gridmenu.post(x, y)
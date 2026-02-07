from logging import root
import webbrowser

from utility import * 
from settings_handler import settings_handler
from gui import Root


class Toolbar:
    def __init__(self, root: Root):
        self.root: Root = root
        self.excecute_code_icon: PhotoImage = PhotoImage(file=resource_path('Assets\\excecute_icon.png'))
        self.stop_excecute_code_icon: PhotoImage = PhotoImage(file=resource_path('Assets\\stop_execute_icon.png'))
        self.linked_false_image: PhotoImage = PhotoImage(file=resource_path('Assets\\linked_false_image.png'))
        self.linked_true_image: PhotoImage = PhotoImage(file=resource_path('Assets\\linked_true_image.png'))
        self.pause_image: PhotoImage = PhotoImage(file=resource_path('Assets\\pause.png'))
        self.resume_image: PhotoImage = PhotoImage(file=resource_path('Assets\\play.png'))
        self.step_image: PhotoImage = PhotoImage(file=resource_path('Assets\\priority-arrow.png'))
        self.add_hamster_image: PhotoImage = PhotoImage(file=resource_path('Assets\\add_hamster.png'))
        self.subtract_hamster_image: PhotoImage = PhotoImage(file=resource_path('Assets\\subtract_hamster.png'))
        self.make_wall_image: PhotoImage = PhotoImage(file=resource_path('Assets\\block-brick.png'))
        self.clear_cell_image: PhotoImage = PhotoImage(file=resource_path('Assets\\cross-small.png'))
        self.clear_all_cells_image: PhotoImage = PhotoImage(file=resource_path('Assets\\trash.png'))
        self.cancel_editing_grid_image: PhotoImage = PhotoImage(file=resource_path('Assets\\ban.png'))
        self.link_grid_to_python_file_image: PhotoImage = PhotoImage(file=resource_path('Assets\\link.png'))
        self.settings_image: PhotoImage = PhotoImage(file=resource_path('Assets\\settings.png'))
        self.github_image: PhotoImage = PhotoImage(file=resource_path('Assets\\github.png'))
        self.lock_image: PhotoImage = PhotoImage(file=resource_path('Assets\\lock.png'))
        self.unlock_image: PhotoImage = PhotoImage(file=resource_path('Assets\\unlock.png'))




        self.frame = DefaultSecondaryFrame(root, height=68, pady=5)
        
        self.filemenu_button = DefaultMenuButton(self.frame, text="File", command=lambda: self.open_filemenu(), padx=50)
        self.filemenu = DefaultMenu(self.frame, tearoff=0)

        self.filemenu.add_command(label="New", command=root.file_manager.new_python_file)
        self.filemenu.add_command(label="Save as", command=root.file_manager.save_python_file_as)
        self.filemenu.add_command(label="Save", command=root.file_manager.save_python_file)
        self.filemenu.add_command(label="Open", command=root.file_manager.open_python_file_dialog)
        
        self.gridmenu_button = DefaultMenuButton(self.frame, text="Grid", command=lambda: self.open_gridmenu(), padx=50)
        self.gridmenu = DefaultMenu(self.frame, tearoff=0)
        self.gridmenu.add_command(label="New", command=root.file_manager.new_grid)
        self.gridmenu.add_command(label="Save as", command=root.file_manager.save_grid_as)
        self.gridmenu.add_command(label="Save", command=root.file_manager.save_grid)
        self.gridmenu.add_command(label="Open", command=root.file_manager.open_grid_dialog)
        
        self.excecute_code_button = DefaultButton(self.frame, image=self.excecute_code_icon, command = root.code_executor.start_execute_code_thread)
        self.stop_code_execution_button = DefaultButton(self.frame, image=self.stop_excecute_code_icon, command = root.code_executor.stop_execute_code_thread)
        self.pause_btn = DefaultButton(self.frame, text="Pause", image=self.pause_image, command=root.code_executor.pause_debugger)
        self.resume_btn = DefaultButton(self.frame, text="Resume", image=self.resume_image, command=root.code_executor.resume_debugger)
        self.step_btn   = DefaultButton(self.frame, text="Step",   image=self.step_image, command=root.code_executor.step_debugger)
        self.tick_rate_slider = DefaultScale(self.frame)
        self.tick_rate_slider.set(settings_handler.get_variable("default_tick_rate")) #type: ignore
        self.tick_rate_slider.pack(side="left")
        self.pick_add_hamster_button = DefaultButton(self.frame, text ="Add Hamster", image=self.add_hamster_image, command = root.grid_manager.pick_add_hamster)
        self.pick_subtract_hamster_button = DefaultButton(self.frame, text ="Subtract Hamster", image=self.subtract_hamster_image, command = root.grid_manager.pick_subtract_hamster)
        self.pick_make_wall_button = DefaultButton(self.frame, text ="Make Wall", image=self.make_wall_image, command = root.grid_manager.pick_make_wall)
        self.pick_clear_cell_button = DefaultButton(self.frame, text ="Clear Cell", image=self.clear_cell_image,command = root.grid_manager.clear_cell)
        self.pick_clear_all_cells_button = DefaultButton(self.frame, text ="Clear All Cells", image=self.clear_all_cells_image,command = root.grid_manager.edit_clear_all_cells)
        self.cancel_editing_grid_button = DefaultButton(self.frame, text ="Cancel Editing Grid", image=self.cancel_editing_grid_image,command = root.grid_manager.cancel_editing_grid)
        self.link_grid_to_python_file = DefaultButton(self.frame, text ="Link Grid To Python File", image=self.link_grid_to_python_file_image, command = root.file_manager.link_grid_to_python_file)
        self.lock_grid_button = DefaultButton(self.frame, text="Lock Grid", image=self.lock_image, command=root.file_manager.lock_button)
        self.is_linked = DefaultLabel(self.frame, text="Linked", image=self.linked_false_image, compound="left")
        self.is_linked.pack(side="left")
        self.is_locked = DefaultLabel(self.frame, text="Unlocked", image=self.unlock_image, compound="left")
        self.is_locked.pack(side="left")

        self.settings_button = DefaultButton(self.frame, text ="Settings", image=self.settings_image, command = self.open_settings)
        self.settings_button.pack(side="right")
        self.help_button = DefaultButton(self.frame, text="GitHub", image=self.github_image, command=self.show_github)
        self.help_button.pack(side="right")

    def open_settings(self):
        if not(self.root.settings.exists):
            self.root.settings.open_settings()


    def update_linked_status(self, linked: bool):
        if linked:
            self.is_linked.configure(image=self.linked_true_image)
        else:
            self.is_linked.configure(image=self.linked_false_image)


    def open_filemenu(self):
        x: int = self.filemenu_button.winfo_rootx()
        y: int = self.filemenu_button.winfo_rooty() + self.filemenu_button.winfo_height()
        self.filemenu.post(x, y)


    def open_gridmenu(self):
        x: int = self.gridmenu_button.winfo_rootx()
        y: int = self.gridmenu_button.winfo_rooty() + self.gridmenu_button.winfo_height()
        self.gridmenu.post(x, y)


    def show_github(self):
        webbrowser.open('https://github.com/Jan-Hentschel/PyKing')  # Go to example.com
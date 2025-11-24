from tkinter import filedialog
import json

from utility import * # type: ignore 
from settings_handler import settings_handler
from gui import Root


class FileManager:
    def __init__(self, root: Root):
        self.root: Root = root
        

    def save_text_widget_content_to_directory(self, directory):
        with open(directory, "w", encoding="utf-8") as file:
            file.write(self.root.code_editor.get_text_widget_content())

    def read_file(self, directory):
        with open(directory, "r", encoding="utf-8") as file:
            content = file.read()
            if content.endswith('\n'):
                content = content[:-1]  # remove exactly one trailing newline
            return content
    
    def create_grid(self, popup):
        columns = popup.column_entry.get()
        rows = popup.row_entry.get()
        popup.destroy()
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        if directory:
            self.root.grid_manager.change_grid_man(int(columns), int(rows))
            grid_dictionary = self.root.grid_manager.get_grid_dict()
            grid_dictionary = json.loads(grid_dictionary)
            grid_dictionary["link"] = ""
            with open(directory, "w", encoding="utf-8") as file:
                file.write(json.dumps(grid_dictionary, indent=4))
            settings_handler.set_variable("current_grid_directory", directory)
            self.root.terminal.show_current_directories(f"created new grid as: {directory}")
            self.root.filetree.refresh_treeview()
            self.root.toolbar.update_linked_status(False)
        
    
    def link_grid_to_python_file(self):
        
        grid_directory: str = settings_handler.get_variable("current_grid_directory")
        python_directory: str = settings_handler.get_variable("current_file_directory")
        try:
            with open(grid_directory, "r", encoding="utf-8") as file:
                content = file.read()
                dict = json.loads(content)
                dict["link"] = python_directory
            with open(grid_directory, "w", encoding="utf-8") as file:
                file.write(json.dumps(dict, indent=4))
            self.root.terminal.show_current_directories(f"linked grid: {grid_directory}\nto python file: {python_directory}")
            self.root.toolbar.update_linked_status(True)
        except FileNotFoundError:
            self.root.terminal.show_current_directories(f"failed to link grid: {grid_directory} to python file: {python_directory}\n\n")


    def open_file(self, directory: str, check_if_linked: bool=True, label_opened: bool=False):
        directory = directory.replace("\\", "/")
        self.root.code_editor.load_into_editor(self.read_file(directory))
        settings_handler.set_variable("current_file_directory", directory)
        if not label_opened:
            self.root.code_editor.add_label(directory)
            
        if not check_if_linked:
            return
        
        all_grid_file_paths = self.root.filetree.all_grid_file_paths()
        for grid_path in all_grid_file_paths:
            if self.has_valid_link(grid_path):
                with open(grid_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    dict = json.loads(content)
                    link = dict["link"].replace("\\", "/")
                    if link == directory:
                        self.open_grid(grid_path, False)
                        self.root.terminal.show_current_directories(f"loaded python file: {link}\nloaded grid: {grid_path}\n\npython file was linked to grid")
                        return
        self.root.toolbar.update_linked_status(False)
        self.root.terminal.show_current_directories(f"loaded python file: {directory}")
        

    def open_python_file_dialog(self):
        #ask to save before
        directory = filedialog.askopenfilename(initialdir=path_from_relative_path("Files"), title="Open a file", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        if directory:
            self.open_file(directory)

    def save_python_file_as(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        if directory:
            self.save_text_widget_content_to_directory(directory)
            settings_handler.set_variable("current_file_directory", directory)
            self.root.terminal.show_current_directories(f"saved python file as: {directory}")

    def save_python_file(self):
        try:
            self.save_text_widget_content_to_directory(settings_handler.get_variable("current_file_directory"))
            self.root.terminal.show_current_directories(f"saved python file: {settings_handler.get_variable('current_file_directory')}")
        except FileNotFoundError:
            self.save_python_file_as()

            
    def new_python_file(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="New File", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        if directory:
            with open(directory, "w", encoding="utf-8") as file:
                file.write("")    
            settings_handler.set_variable("current_file_directory", directory)
            self.root.terminal.show_current_directories(f"created new python file as: {directory}")
            self.open_file(directory)
            
            self.root.filetree.refresh_treeview()
                


    def has_valid_link(self, directory: str) -> bool:
        with open(directory, "r", encoding="utf-8") as file:
            content = file.read()
            dict = json.loads(content)
            link = None
            try:
                link = dict["link"]        
                if os.path.isfile(link) and link[-3:] == ".py":
                    return True 
                else:
                    return False
            except KeyError:
                return False

                
        

    def open_grid(self, directory: str, check_if_linked: bool=True, label_opened: bool=False):
        directory = directory.replace("\\", "/")
        with open(directory, "r", encoding="utf-8") as file:
            content: str = file.read()

        grid_dictionary = json.loads(content)

        columns: int = grid_dictionary["columns"]
        rows: int = grid_dictionary["rows"]
        new_cells: list[str] = grid_dictionary["cells"]
        link: str = grid_dictionary["link"].replace("\\", "/")

        self.root.grid_manager.change_grid(columns, rows, new_cells, link)
        settings_handler.set_variable("current_grid_directory", directory)

        if not label_opened:
            self.root.grid_manager.add_label(directory)

        if self.has_valid_link(directory) and check_if_linked:
            self.open_file(grid_dictionary["link"], check_if_linked=False)
            settings_handler.set_variable("current_file_directory", link)
            self.root.terminal.show_current_directories(f"loaded python file: {link}\nloaded grid: {directory}\n\npython file was linked to grid")

        elif check_if_linked:
            if link:
                self.root.terminal.show_current_directories(f"loaded grid: {directory}\nfailed to load linked python file: {link}\n\nlinked python file does not exist maybe check if the path is correct")
            else:
                self.root.terminal.show_current_directories(f"loaded grid: {directory}")

        if self.has_valid_link(directory) and link==settings_handler.get_variable("current_file_directory"):
            self.root.toolbar.update_linked_status(True)
        else:
            self.root.toolbar.update_linked_status(False)


    def open_grid_dialog(self):
        #ask to save before
        directory = filedialog.askopenfilename(initialdir=path_from_relative_path("Files"), title="Open a file", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        if directory:
            self.open_grid(directory)
        
    def save_grid_as(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        if directory:
            json_dict = self.root.grid_manager.get_grid_dict()
            with open(directory, "w", encoding="utf-8") as file:
                file.write(json_dict)
            settings_handler.set_variable("current_grid_directory", directory)
            self.root.terminal.show_current_directories(f"saved grid as: {directory}")

    def save_grid(self):
        try:
            directory = settings_handler.get_variable("current_grid_directory")
            json_dict = self.root.grid_manager.get_grid_dict()
            with open(directory, "w", encoding="utf-8") as file:
                file.write(json_dict)
            self.root.terminal.show_current_directories(f"saved grid: {settings_handler.get_variable('current_grid_directory')}")
        except FileNotFoundError:
            self.save_grid_as()


    def new_grid(self):
        popup = GridSizeSelectionPopup(self.root, self)

    def save_python_file_and_grid(self):
        self.save_python_file()
        self.save_grid()
        self.root.terminal.show_current_directories(f"saved python file: {settings_handler.get_variable('current_file_directory')}\nsaved grid: {settings_handler.get_variable('current_grid_directory')}")
        
    def open_python_file_and_grid_from_options(self):
        try:
            self.open_file(settings_handler.get_variable("current_file_directory"))
        except FileNotFoundError:
            pass
        try:
            self.open_grid(settings_handler.get_variable("current_grid_directory"))
        except FileNotFoundError:
            pass
        self.root.terminal.show_current_directories(f"loaded python file: {settings_handler.get_variable('current_file_directory')}\nloaded grid: {settings_handler.get_variable('current_grid_directory')}")

class GridSizeSelectionPopup(Toplevel):
    def __init__(self, root: Root, file_manager: FileManager):
        super().__init__(root)
        self.geometry("400x200")
        self.title("Input Grid Height and Width")
        self.iconbitmap(resource_path("Assets\\Icon.ico"))

        column_label = DefaultLabel(self, text="Columns:")
        self.column_entry = DefaultEntry(self)

        row_label = DefaultLabel(self, text="Rows:")
        self.row_entry = DefaultEntry(self)
        
        ok_button = DefaultButton(self, text="OK", command=lambda: file_manager.create_grid(self))
        ok_button.pack(side="left")

        cancel_button = DefaultButton(self, text="Cancel", command= lambda: self.destroy())
        cancel_button.pack(side="right")
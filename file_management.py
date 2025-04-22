from tkinter import *
from tkinter import filedialog
from utility import ToolbarButton
import json

from utility import path_from_relative_path
from options_handler import options_handler




from gui import root

class FileManager:
    def __init__(self, root):
        self.root = root
        

    def save_text_widget_content_to_directory(self, directory):
        with open(directory, "w", encoding="utf-8") as file:
            file.write(self.rootcode_editor.get_text_widget_content())

    def read_file(self, directory):
        with open(directory, "r", encoding="utf-8") as file:
            return file.read()
    
    def create_grid(self, popup):
                columns = popup.column_entry.get()
                rows = popup.row_entry.get()
                root.grid_man.change_grid_man(int(columns), int(rows))
                popup.destroy()
                directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
                json_dict = json.dumps(root.grid_man.get_grid_dict())
                with open(directory, "w", encoding="utf-8") as file:
                    file.write(json_dict)
                options_handler.set_variable("current_grid_directory", directory)
                self.root.terminal.show_current_directories(f"created new grid as: {directory}")



    def open_file(self, directory):
        self.root.code_editor.load_into_editor(self.read_file(directory))
        options_handler.set_variable("current_file_directory", directory)
        self.root.terminal.show_current_directories(f"loaded python file: {directory}")

    def open_python_file_dialog(self):
        #ask to save before
        directory = filedialog.askopenfilename(initialdir=path_from_relative_path("Files"), title="Open a file", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        self.open_file(directory)

    def save_python_file_as(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        self.save_text_widget_content_to_directory(directory)
        options_handler.set_variable("current_file_directory", directory)
        self.root.terminal.show_current_directories(f"saved python file as: {directory}")

    def save_python_file(self):
        self.save_text_widget_content_to_directory(options_handler.get_variable("current_file_directory"))
        self.root.terminal.show_current_directories(f"saved python file: {options_handler.get_variable('current_file_directory')}")
    
    def new_python_file(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="New File", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        with open(directory, "w", encoding="utf-8") as file:
            file.write("")    
        options_handler.set_variable("current_file_directory", directory)
        self.root.terminal.show_current_directories(f"created new python file as: {directory}")
              

    def open_grid(self, directory):
        with open(directory, "r", encoding="utf-8") as file:
            content = file.read()
            dict = json.loads(content)
            columns = dict["columns"]
            rows = dict["rows"]
            new_cells = dict["cells"]
            root.grid_man.change_grid(columns, rows, new_cells)
        options_handler.set_variable("current_grid_directory", directory)
        self.root.terminal.show_current_directories(f"loaded grid: {directory}")

    def open_grid_dialog(self):
        #ask to save before
        directory = filedialog.askopenfilename(initialdir=path_from_relative_path("Files"), title="Open a file", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        self.open_grid(directory)
        
    def save_grid_as(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        json_dict = json.dumps(root.grid_man.get_grid_dict())
        with open(directory, "w", encoding="utf-8") as file:
            file.write(json_dict)
        options_handler.set_variable("current_grid_directory", directory)
        self.root.terminal.show_current_directories(f"saved grid as: {directory}")

    def save_grid(self):
        directory = options_handler.get_variable("current_grid_directory")
        json_dict = json.dumps(root.grid_man.get_grid_dict())
        with open(directory, "w", encoding="utf-8") as file:
            file.write(json_dict)
        self.root.terminal.show_current_directories(f"saved grid: {options_handler.get_variable('current_grid_directory')}")

    def new_grid(self):


        popup = Toplevel(self.root)
        popup.geometry("400x200")
        popup.title("Input Grid Height and Width")

        column_label = Label(popup, text="Columns:")
        column_label.pack()
        popup.column_entry = Entry(popup)
        popup.column_entry.pack()

        row_label = Label(popup, text="Rows:")
        row_label.pack()
        popup.row_entry = Entry(popup)
        popup.row_entry.pack()
        
        ok_button = ToolbarButton(popup, text="OK", command=lambda: self.create_grid(popup))
        ok_button.pack(side="left")

        cancel_button = ToolbarButton(popup, text="Cancel", command= lambda: popup.destroy())
        cancel_button.pack(side="right")
   

    def save_python_file_and_grid(self):
        self.save_python_file()
        self.save_grid()
        self.root.terminal.show_current_directories(f"saved python file: {options_handler.get_variable('current_file_directory')}\nsaved grid: {options_handler.get_variable('current_grid_directory')}")
        
    def open_python_file_and_grid_from_options(self):
        try:
            self.open_file(options_handler.get_variable("current_file_directory"))
            self.open_grid(options_handler.get_variable("current_grid_directory"))
        except Exception as error:
            print(error)
        self.root.terminal.show_current_directories(f"loaded python file: {options_handler.get_variable('current_file_directory')}\nloaded grid: {options_handler.get_variable('current_grid_directory')}")


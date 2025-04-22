from tkinter import *
from tkinter import filedialog
from utility import ToolbarButton
import json

from utility import path_from_relative_path
from options_handler import options_handler

from gui import root
from code_editor import code_editor
from terminal import terminal
from virtual_environment import grid_man

class FileManager:
    def __init__(self):
        pass

    def save_content_to_directory(self, directory):
        with open(directory, "w", encoding="utf-8") as file:
            file.write(code_editor.getStringFromEditor())


    def get_content_from_directory(self, directory):
        with open(directory, "r", encoding="utf-8") as file:
            return file.read()

    def load_file_directory(self, directory):
        code_editor.load_into_editor(self.get_content_from_directory(directory))
        options_handler.set_variable("current_file_directory", directory)
        terminal.show_current_directories()


    def load_file(self):
        #ask to save before
        directory = filedialog.askopenfilename(initialdir=path_from_relative_path("Files"), title="Open a file", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        self.load_file_directory(directory)



    def save_file_as(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        self.save_content_to_directory(directory)
        options_handler.set_variable("current_file_directory", directory)
        terminal.show_current_directories()

    def save_file(self, event = ""):
        self.save_content_to_directory(options_handler.get_variable("current_file_directory"))



    def load_grid_directory(self, directory):
        with open(directory, "r", encoding="utf-8") as file:
            content = file.read()
            dict = json.loads(content)
            columns = dict["columns"]
            rows = dict["rows"]
            new_cells = dict["cells"]
            grid_man.change_grid(columns, rows, new_cells)
        options_handler.set_variable("current_grid_directory", directory)
        terminal.show_current_directories()

    def load_grid(self):
        #ask to save before
        directory = filedialog.askopenfilename(initialdir=path_from_relative_path("Files"), title="Open a file", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        self.load_grid_directory(directory)
    

    def save_grid(self):
        
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        json_dict = json.dumps(grid_man.get_grid_dict())
        with open(directory, "w", encoding="utf-8") as file:
            file.write(json_dict)
        options_handler.set_variable("current_grid_directory", directory)
        terminal.show_current_directories()

        
    def new_file(self):
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="New File", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
        with open(directory, "w", encoding="utf-8") as file:
            file.write("")    
        options_handler.set_variable("current_file_directory", directory)
        terminal.show_current_directories()
        

        
    def create_grid(self, popup):
        
        columns = popup.column_entry.get()
        rows = popup.row_entry.get()
        grid_man.change_grid_man(int(columns), int(rows))
        popup.destroy()
        directory = filedialog.asksaveasfilename(initialdir=path_from_relative_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
        json_dict = json.dumps(grid_man.get_grid_dict())
        with open(directory, "w", encoding="utf-8") as file:
            file.write(json_dict)
        options_handler.set_variable("current_grid_directory", directory)
        terminal.show_current_directories()



    def new_grid(self):

        popup = Toplevel(root)
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

file_manager = FileManager()
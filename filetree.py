import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys
from tkinter import filedialog
from tkinter import simpledialog

import json

import gui
from code_editor import loadIntoEditor, getStringFromEditor

# Frame für den Filetree erstellen (links)
file_tree_widget = Frame(gui.horizontally_paned_window, bg="#333333")



def resource_path(relative_path):

    base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




test_file_path = resource_path("Files\\testfile.py")

def save_content_to_directory(directory):
    with open(directory, "w", encoding="utf-8") as file:
        file.write(getStringFromEditor())


def get_content_from_directory(directory):
    with open(directory, "r", encoding="utf-8") as file:
        return file.read()

def load_directory(directory):
    loadIntoEditor(get_content_from_directory(directory))

from virtual_environment import throw_error_to_terminal
def load_test_file():
    throw_error_to_terminal(test_file_path)
    try:
        load_directory(test_file_path)
    except:
        throw_error_to_terminal(Exception)

def save_test_file():
    throw_error_to_terminal(test_file_path)
    try:
        save_content_to_directory(test_file_path)
    except:
        throw_error_to_terminal(Exception)

def load_file():
    directory = filedialog.askopenfilename(initialdir=resource_path("Files"), title="Open a file", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    load_directory(directory)

def save_file():
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="Save as", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    save_content_to_directory(directory)



from virtual_environment import change_grid, get_grid_dict, change_grid_man

def load_grid():
    directory = filedialog.askopenfilename(initialdir=resource_path("Files"), title="Open a file", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
    with open(directory, "r", encoding="utf-8") as file:
        content = file.read()
        dict = json.loads(content)
        columns = dict["columns"]
        rows = dict["rows"]
        new_cells = dict["cells"]
        change_grid(columns, rows, new_cells)

def save_grid():
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
    json_dict = json.dumps(get_grid_dict())
    with open(directory, "w", encoding="utf-8") as file:
        file.write(json_dict)

    
def new_file():
    file = filedialog.asksaveasfile(initialdir=resource_path("Files"), title="New File", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    file.close()
    

    
def create_grid(popup):
    columns = popup.column_entry.get()
    rows = popup.row_entry.get()
    change_grid_man(int(columns), int(rows))
    popup.destroy()



def new_grid():
    from gui import root
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
    
    ok_button = Button(popup, text="OK", command=lambda: create_grid(popup))
    ok_button.pack(side="left")

    cancel_button = Button(popup, text="Cancel", command= lambda: popup.destroy())
    cancel_button.pack(side="right")
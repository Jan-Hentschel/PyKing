import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys
from tkinter import filedialog

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

def save_test_grid():
    pass
def load_test_grid():
    pass
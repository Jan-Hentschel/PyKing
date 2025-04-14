import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys


import gui
from code_editor import loadIntoEditor, getStringFromEditor

# Frame für den Filetree erstellen (links)
file_tree_widget = Frame(gui.horizontally_paned_window, bg="#333333")



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




test_file_path = resource_path("dist\\Files\\file.py")

def save_content_to_directory(directory):
    with open(directory, "w", encoding="utf-8") as file:
        file.write(getStringFromEditor())


def get_content_from_directory(directory):
    with open(directory, "r", encoding="utf-8") as file:
        return file.read()

def load_directory(directory):
    loadIntoEditor(get_content_from_directory(directory))

def load_test_file():
    load_directory(test_file_path)

def save_test_file():
    save_content_to_directory(test_file_path)
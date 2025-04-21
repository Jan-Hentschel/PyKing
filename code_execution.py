import tkinter as tk
from gui import root
from tkinter import *
from code_editor import code_editor_widget
from terminal import terminal_widget
from virtual_environment import Snake, grid_man
import threading

#help from chatgpt to get everything working
def print_to_terminal_widget(*args):
    output = " ".join(map(str, args)) + "\n"
    terminal_widget.insert(tk.END, output)


PyKing_functions = {
    "print": print_to_terminal_widget,
    "Snake": Snake
}

from filetree import load_grid_directory
from options_handler import get_variable
def execute_code():
    try:
        load_grid_directory(get_variable("current_grid_directory")) #ask to save before
        root.update_idletasks()
        code = code_editor_widget.get("1.0", END)
        exec(code, PyKing_functions)
        #runMovie()
    except Exception as error:
        print_to_terminal_widget(error)

def start_execute_code_thread():
    threading.Thread(target=execute_code).start()
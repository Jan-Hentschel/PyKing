import tkinter as tk
from gui import root
from tkinter import *
from code_editor import code_editor_widget
from terminal import terminal_widget

#chatgpt
def print_to_terminal_widget(*args):
    output = " ".join(map(str, args))
    terminal_widget.insert(tk.END, output)


PyKing_functions = {
    "print": print_to_terminal_widget
}
def executeCode(event):
    try:
        terminal_widget.delete('1.0', END)
        root.update_idletasks()
        code = code_editor_widget.get("1.0", END)
        exec(code, PyKing_functions)
    except Exception as error:
        print_to_terminal_widget(error)

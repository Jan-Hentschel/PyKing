import tkinter as tk
from tkinter import *
import threading
import code
import traceback
import sys
import io
import bdb
import time
import linecache

from settings_handler import settings_handler

from virtual_environment import Snake


#help from chatgpt to get everything working
def print_to_terminal_widget(*args):
    from gui import root
    output = " ".join(map(str, args))
    root.terminal.print(output)



#https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
class StoppableThread(threading.Thread):
    
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Debugger(bdb.Bdb):
    def __init__(self, tickrate=1.0):
        super().__init__()
        self.tickrate = tickrate

    def user_line(self, frame):
        lineno = frame.f_lineno
        filename = frame.f_code.co_filename
        line = linecache.getline(filename, lineno).strip()
        print(f"\n▶ Line {lineno}: {line}")
        print(f"📦 Locals: {frame.f_locals}")
        self.set_step()  # Wait for the next step (you could also pause here)

    def run_file(self, filename, custom_globals):
        # Inject our globals into the run context
        with open(filename) as file:
            code = file.read()
            self.run(code, custom_globals)



class CodeExecution:
    def __init__(self, root):
        self.root = root
        self.execute_code_thread = None


    def execute_code(self):
        PyKing_globals = {
            "Snake": Snake,
            "__builtins__": dict(__builtins__),  # clone builtins
            "__name__": "__main__"
        }
        PyKing_globals["__builtins__"]["print"] = print_to_terminal_widget

        cursor_position = self.root.code_editor.frame.text_widget.index("insert")
        self.root.file_manager.open_grid(settings_handler.get_variable("current_grid_directory"))
        self.root.code_editor.frame.text_widget.mark_set("insert", cursor_position)
        self.root.update_idletasks()
        # Your setup


        # Use this where you previously had execute_code()
        debugger = Debugger(tickrate=1.0)
        try:
            debugger.run_file("C:/Users/jmast/OneDrive/Seminararbeit/Seminararbeits Projekt/PyKing/Files/Hello World.py", PyKing_globals)
        except Exception as error:
            error_message = traceback.format_exc()
            print_to_terminal_widget(error_message)

    def start_execute_code_thread(self):
        self.execute_code_thread = StoppableThread(target=self.execute_code, daemon=True)
        self.execute_code_thread.start()


    def stop_execute_code_thread(self):
        if self.execute_code_thread and self.execute_code_thread.is_alive():
            self.execute_code_thread.stop()  








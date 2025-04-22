import tkinter as tk
from tkinter import *
import threading
import code

from gui import root
from code_editor import code_editor
from terminal import terminal
from file_management import file_manager
from options_handler import options_handler
from virtual_environment import Snake


#help from chatgpt to get everything working
def print_to_terminal_widget(*args):
    output = " ".join(map(str, args)) + "\n"
    terminal.text_widget.insert(tk.END, output)



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
    
    def stop_if_stopped(self):
        if self.stopped():
            self.join()
        from terminal import terminal
        terminal.show_current_directories()




def execute_code():
    
    PyKing_functions = {
    "print": print_to_terminal_widget,
    "Snake": Snake
    }

    # Create an interpreter with your custom context
    interpreter = code.InteractiveInterpreter(locals=PyKing_functions)

    try:
        file_manager.load_grid_directory(options_handler.get_variable("current_grid_directory")) #ask to save before
        root.update_idletasks()
        code_string = code_editor.code_editor_widget.get("1.0", END)
        exec(code_string, PyKing_functions)

        # buffer = ""
        # for line in code_string.splitlines():
        #     buffer += line + "\n"
        #     if interpreter.runsource(buffer, symbol="exec"):
        #         continue
        #     else:
        #         buffer = ""
        
    except Exception as error:
        print_to_terminal_widget(error)

execute_code_thread = None





def start_execute_code_thread():
    global execute_code_thread 
    execute_code_thread = StoppableThread(target=execute_code)
    execute_code_thread.start()

def stop_execute_code_thread():
    global execute_code_thread
    execute_code_thread.stop()

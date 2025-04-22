import tkinter as tk
from tkinter import *
import threading
import code
import time

from gui import root
from code_editor import code_editor
from file_management import file_manager
from options_handler import options_handler
from virtual_environment import Snake


#help from chatgpt to get everything working
def print_to_terminal_widget(*args):
    output = " ".join(map(str, args)) + "\n"
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
    
    def stop_if_stopped(self):
        if self.stopped():
            self.join()

        root.terminal.show_current_directories()




def execute_code():
    
    PyKing_functions = {
    "print": print_to_terminal_widget,
    "Snake": Snake
    }

    # Create an interpreter with your custom context
    interpreter = code.InteractiveInterpreter(locals=PyKing_functions)

    try:
        file_manager.open_grid(options_handler.get_variable("current_grid_directory")) #ask to save before
        root.update_idletasks()
        code_string = code_editor.text_widget.get("1.0", END)
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


# def wait_for():
#     while execute_code_thread.is_alive():
#         print("still runnin")
#         time.sleep(.1)
#     from virtual_environment import grid_man
#     print(grid_man.cells[0].type)


def start_execute_code_thread():
    global execute_code_thread 
    execute_code_thread = StoppableThread(target=execute_code)
    execute_code_thread.start()
    # idk = threading.Thread(target=wait_for)
    # idk.start()
    




def stop_execute_code_thread():
    global execute_code_thread
    if execute_code_thread and execute_code_thread.is_alive():
        execute_code_thread.stop()


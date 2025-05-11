import tkinter as tk
from tkinter import *
import threading
import code
import traceback
import sys
import io


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


class CodeExecution:
    def __init__(self, root):
        self.root = root
        self.execute_code_thread = None


    def execute_code(self):
        PyKing_functions = {
            "print": print_to_terminal_widget,
            "Snake": Snake
        }

        interpreter = code.InteractiveInterpreter(locals=PyKing_functions)

        self.root.file_manager.open_grid(settings_handler.get_variable("current_grid_directory"))
        self.root.update_idletasks()
        code_string = self.root.code_editor.frame.text_widget.get("1.0", END)

        buffer = ""
        stderr_buffer = io.StringIO()
        original_stderr = sys.stderr
        sys.stderr = stderr_buffer  # Redirect stderr before the loop

        try:
            for line in code_string.splitlines():
                buffer += line + "\n"
                if self.execute_code_thread.stopped():
                    return
                success = interpreter.runsource(buffer, symbol="exec")
                if success:
                    continue  # More input expected
                else:
                    buffer = ""  # Reset buffer after complete statement
        finally:
            sys.stderr = original_stderr  # Always restore stderr

        error_output = stderr_buffer.getvalue()
        if error_output:
            print_to_terminal_widget(error_output)

    def start_execute_code_thread(self):
        self.execute_code_thread = StoppableThread(target=self.execute_code)
        self.execute_code_thread.start()

    def stop_execute_code_thread(self):
        if self.execute_code_thread and self.execute_code_thread.is_alive():
            self.execute_code_thread.stop()  








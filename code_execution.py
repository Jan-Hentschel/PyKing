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
import os

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
    def __init__(self, target_path):
        super().__init__()
        self.target_path = os.path.abspath(target_path)
        from gui import root
        self._quit_event  = threading.Event()
        self._pause_event = threading.Event()
        
        self._pause_event.set()        # start unpaused
        self._one_step    = False      # flag for stepping

    @property
    def wait_time(self):
        # Always invert the current slider value
        from gui import root
        tickrate = root.toolbar.tick_rate_slider.get()
        # Avoid division by zero
        return 1.0 / tickrate if tickrate else 0.01
    
    def user_line(self, frame):
        # Handle quit
        if self._quit_event.is_set():
            self.set_quit()
            return

        if os.path.abspath(frame.f_code.co_filename) != self.target_path:
            self.set_step()
            return
        
        # Block here when paused
        self._pause_event.wait()

        # Display line + locals
        lineno   = frame.f_lineno
        filename = frame.f_code.co_filename
        src      = linecache.getline(filename, lineno).rstrip()
        print_to_terminal_widget(f"▶ {filename}:{lineno} — {src}")
        # Make a shallow copy of locals
        user_locals = dict(frame.f_locals)

        # Remove the builtins key entirely
        user_locals.pop("__builtins__", None)

        # Now display only the remaining names
        print_to_terminal_widget(f"📦 Locals: {user_locals}")

        # Delay
        # report line & locals …
        timeout = self.wait_time
        # This will wake if unpaused (pause_event) or after timeout:
        
        time.sleep(timeout)

        self.set_step()

        # If this was a single-step request, pause again
        if self._one_step:
            self._pause_event.clear()  # block next
            self._one_step = False

    def run_file(self, filename, custom_globals):
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()

        # Compile with filename so co_filename matches
        code_obj = compile(source, filename, "exec")

        self._quit_event.clear()
        self._pause_event.set()
        self._one_step = False

        # Run the compiled object instead of raw source
        self.run(code_obj, custom_globals)

    # Control API
    def pause(self):
        self._pause_event.clear()

    def resume(self):
        self._pause_event.set()

    def step_once(self):
        # next user_line will run exactly one step then pause
        self._one_step = True
        self._pause_event.set()

    def quit(self):
        self._quit_event.set()
        self._pause_event.set()

class CodeExecution:
    def __init__(self, root):
        self.root = root
        self.debugger = None
        self.exec_thread = None

    def execute_code(self):
        # Prepare globals
        PyKing_globals = {
            "Snake": Snake,
            "__builtins__": dict(__builtins__),
            "__name__": "__main__"
        }
        PyKing_globals["__builtins__"]["print"] = print_to_terminal_widget

        cursor_position = self.root.code_editor.frame.text_widget.index("insert")
        self.root.file_manager.open_grid(settings_handler.get_variable("current_grid_directory"))
        self.root.code_editor.frame.text_widget.mark_set("insert", cursor_position)
        self.root.update_idletasks()

        # Instantiate debugger
        self.debugger = Debugger(settings_handler.get_variable("current_file_directory"))
        try:
            self.debugger.run_file(settings_handler.get_variable("current_file_directory"), PyKing_globals)
        except Exception:
            import traceback
            print_to_terminal_widget(traceback.format_exc())

    def start_execute_code_thread(self):
        # fire off code execution in a thread so GUI stays responsive
        self.exec_thread = StoppableThread(target=self.execute_code, daemon=True)
        self.exec_thread.start()

    def stop_execute_code_thread(self):
        # This only stops the thread wrapper, not the debugger itself
        if self.exec_thread and self.exec_thread.is_alive():
            self.exec_thread.stop()
        if self.debugger:
            self.debugger.quit()

    # New methods to tie to your GUI controls:
    def pause_debugger(self):
        if self.debugger:
            self.debugger.pause()

    def resume_debugger(self):
        if self.debugger:
            self.debugger.resume()

    def step_debugger(self):
        if self.debugger:
            self.debugger.step_once()





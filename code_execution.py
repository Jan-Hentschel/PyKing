import threading
import sys
import bdb
import time
import linecache
import os
import builtins
import traceback
from typing import Any
from types import FrameType

from settings_handler import settings_handler

from gui import Root
from virtual_environment import Snake

#help from chatgpt to get everything working
def print_to_terminal_widget(*args: Any):
    try:
        from gui import root
        output: str = " ".join(map(str, args))
        root.terminal.print(output)
    except ImportError:
        pass

class TerminalWriter:
    def write(self, text: str):
        print_to_terminal_widget(text.rstrip("\n"))
    def flush(self):
        pass

# At startup:

#https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
class StoppableThread(threading.Thread):
    
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args: Any, **kwargs: Any):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class Debugger(bdb.Bdb):
    def __init__(self, target_path: str):
        super().__init__()
        from gui import root
        self.root: Root = root
        self.target_path: str = os.path.abspath(target_path)
        self._quit_event  = threading.Event()
        self._pause_event = threading.Event()
        
        self._pause_event.set()        # start unpaused
        self._one_step    = False      # flag for stepping

    @property
    def wait_time(self):
        # Always invert the current slider value

        tickrate = self.root.toolbar.tick_rate_slider.get()
        # Avoid division by zero
        return 1.0 / tickrate if tickrate else 0.01
    
    def user_line(self, frame: FrameType):
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

        # Make a shallow copy of locals
        user_locals = dict(frame.f_locals)

        # Remove the builtins key entirely
        user_locals.pop("__builtins__", None)

        # Now display only the remaining names
        
        if self.root.settings_variables["show_debugger_prints"] == "True":
            print_to_terminal_widget(f"▶ {filename}:{lineno} — {src}")
            print_to_terminal_widget(f"📦 Locals: {user_locals}")
            

        # Delay
        # report line & locals …
        # This will wake if unpaused (pause_event) or after timeout:
        
        time.sleep(self.wait_time)

        self.set_step()

        # If this was a single-step request, pause again
        if self._one_step:
            self._pause_event.clear()  # block next
            self._one_step = False

    def run_file(self, filename: str, custom_globals: dict[str, Any]):
        folder = os.path.dirname(os.path.abspath(filename))
        if folder not in sys.path:
            sys.path.insert(0, folder)

        with open(filename, "r", encoding="utf-8") as f:
            source: str = f.read()

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
    def __init__(self, root: Root):
        self.root: Root = root
        self.debugger: Debugger = None # type: ignore 
        self.exec_thread: StoppableThread = None # type: ignore 

    def execute_code(self):
        sys.stdout = TerminalWriter()
        # Prepare globals
        PyKing_globals: dict[str, Any] = {
            "__builtins__": dict(__builtins__),
            "__name__": "__main__"
        }
        PyKing_globals["__builtins__"]["print"] = print_to_terminal_widget
        

        setattr(builtins, "Snake", Snake)

        cursor_position: str = self.root.code_editor.frame.text_widget.index("insert")

        self.root.file_manager.open_grid(settings_handler.get_variable("current_grid_directory"))
        self.root.code_editor.frame.text_widget.mark_set("insert", cursor_position)
        self.root.update_idletasks()

        # Instantiate debugger
        self.debugger = Debugger(settings_handler.get_variable("current_file_directory"))

        try:
            self.debugger.run_file(settings_handler.get_variable("current_file_directory"), PyKing_globals)
        except Exception:
            
            print_to_terminal_widget(traceback.format_exc())
        
        sys.stdout = sys.__stdout__

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





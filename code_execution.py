import tkinter as tk
from tkinter import *
import threading
import code


from options_handler import options_handler
from virtual_environment import Snake


#help from chatgpt to get everything working
def print_to_terminal_widget(*args):
    from gui import root
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



class CodeExecution:
    def __init__(self, root):
        self.root = root
        self.execute_code_thread = None


    
    def execute_code(self):
        
        PyKing_functions = {
        "print": print_to_terminal_widget,
        "Snake": Snake
        }

        # Create an interpreter with your custom context
        interpreter = code.InteractiveInterpreter(locals=PyKing_functions)

        try:
            self.root.file_manager.open_grid(options_handler.get_variable("current_grid_directory")) #ask to save before
            self.root.update_idletasks()
            code_string = self.root.code_editor.text_widget.get("1.0", END)
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

    def start_execute_code_thread(self):
        self.execute_code_thread = StoppableThread(target=self.execute_code)
        self.execute_code_thread.start()
        # idk = threading.Thread(target=wait_for)
        # idk.start()
        




    def stop_execute_code_thread(self):
        if self.execute_code_thread and self.execute_code_thread.is_alive():
            self.execute_code_thread.stop()  



# def wait_for():
#     while execute_code_thread.is_alive():
#         print("still runnin")
#         time.sleep(.1)
#     from virtual_environment import grid_man
#     print(grid_man.cells[0].type)





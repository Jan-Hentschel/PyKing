import json
from pathlib import Path


from utility import * # type: ignore 

from settings_handler import settings_handler
from gui import Root

class Terminal:
    def __init__(self, root: Root, master: DefaultSecondaryFrame):
        self.status_seperator: str = "_"
        self.frame = DefaultTextFrame(master, bg=root.primary_color, bd=0,)
        self.frame.pack(fill=BOTH, expand=True)

    def calculate_seperator_length(self, status: str) -> int:
        longest_line: int = len(status)

        if len(status.splitlines()) > 1:
            longest_line = max(len(line) for line in status.splitlines())

        longest_line = max(longest_line, len(f"File: {settings_handler.get_variable("current_file_directory")} "), len(f"Grid: {settings_handler.get_variable("current_grid_directory")} "))

        return longest_line

    def show_current_directories(self, status: str) -> None:
        seperator: str = self.status_seperator * self.calculate_seperator_length(status)
        try:
            with open(settings_handler.get_variable('current_grid_directory'), "r", encoding="utf-8") as file:
                content: str = file.read()
        except FileNotFoundError:
            content = ""
        grid_dictionary = json.loads(content) if content else {}
        message: str = grid_dictionary["message"] if "message" in grid_dictionary else ""
        if message:
            message += f"\n{seperator}\n\n"
            path = settings_handler.get_variable('current_grid_directory')

            filename = Path(path).name + ":\n\n"
        else: 
            message = ""
            filename = ""

        self.frame.text_widget.delete('1.0', END)
        self.frame.text_widget.insert(tk.END, 
                    f"{status}\n"
                    f"{seperator}\n\n"
                    f"File: {settings_handler.get_variable('current_file_directory')}\n"
                    f"Grid: {settings_handler.get_variable('current_grid_directory')}\n"
                    f"{seperator}\n\n"
                    f"{filename}"
                    f"{message}"
                    )
                    

    def print(self, string: str) -> None:
        self.frame.text_widget.insert(tk.END, string + "\n")   

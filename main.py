from options_handler import options_handler

from gui import root
from file_management import file_manager


if __name__ == "__main__":
    try:
        file_manager.load_file_directory(options_handler.get_variable("current_file_directory"))
        file_manager.load_grid_directory(options_handler.get_variable("current_grid_directory"))
    except:
        raise Exception
    root.bind("<Control-s>", lambda event: file_manager.save_file_and_grid())
    root.mainloop()


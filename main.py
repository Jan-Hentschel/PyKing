from options_handler import get_variable

from gui import root
from file_management import file_manager


if __name__ == "__main__":
    try:
        file_manager.load_file_directory(get_variable("current_file_directory"))
        file_manager.load_grid_directory(get_variable("current_grid_directory"))
    except:
        raise Exception
    root.bind("<Control-s>", file_manager.save_file)
    root.mainloop()


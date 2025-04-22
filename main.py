from options_handler import get_variable

from gui import root
from filetree import load_file_directory, load_grid_directory, save_file


if __name__ == "__main__":
    try:
        load_file_directory(get_variable("current_file_directory"))
        load_grid_directory(get_variable("current_grid_directory"))
    except:
        raise Exception
    root.bind("<Control-s>", save_file)
    root.mainloop()


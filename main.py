from gui import root
from filetree import load_file_directory, load_grid_directory
from options_handler import get_variable
if __name__ == "__main__":
    try:
        load_file_directory(get_variable("current_file_directory")[1:-1])
        load_grid_directory(get_variable("current_grid_directory")[1:-1])
    except:
        raise Exception
    root.mainloop()


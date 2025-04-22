from gui import root
from file_management import file_manager


if __name__ == "__main__":
    file_manager.open_python_file_and_grid_from_options()        
    root.bind("<Control-s>", lambda event: file_manager.save_python_file_and_grid())
    root.mainloop()


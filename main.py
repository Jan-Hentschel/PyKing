from gui import root



if __name__ == "__main__":
    root.file_manager.open_python_file_and_grid_from_options()        
    root.bind("<Control-s>", lambda event: root.file_manager.save_python_file_and_grid())
    root.mainloop()


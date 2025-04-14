import gui

from virtual_environment import *

if __name__ == "__main__":
    root.bind("<Control-x>", change_grid_man)
    root.bind("<Control-w>", spawn_grid_elements)
    root.mainloop()


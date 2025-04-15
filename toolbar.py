import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import root



#toolbar als frame erstellen
toolbar_frame = Frame(root, height=68, bg="#333333")


from filetree import save_file, load_file, load_grid, save_grid, new_file, new_grid

new_file_button = Button(toolbar_frame, text ="New File", command = new_file)
new_file_button.pack(side="left")

save_button = Button(toolbar_frame, text ="Save File", command = save_file)
save_button.pack(side="left")

load_button = Button(toolbar_frame, text ="Load File", command = load_file)
load_button.pack(side="left")

new_grid_button = Button(toolbar_frame, text ="New Grid", command = new_grid)
new_grid_button.pack(side="left")

save_grid_button = Button(toolbar_frame, text ="Save Grid", command = save_grid)
save_grid_button.pack(side="left")

load_grid_button = Button(toolbar_frame, text ="Load Grid", command = load_grid)
load_grid_button.pack(side="left")



from code_execution import executeCode
excecute_code_button = Button(toolbar_frame, text ="Excecute Code", command = executeCode)
excecute_code_button.pack(side="left")


from options_handler import get_variable
tick_rate_slider = Scale(toolbar_frame, from_=1, to=100, orient=HORIZONTAL, length=200)
tick_rate_slider.set(get_variable("default_tick_rate"))
tick_rate_slider.pack(side="left")


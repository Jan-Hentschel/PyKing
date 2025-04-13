import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import root



#toolbar als frame erstellen
toolbar_frame = Frame(root, height=68, bg="#333333")


from filetree import saveTestFile, loadTestFile
save_button = Button(toolbar_frame, text ="Save", command = saveTestFile)
save_button.pack(side="left")

load_button = Button(toolbar_frame, text ="Load", command = loadTestFile)
load_button.pack(side="left")



from code_execution import executeCode
excecute_code_button = Button(toolbar_frame, text ="Excecute Code", command = executeCode)
excecute_code_button.pack(side="left")


from virtual_environment import tick_rate
tick_rate_slider = Scale(toolbar_frame, from_=1, to=100, orient=HORIZONTAL, length=200)
tick_rate_slider.set(tick_rate)
tick_rate_slider.pack(side="left")
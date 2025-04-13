import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import root
from filetree import saveTestFile, loadTestFile

#toolbar als frame erstellen
toolbar_frame = Frame(root, height=68, bg="#333333")

save_button = Button(toolbar_frame, text ="Save", command = saveTestFile)
save_button.pack(side="left")
load_button = Button(toolbar_frame, text ="Load", command = loadTestFile)
load_button.pack(side="left")
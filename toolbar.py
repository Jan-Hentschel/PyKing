import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import root
from filetree import saveTestFile

#toolbar als frame erstellen
toolbar_frame = Frame(root, height=68, bg="#333333")

save_button = Button(toolbar_frame, text ="Hello", command = saveTestFile)
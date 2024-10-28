import tkinter as tk
from tkinter import *
from tkinter import ttk

from gui import horizontally_paned_window 

# Text-Feld für den Code Editor erstellen (mitte)
code_editor_widget = Text(horizontally_paned_window, bg="#3F3F3F", fg="white", bd=0)
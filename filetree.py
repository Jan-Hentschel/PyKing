import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys

from gui import horizontally_paned_window

# Frame für den Filetree erstellen (links)
file_tree_widget = Frame(horizontally_paned_window, bg="#333333")



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




test_file_path = resource_path("dist\\Files\\file.py")

def saveContentToFile(content, directory):

    with open(directory, "w", encoding="utf-8") as file:
        file.write(content)


def getContentFromFile(directory):
    with open(directory, "r", encoding="utf-8") as file:
        return file.read()
    
saveContentToFile("dumb", test_file_path)

print(getContentFromFile(test_file_path))
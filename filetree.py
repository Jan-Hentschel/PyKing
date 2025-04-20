import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys
from tkinter import filedialog
from tkinter import simpledialog
from utility import toolbar_button
import json
from options_handler import get_variable, set_variable
import gui
from code_editor import load_into_editor, getStringFromEditor

# Frame für den Filetree erstellen (links)
file_tree_frame = Frame(gui.horizontally_paned_window, bg="#333333")


def resource_path(relative_path):

    base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


from terminal import show_current_directories

test_file_path = resource_path("Files\\testfile.py")

def save_content_to_directory(directory):
    with open(directory, "w", encoding="utf-8") as file:
        file.write(getStringFromEditor())


def get_content_from_directory(directory):
    with open(directory, "r", encoding="utf-8") as file:
        return file.read()

def load_file_directory(directory):
    load_into_editor(get_content_from_directory(directory))

from virtual_environment import throw_error_to_terminal
def load_test_file():
    throw_error_to_terminal(test_file_path)
    try:
        load_file_directory(test_file_path)
    except:
        throw_error_to_terminal(Exception)

def save_test_file():
    throw_error_to_terminal(test_file_path)
    try:
        save_content_to_directory(test_file_path)
    except:
        throw_error_to_terminal(Exception)

def load_file():
    #ask to save before
    directory = filedialog.askopenfilename(initialdir=resource_path("Files"), title="Open a file", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    load_file_directory(directory)
    set_variable("current_file_directory", directory)
    show_current_directories()


def save_file():
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="Save as", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    save_content_to_directory(directory)
    set_variable("current_file_directory", directory)
    show_current_directories()



from virtual_environment import change_grid, get_grid_dict, change_grid_man

def load_grid_directory(directory):
    with open(directory, "r", encoding="utf-8") as file:
        content = file.read()
        dict = json.loads(content)
        columns = dict["columns"]
        rows = dict["rows"]
        new_cells = dict["cells"]
        change_grid(columns, rows, new_cells)
    set_variable("current_grid_directory", directory)
    show_current_directories()

def load_grid():
    #ask to save before
    directory = filedialog.askopenfilename(initialdir=resource_path("Files"), title="Open a file", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
    load_grid_directory(directory)
  

def save_grid():
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
    json_dict = json.dumps(get_grid_dict())
    with open(directory, "w", encoding="utf-8") as file:
        file.write(json_dict)
    set_variable("current_grid_directory", directory)
    show_current_directories()

    
def new_file():
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="New File", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    with open(directory, "w", encoding="utf-8") as file:
        file.write("")    
    set_variable("current_file_directory", directory)
    show_current_directories()
    

    
def create_grid(popup):
    columns = popup.column_entry.get()
    rows = popup.row_entry.get()
    change_grid_man(int(columns), int(rows))
    popup.destroy()
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="Save as", defaultextension=".json", filetypes=(("Json files", "*.json"), ("All Files", "*.*")))
    json_dict = json.dumps(get_grid_dict())
    with open(directory, "w", encoding="utf-8") as file:
        file.write(json_dict)
    set_variable("current_grid_directory", directory)
    show_current_directories()



def new_grid():
    from gui import root
    popup = Toplevel(root)
    popup.geometry("400x200")
    popup.title("Input Grid Height and Width")

    column_label = Label(popup, text="Columns:")
    column_label.pack()
    popup.column_entry = Entry(popup)
    popup.column_entry.pack()

    row_label = Label(popup, text="Rows:")
    row_label.pack()
    popup.row_entry = Entry(popup)
    popup.row_entry.pack()
    
    ok_button = toolbar_button(popup, text="OK", command=lambda: create_grid(popup))
    ok_button.pack(side="left")

    cancel_button = toolbar_button(popup, text="Cancel", command= lambda: popup.destroy())
    cancel_button.pack(side="right")

start_path=get_variable("current_filetree_directory")
def open_directory():
    treeview.delete(*treeview.get_children())
    global start_path
    start_path = filedialog.askdirectory(initialdir=resource_path("Files"), title="Open a Directory")
    set_variable("current_filetree_directory", start_path)
    display_treeview()

def display_treeview():
    start_dir_entries = os.listdir(start_path)
    parent_iid = treeview.insert(parent='', index='0', text=os.path.basename(start_path), open=True, image=directory_image)
    # inserting items to the treeview
    add_directory_to_treeview(start_path, start_dir_entries, parent_iid, file_image, directory_image)

open_directory_button = toolbar_button(file_tree_frame, text="Open Directory", command=open_directory)
open_directory_button.pack()

#https://stackoverflow.com/questions/68078498/recursively-arrange-all-folders-and-files-in-a-hierarchical-treeview-in-tkinter

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333")
style.map("Treeview", background=[("selected", "#3F3F3F")])

treeview = ttk.Treeview(file_tree_frame, show='tree')
treeview.pack(fill='both', expand=True)


def add_directory_to_treeview(parent_path, directory_entries,
               parent_iid, file_image, directory_image):
    """Creates a graphical representation of the structure
    of subdirectories and files in the specified parent_path.

    Recursive tree building for large directories can take some time.

    :param parent_path: directory path, string
    :param directory_entries: List[str]
           a list containing the names of the entries in the parent_path
           obtained using os.listdir()
    :param parent_iid: unique identifier for a treeview item, string
    :param f_image: file icon, tkinter.PhotoImage
    :param d_image: directory icon, tkinter.PhotoImage
    :return: None
    """
    for name in directory_entries:
        item_path = parent_path+os.sep+name
        # optional: file does not exist or broken symbolic link
        #if not os.path.exists(item_path):
            #print("Skipped:", item_path)
            #continue
        if os.path.isdir(item_path):
            # set subdirectory node
            subdir_iid = treeview.insert(parent=parent_iid, index='end', text=name, image=directory_image)
            try:
                # pass the iid of the subdirectory as parent iid
                # all files/folders found in this subdirectory
                # will be attached to this subdirectory node
                subdir_entries = os.listdir(item_path)
                add_directory_to_treeview(item_path, subdir_entries, subdir_iid, file_image, directory_image)
            except PermissionError:
                pass
        else:
            treeview.insert(parent=parent_iid, index='end', text=name, image=file_image)
        


# png 16x16 -> base64 strings for tkinter.PhotoImage
file_img = """
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAASUExURQAAABwcHCoqKj8/Pzp/PAAAANrcZR8AAAAGdFJOU///////ALO/pL8AAAAJcEhZcwAADr8AAA6/ATgFUyQAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuN4vW9zkAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAApnYBAOgDAACmdgEA6AMAAFBhaW50Lk5FVCA1LjEuNwADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAABsjsoPP+oYDgAAAEVJREFUKFN9jgkKACAIBMvj/19utaJNqInAGYRqXniGBuawrIM5x4WIqpwAAxTSOZhZCZqnbNi1ATiE/18JE/7pZgfCfQAADQOjIpnmOQAAAABJRU5ErkJggg==
"""
dir_img = """
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsAAAA7AAWrWiQkAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuN4vW9zkAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAAv3YBAOgDAAC/dgEA6AMAAFBhaW50Lk5FVCA1LjEuNwADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAADCrx1n7WSHCAAAAPNJREFUOE9jGAUMjFAaDM7MNP4Pov/+/cvw798/sJhlziUUNegALgnSbJx2BsiaBREAgzSGfd2qDL9+/QIbCMK+Dc9QDGSB0gz//wMt/zEJZD1UBAT6GZxKb0PZELCZQfo/siFwxslpBv/NQkMZGH7/Zji2Zg1UFAJ+A8X+/PkDxiA2CKC7hOH4FL3//x9U/T86SQfoGPxgcQEXOKxAgAlKQ0x+84aBjY0N4hVcGBhGMFeAANwAWKiDAozhyxfcGAhgakEAbgAo6kAAbMDXr7gxECAbgBIQW5tk/oMkQU4EGQjDID5IHIRB/PRZqPqGNGBgAAAHJ8Q7hrD1SAAAAABJRU5ErkJggg==
"""
file_image = PhotoImage(data=file_img)
directory_image = PhotoImage(data=dir_img)

display_treeview()
# adds a parent item to the tree
# and returns the item's iid value (generated automatically)

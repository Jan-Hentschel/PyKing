import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import sys
from tkinter import filedialog
from tkinter import simpledialog

import json

import gui
from code_editor import load_into_editor, getStringFromEditor

# Frame für den Filetree erstellen (links)
file_tree_frame = Frame(gui.horizontally_paned_window, bg="#333333")


def resource_path(relative_path):

    base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from options_handler import change_variable_to
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
    change_variable_to("current_file_directory", directory)
    show_current_directories()


def save_file():
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="Save as", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    save_content_to_directory(directory)
    change_variable_to("current_file_directory", directory)
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
    change_variable_to("current_grid_directory", directory)
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
    change_variable_to("current_grid_directory", directory)
    show_current_directories()

    
def new_file():
    directory = filedialog.asksaveasfilename(initialdir=resource_path("Files"), title="New File", defaultextension=".py", filetypes=(("Python files", "*.py"), ("All Files", "*.*")))
    with open(directory, "w", encoding="utf-8") as file:
        file.write("")    
    change_variable_to("current_file_directory", directory)
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
    change_variable_to("current_grid_directory", directory)
    show_current_directories()


from utility import toolbar_button
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





#https://stackoverflow.com/questions/68078498/recursively-arrange-all-folders-and-files-in-a-hierarchical-treeview-in-tkinter

ttk.Label(file_tree_frame, text="Treeview(hierarchical)").pack()

treeview = ttk.Treeview(file_tree_frame, show='tree')
treeview.pack(fill='both', expand=True)


def new_folder(parent_path, directory_entries,
               parent_iid, f_image, d_image):
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
            subdir_iid = treeview.insert(parent=parent_iid,
                                         index='end',
                                         text=name,
                                         image=d_image)
            try:
                # pass the iid of the subdirectory as parent iid
                # all files/folders found in this subdirectory
                # will be attached to this subdirectory node
                subdir_entries = os.listdir(item_path)
                new_folder(parent_path=item_path,
                           directory_entries=subdir_entries,
                           parent_iid=subdir_iid,
                           f_image=f_image,
                           d_image=d_image)
            except PermissionError:
                pass
        else:
            treeview.insert(parent=parent_iid,
                            index='end',
                            text=name,
                            image=f_image)
        print(item_path)


# png 16x16 -> base64 strings for tkinter.PhotoImage
file_img = """
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABGdB
TUEAALGPC/xhBQAAAAlwSFlzAAAScwAAEnMBjCK5BwAAAalJREFU
OE99kUtLAmEUhg38Af6a6he06SJIF8FFREVtqkVEkBB2IcJIRDAk
80KrNq3CWihuuuh4GVIwM9BSa0bHUXGc8X7p1Bc6jtLLxzAwz3Pm
nPMNcaWySCR6CYVoOgMvzWaz3W63Wq1GowFPsVg8PDIqkUjg019A
gEOSJHAowEHAhDidzmAwGI3FEPZTXSDwafiJ3W5nWRbH8TSVGSAI
aBDi8TiGYT6fz2QyCwU+Dc0ADanX67XfWK3W/4QOjYRqtWqxWIQC
mhKh/NpAVyoVs/GcclwzabI7NF/odILocrnsPFwvGRcS6uUeob8T
RDOxMGuYz2vkfsdtVxhIg1AqMqnTRUYrD+iU2Vy+R+jvBMpTN+aC
Zi6umo2+RXouDmgkFJ4fyLNNNvUFdJFM0kfTuQOpfk9ZZLmuQBBE
Z4Np/VrtapVSKwqf7wmlLLc/iR9vGAyGnrWCgC4ImmZpKqVbKeoV
xK4sq5pI7kgjAfzCZBIK/PWX8jRxspRVjVPbY8FLLcdxfQKZ8vlx
j9eLebxuzOPGMO/j/YdyJro1dWezPblc4defieF8A+ZBma193+p6
AAAAAElFTkSuQmCC
"""
dir_img = """
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABGdB
TUEAALGPC/xhBQAAAAlwSFlzAAAScgAAEnIBXmVb4wAAAihJREFU
OE990vtv0kAcAPDh4wd/8w/yp5n4i4kkmizoBMKcRIfG7YepWSSZ
MSTGSXQao8wtjIw5ZkJEJ4+O0CGvoWhSCmw0sFJaHoU+GEJbyDax
EwMjQS+Xy30v97m7791JOF4Y+FMOBEJsj508PXD8lERyoj3Yp4ig
XclNRSlyg0F0TFxLRbXFyAMqaarkQrXabmfO4eqdoBRWtgQnujGM
+DRVbIYnTU3Wvrf7hcubGRToTOsFvK3V/JZyy6KeCXL7CZc3CEVj
k7bTO85/A+FDgwr6rKNIQEtu6XnC0Ch/+j+wCSXXulke994vxh/X
sNkGaaXTfXfYVLbEIwk2gbQBpstxz0QOmq6mdXxxmUr1A8Wg4i8o
rLoWh2C3hvhxr5KcqhMLVMrRJ4eCX97irL/qFh6fdxkvQoAaj4yz
iTv17KsyYu8D8t7hg+q7fXahjr50GaWQawT7OkbDN3/u6JIflQxb
qXN8zzsQniv7tGGv9Czx/tz64gXIqcTCagoaqWxpcO/dKBzL4oTI
uu+QBYaaBX2DeBgyDoJmKQzIMyEVE5Wz8HXMO7W29tnnD8TiiS5A
HbIGPi1kJn3zZzdWLh2CoIKGZHRUlXJPzs29XVoy40SuC6p0lgyo
+PS4e/aM8835GHALDWvY2LVybAxcVs881XtAUEyjC8SEGPx7bfu2
4/mgzfwiEgSz4dcJixRxjq5YVtEM1r6oHiDGuP9RwHS1TOaP/tCj
/d+VL1STn8NNZQAAAABJRU5ErkJggg==
"""
file_image = PhotoImage(data=file_img)
dir_image = PhotoImage(data=dir_img)

# adds a parent item to the tree
# and returns the item's iid value (generated automatically)
parent_iid = treeview.insert(parent='',
                             index='0',
                             text='Documents',
                             open=True,
                             image=dir_image)

start_path = os.path.expanduser(r"~\Documents")
start_dir_entries = os.listdir(start_path)

# inserting items to the treeview
new_folder(parent_path=start_path,
           directory_entries=start_dir_entries,
           parent_iid=parent_iid,
           f_image=file_image,
           d_image=dir_image)
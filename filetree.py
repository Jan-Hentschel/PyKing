from tkinter import *
from tkinter import ttk
import os
from tkinter import filedialog
from utility import toolbar_button


from utility import resource_path, path_from_relative_path
from options_handler import get_variable, set_variable

from gui import horizontally_paned_window
from file_management import file_manager


# Frame für den Filetree erstellen (links)
file_tree_frame = Frame(horizontally_paned_window, bg="#333333")


def open_file_from_tree(iid):
    
    name = treeview.item(iid)["text"]

    added_path = f"/{name}"
    base_path = start_path

    cur_iid = iid
    parent_names= []

    while treeview.parent(cur_iid):

        parent_iid=treeview.parent(cur_iid)
        parent_name = treeview.item(parent_iid)["text"]

        if parent_name not in base_path:
            parent_names.append(parent_name)

        cur_iid = parent_iid
    for parent_name in reversed(parent_names):
        base_path += f"/{parent_name}"

    directory = base_path + added_path
    if directory[-3:] == ".py":
        file_manager.load_file_directory(directory)
    elif directory[-5:]==".json":
        file_manager.load_grid_directory(directory)
    else:
        print("cant open im sowy")


start_path=get_variable("current_filetree_directory")
def open_directory():
    treeview.delete(*treeview.get_children())
    global start_path
    start_path = filedialog.askdirectory(initialdir=path_from_relative_path("Files"), title="Open a Directory")
    set_variable("current_filetree_directory", start_path)
    display_treeview()

def display_treeview():
    start_dir_entries = os.listdir(start_path)
    parent_iid = treeview.insert(parent='', index='0', text=os.path.basename(start_path), open=True, image=folder_icon)
    # inserting items to the treeview
    add_directory_to_treeview(start_path, start_dir_entries, parent_iid)
    

open_directory_button = toolbar_button(file_tree_frame, text="Open Directory", command=open_directory)
open_directory_button.pack()

#https://stackoverflow.com/questions/68078498/recursively-arrange-all-folders-and-files-in-a-hierarchical-treeview-in-tkinter

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333")
style.map("Treeview", background=[("selected", "#3F3F3F")])

treeview = ttk.Treeview(file_tree_frame, show='tree')
treeview.pack(fill='both', expand=True)



file_icon = PhotoImage(file=resource_path('Assets\\file_icon.png'))

python_file_icon = PhotoImage(file=resource_path('Assets\\python_file_icon.png'))
json_file_icon = PhotoImage(file=resource_path('Assets\\json_file_icon.png'))

folder_icon = PhotoImage(file=resource_path('Assets\\folder_icon.png'))


def add_directory_to_treeview(parent_path, directory_entries, parent_iid):

    for index, name in enumerate(directory_entries):
        tag = f"file_{index}"
        item_path = parent_path+os.sep+name
        # optional: file does not exist or broken symbolic link
        #if not os.path.exists(item_path):
            #print("Skipped:", item_path)
            #continue
        if os.path.isdir(item_path):
            # set subdirectory node
            subdir_iid = treeview.insert(parent=parent_iid, index='end', text=name, image=folder_icon, tags=tag)
            try:
                # pass the iid of the subdirectory as parent iid
                # all files/folders found in this subdirectory
                # will be attached to this subdirectory node
                subdir_entries = os.listdir(item_path)
                add_directory_to_treeview(item_path, subdir_entries, subdir_iid)
            except PermissionError:
                pass
        else:
            if name[-3:] == ".py":
                iid=treeview.insert(parent=parent_iid, index='end', text=name, image=python_file_icon, tags=tag)
                treeview.tag_bind(tag, "<Double-Button-1>", lambda event, item_iid=iid: open_file_from_tree(item_iid))
                
            elif name[-5:]==".json":
                iid=treeview.insert(parent=parent_iid, index='end', text=name, image=json_file_icon, tags=tag)
                treeview.tag_bind(tag, "<Double-Button-1>", lambda event, item_iid=iid: open_file_from_tree(item_iid))
            else:
                iid=treeview.insert(parent=parent_iid, index='end', text=name, image=file_icon, tags=tag)
        
                




display_treeview()
# adds a parent item to the tree
# and returns the item's iid value (generated automatically)

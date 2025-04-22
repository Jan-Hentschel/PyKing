from tkinter import *
from tkinter import ttk
import os
from tkinter import filedialog
from utility import ToolbarButton


from utility import resource_path, path_from_relative_path
from options_handler import options_handler

from gui import horizontally_paned_window
from file_management import file_manager

class Filetree:
    def __init__(self):
        self.frame = Frame(horizontally_paned_window, bg="#333333")
        self.start_path = options_handler.get_variable("current_filetree_directory")

        self.file_icon = PhotoImage(file=resource_path('Assets\\file_icon.png'))
        self.python_file_icon = PhotoImage(file=resource_path('Assets\\python_file_icon.png'))
        self.json_file_icon = PhotoImage(file=resource_path('Assets\\json_file_icon.png'))
        self.folder_icon = PhotoImage(file=resource_path('Assets\\folder_icon.png'))

        self.open_directory_button = ToolbarButton(self.frame, text="Open Directory", command=self.open_directory)
        self.open_directory_button.pack()

        #https://stackoverflow.com/questions/68078498/recursively-arrange-all-folders-and-files-in-a-hierarchical-treeview-in-tkinter

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333")
        self.style.map("Treeview", background=[("selected", "#3F3F3F")])

        self.treeview = ttk.Treeview(self.frame, show='tree')
        self.treeview.pack(fill='both', expand=True)

        self.display_treeview()





    def open_file_from_tree(self, iid):
        
        name = self.treeview.item(iid)["text"]

        added_path = f"/{name}"
        base_path = self.start_path

        cur_iid = iid
        parent_names= []

        while self.treeview.parent(cur_iid):

            parent_iid = self.treeview.parent(cur_iid)
            parent_name = self.treeview.item(parent_iid)["text"]

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


    
    def open_directory(self):
        self.treeview.delete(*self.treeview.get_children())
 
        self.start_path = filedialog.askdirectory(initialdir=path_from_relative_path("Files"), title="Open a Directory")
        options_handler.set_variable("current_filetree_directory", self.start_path)
        self.display_treeview()

    def display_treeview(self):
        start_dir_entries = os.listdir(self.start_path)
        parent_iid = self.treeview.insert(parent='', index='0', text=os.path.basename(self.start_path), open=True, image=self.folder_icon)
        # inserting items to the treeview
        self.add_directory_to_treeview(self.start_path, start_dir_entries, parent_iid)
        



    def add_directory_to_treeview(self, parent_path, directory_entries, parent_iid):

        for index, name in enumerate(directory_entries):
            tag = f"file_{index}"
            item_path = parent_path+os.sep+name
            # optional: file does not exist or broken symbolic link
            #if not os.path.exists(item_path):
                #print("Skipped:", item_path)
                #continue
            if os.path.isdir(item_path):
                # set subdirectory node
                subdir_iid = self.treeview.insert(parent=parent_iid, index='end', text=name, image=self.folder_icon, tags=tag)
                try:
                    # pass the iid of the subdirectory as parent iid
                    # all files/folders found in this subdirectory
                    # will be attached to this subdirectory node
                    subdir_entries = os.listdir(item_path)
                    self.add_directory_to_treeview(item_path, subdir_entries, subdir_iid)
                except PermissionError:
                    pass
            else:
                if name[-3:] == ".py":
                    iid = self.treeview.insert(parent=parent_iid, index='end', text=name, image=self.python_file_icon, tags=tag)
                    self.treeview.tag_bind(tag, "<Double-Button-1>", lambda event, item_iid=iid: self.open_file_from_tree(item_iid))
                    
                elif name[-5:]==".json":
                    iid = self.treeview.insert(parent=parent_iid, index='end', text=name, image=self.json_file_icon, tags=tag)
                    self.treeview.tag_bind(tag, "<Double-Button-1>", lambda event, item_iid=iid: self.open_file_from_tree(item_iid))
                else:
                    iid = self.treeview.insert(parent=parent_iid, index='end', text=name, image=self.file_icon, tags=tag)
            
                    




    

file_tree = Filetree()
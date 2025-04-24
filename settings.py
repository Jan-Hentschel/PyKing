from utility import *

class Settings:
    def __init__(self, root):
        self.root = root

    def open_settings(self):
        self.settings_toplevel = DefaultToplevel(self.root)
        self.settings_toplevel.geometry("400x200")
        self.settings_toplevel.title("Settings")
        self.settings_toplevel.iconbitmap(resource_path("Assets\\Icon.ico"))

        self.foreground_color_label = DefaultLabel(self.settings_toplevel, text="Foreground Color:")
        self.foreground_color_label.pack()

        self.foreground_color_entry = DefaultEntry(self.settings_toplevel)
        self.foreground_color_entry.pack()

        self.primary_color_label = DefaultLabel(self.settings_toplevel, text="Primary Color:")
        self.primary_color_label.pack()

        self.primary_color_entry = DefaultEntry(self.settings_toplevel)
        self.primary_color_entry.pack()

        self.secondary_color_label = DefaultLabel(self.settings_toplevel, text="Secondary Color:")
        self.secondary_color_label.pack()

        self.secondary_color_entry = DefaultEntry(self.settings_toplevel)
        self.secondary_color_entry.pack()
        
        self.ok_button = DefaultButton(self.settings_toplevel, text="OK", command=lambda: self.apply_settings())
        self.ok_button.pack(side="left")

        self.cancel_button = DefaultButton(self.settings_toplevel, text="Cancel", command= lambda: self.settings_toplevel.destroy())
        self.cancel_button.pack(side="right")
        
    def change_foreground_color(self, color):
        self.root.foreground_color = color
        self.root.update_colors()

    def change_primary_color(self, color):
        self.root.primary_color = color
        self.root.update_colors()

    def change_secondary_color(self, color):
        self.root.secondary_color = color
        self.root.update_colors()
    
    def apply_settings(self):
        foreground_color = self.foreground_color_entry.get()
        primary_color = self.primary_color_entry.get()
        secondary_color = self.secondary_color_entry.get()

        if foreground_color:
            self.change_foreground_color(foreground_color)
        if primary_color:
            self.change_primary_color(primary_color)

        if secondary_color:
            self.change_secondary_color(secondary_color)

        self.settings_toplevel.destroy()

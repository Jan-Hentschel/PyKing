from utility import *
from settings_handler import settings_handler

class Settings:
    def __init__(self, root):
        self.root = root

    def open_settings(self):
        self.settings_toplevel = DefaultToplevel(self.root)
        self.settings_toplevel.geometry("400x800")
        self.settings_toplevel.title("Settings")
        self.settings_toplevel.iconbitmap(resource_path("Assets\\Icon.ico"))

        
        self.ask_to_save_on_close_check = SettingsCheckbutton(self.settings_toplevel, "ask_to_save_on_close", text = "Ask to Save on Close")

        self.remember_last_file_check = SettingsCheckbutton(self.settings_toplevel, "remember_last_file", text = "Remember Last File") 
        self.remember_last_grid_check = SettingsCheckbutton(self.settings_toplevel, "remember_last_grid", text = "Remember Last Grid") 
        self.remember_last_directory_check = SettingsCheckbutton(self.settings_toplevel, "remember_last_directory", text = "Remember Last Directory") 
            
        self.show_snake_actions_in_terminal_check = SettingsCheckbutton(self.settings_toplevel, "show_snake_actions_in_terminal", text = "Show Snake Actions in Terminal")

        self.ask_to_save_on_close_check.pack()

        self.remember_last_file_check.pack() 
        self.remember_last_grid_check.pack() 
        self.remember_last_directory_check.pack() 

        self.show_snake_actions_in_terminal_check.pack()

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

        self.reset_to_darkmode_button = DefaultButton(self.settings_toplevel, text="Reset To Darkmode", command=lambda: self.apply_darkmode())
        self.reset_to_darkmode_button.pack(side="top")
        
        self.ok_button = DefaultButton(self.settings_toplevel, text="OK", command=lambda: self.apply_settings())
        self.ok_button.pack(side="left")

        self.cancel_button = DefaultButton(self.settings_toplevel, text="Cancel", command= lambda: self.settings_toplevel.destroy())
        self.cancel_button.pack(side="right")
        
    def apply_darkmode(self):
        self.apply_settings()
        self.change_foreground_color("#FFFFFF")
        self.change_primary_color("#3F3F3F")
        self.change_secondary_color("#333333")
        self.settings_toplevel.destroy()

    def change_foreground_color(self, color):
        self.root.foreground_color = color
        settings_handler.set_variable("foreground_color", color)
        self.root.update_colors()

    def change_primary_color(self, color):
        self.root.primary_color = color
        settings_handler.set_variable("primary_color", color)
        self.root.update_colors()

    def change_secondary_color(self, color):
        self.root.secondary_color = color
        settings_handler.set_variable("secondary_color", color)
        self.root.update_colors()
    
    def apply_settings(self):
        foreground_color = self.foreground_color_entry.get()
        primary_color = self.primary_color_entry.get()
        secondary_color = self.secondary_color_entry.get()


        self.ask_to_save_on_close_check.apply()

        self.remember_last_file_check.apply() 
        self.remember_last_grid_check.apply() 
        self.remember_last_directory_check.apply() 

        self.show_snake_actions_in_terminal_check.apply()

        if foreground_color:
            self.change_foreground_color(foreground_color)
        if primary_color:
            self.change_primary_color(primary_color)
        if secondary_color:
            self.change_secondary_color(secondary_color)

        self.settings_toplevel.destroy()

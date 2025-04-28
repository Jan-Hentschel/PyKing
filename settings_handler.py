import os
def path_from_relative_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SettingsHandler:
    def __init__(self):
        self.directory = path_from_relative_path("settings.txt")
    

    def get_variable(self, name):
        with open(self.directory, "r", encoding="utf-8") as file:
            for line in file:
                if name in line:
                    split_line = line.split("=")
                    return split_line[1][1:-1]
            raise Exception(f"could not find {name} in settings.txt")
            
        
    def set_variable(self, name, new_value):
        with open(self.directory, "r", encoding="utf-8") as file:
            old_file = file.readlines()

        for i, line in enumerate(old_file):
            if name in line:
                old_file[i] = f"{name} = {new_value}\n"

        with open(self.directory, "w", encoding="utf-8") as file:
            file.writelines(old_file)

settings_handler = SettingsHandler()
            
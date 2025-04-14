import os
import sys

def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

directory = resource_path("options.txt")

def get_variable(name):
    with open(directory, "r", encoding="utf-8") as file:
        for line in file:
            if name in line:
                split_line = line.split("=")
                return split_line[1]
        print(f"could not find {name} in options.txt")
        return None
    

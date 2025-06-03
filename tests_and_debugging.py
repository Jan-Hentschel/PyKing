
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledText
import subprocess
import sys
import os

# from utility import resource_path
# # Path to embedded Python executable
# PYTHON_EXECUTABLE = resource_path(".\\dist\\Python313\\python.exe")

# def install_package(package_name):
#     try:
#         subprocess.run([PYTHON_EXECUTABLE, "-m", "pip", "install", package_name], check=True)
#         print(f"Package {package_name} installed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error occurred while installing {package_name}: {e}")



    

# def debugPrints():
#     root.update_idletasks()
#     print(f"screen width: {screen_width}")
#     print(f"screen height: {screen_height}")


# x = "wooow"
# print(f"Hello {x}  world" + str(123))

# print("hello")
# print("hi")
# wilhelm = Snake(0, 0, "N")
# wilhelm.move()

# paul = Snake(0,0, "N")
# paul.move()
# paul.move()
# paul.eat()
# paul.move()
# paul.turn_right()
# paul.move()
# paul.spit()

root = tk.Tk()

text = ScrolledText(root, wrap=None, hbar=True)
text.pack()
root.mainloop()
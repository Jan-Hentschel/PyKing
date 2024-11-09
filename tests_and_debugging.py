from gui import root, screen_height, screen_width
import tkinter as tk

def debugPrints():
    root.update_idletasks()
    print(f"screen width: {screen_width}")
    print(f"screen height: {screen_height}")
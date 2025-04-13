import os
import sys


from code_editor import loadIntoEditor, getStringFromEditor


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




test_file_path = resource_path("dist\\Files\\file.py")

def saveContentToFile(directory):
    with open(directory, "w", encoding="utf-8") as file:
        file.write(getStringFromEditor())


def getContentFromFile(directory):
    with open(directory, "r", encoding="utf-8") as file:
        return file.read()

def loadFile(directory):
    loadIntoEditor(getContentFromFile(directory))

def loadTestFile(event):
    loadFile(test_file_path)

def saveTestFile(event):
    saveContentToFile(test_file_path)
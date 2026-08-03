# imports go here
import pyautogui
# i dont understand why it only works with the * import
from tkinter import *
from tkinter import ttk
import json


__author__ = "Brick"

dialog_contents: str

dialog_box = Tk()

# the data taken from the file in form [title, contents]
dialog_data: tuple [str, str]

def box_appearance():
    """
    The function which contains all the contents for how the dialog boxes are to be displayed
    This can be considered a preset for how the box looks
    """
    # some column and row configuration - dont really understand this part
    dialog_box.columnconfigure(0, weight=1)
    dialog_box.rowconfigure(0, weight=1)

def box_contents():
    """
    The function which obtains all the info that goes into the dialog box
    and the stuff that affects the appearance because of the contents
    """
    # obtain the contents of the file to be used in the dialog box
    dialog_data = pull_file_contents()

    # set dialog box title
    dialog_box.title("JSON file reader")

    # set dialog box contents
    ttk.Label(dialog_box, text=f"{dialog_data}").grid(column=0, row=0, padx=30, pady=20)

def pull_file_contents() -> str:
    """
    Obtain the data from the specified file
    """
    file_data = "No JSON file found to read."

    # looks for JSON file and takes contents
    try:
        with open("contents_file.json", "r") as contents:
            file_data = json.load(contents)
        print("Obtained current wordList.json")
    except FileNotFoundError:
        print("JSON file not found, reverting to fallback contents")
        no_file_found()

    return file_data

def no_file_found():
    """
    This function triggers if there is no JSON file found to read from
    it allows the user to create a new file to read from 
    """

def main():
    """
    The main block where all other main functions are called through
    for easy access and modification of the program
    """

    # first set appearance
    box_appearance()
    # then set contents (in case of override)
    box_contents()

    dialog_box.mainloop()


if __name__ == "__main__":
    main()
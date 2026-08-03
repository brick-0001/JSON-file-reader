# imports go here
import pyautogui
# i dont understand why it only works with the * import
from tkinter import *
from tkinter import ttk
import json

"""
JSON File Reader Python Program
"""

__author__ = "Brick"

window_contents: str
user_file_input: StringVar
file_name: str = "contents_file.json"
# main window
window_box = Tk()
# file input window
window_input_box = Tk()


def box_appearance(chosen_window: Tk, window_size_x: int, window_size_y: int):
    """
    The function which contains all the contents for how the window boxes are to be displayed
    This can be considered a preset for how the box looks
    """
    # some column and row configuration - dont really understand this part
    chosen_window.columnconfigure(window_size_x, weight=1)
    chosen_window.rowconfigure(window_size_y, weight=1)


def box_contents():
    """
    The function which obtains all the info that goes into the window box
    and the stuff that affects the appearance because of the contents
    """
    # obtain the contents of the file to be used in the window box
    window_contents = pull_file_contents()

    # set window box title
    window_box.title("JSON file reader")

    # set window box contents
    ttk.Label(window_box, text=f"{window_contents}").grid(column=0, row=0, padx=30, pady=20)


def pull_file_contents() -> str:
    """
    Obtain the data from the specified file
    """
    # the "window_contents" for this function (done to prevent possible errors)
    file_data = "No JSON file found to read."

    # looks for JSON file and takes contents
    try:
        with open(f"{file_name}", "r") as contents:
            file_data = json.load(contents)
        print("Obtained JSON file")
    except FileNotFoundError:
        print("JSON file not found, reverting to fallback contents")
        no_file_found()

    return file_data


def no_file_found():
    """
    This function triggers if there is no JSON file found to read from
    it allows the user to create a new file to read from 
    """
    user_file_input = StringVar(window_input_box)

    # create new window box to let user create a file
    box_appearance(window_input_box, 0, 2)
    window_input_box.title("String input window")

    # text input appearance
    user_input = ttk.Entry(window_input_box, width=21, textvariable = user_file_input)
    user_input.grid(column=0, row=0, padx=30, pady=20)

    # file input confirmation button
    ttk.Button(window_input_box, text="Save", command=lambda: create_file(user_file_input.get())).grid(column=0, row=1)


def create_file(user_str: str):
    """
    Creates the JSON file and saves it to the correct directory location
    """
    print(f"{user_str}") # for testing purposes only - remove once working as intended

    with open(f"{file_name}", "w"):
        json.dumps(user_str)
        print(f"File contents '{user_str}' have been successfully saved in the file named '{file_name}'.")


def main():
    """
    The main block where all other main functions are called through
    for easy access and modification of the program
    """

    # first set appearance
    box_appearance(window_box, 0, 0)
    # then set contents (in case of override)
    box_contents()

    window_box.mainloop()


if __name__ == "__main__":
    main()
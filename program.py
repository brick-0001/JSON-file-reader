# imports go here
# i dont understand why it works with the * import but not importing tkinter itself
from tkinter import *
from tkinter import ttk
import json, os, pyautogui

"""
JSON File Reader Python Program
"""

__author__ = "Brick"


window_contents: str
user_file_input: StringVar
select_file_input: StringVar
file_name: str = "contents_file.json"
# window size data as [x size, y size, x offset, y offset]
window_size: tuple [int, int, int, int]

# main window
window_box = Tk()
# file input window
window_input_box = Tk()
# file selection window
window_file_select_box = Tk()

# set window box title
window_box.title("JSON file reader")
# set window box size
content_label = ttk.Label(window_box, text="")
content_label.grid(column=0, row=1, padx=30, pady=20, columnspan=2)


def get_screen_dimensions() -> tuple [int, int, int, int]:
    """
    Obtain the dimensions of the screen and set the size and location to
    1/5 screen size and 1/4 distance from top left corner
    """
    # get the monitor resolution / size
    screenWidth, screenHeight = pyautogui.size()

    window_size = int(screenWidth / 5), int(screenHeight / 5), int(screenWidth / 4), int(screenHeight / 4)

    return window_size


def file_system_stuff(file_name: str) -> str:
    """
    The file directory system, is run whenever a file is opened or created
    """
    # the name of the folder where the JSON files are stored
    folder_name: str = "JSON files"
    # create the folder IF it does not exist
    os.makedirs(folder_name, exist_ok=True)
    # stitch the file path together so the files are under the correct location
    file_path = os.path.join(folder_name, file_name)

    return file_path


def box_appearance(chosen_window: Tk, window_columns: int, window_rows: int, window_geo: tuple [int, int, int, int]):
    """
    The function which contains all the contents for how the window boxes are to be displayed
    This can be considered a preset for how the box looks
    """
    # column and row configuration (how many of each)
    chosen_window.columnconfigure(window_columns, weight=1)
    chosen_window.rowconfigure(window_rows, weight=1)

    # must be converted to a list to edit the tuple
    window_geo_list = list(window_geo)

    if (chosen_window == window_input_box):
        # sets the offset of the input window by +10%
        window_geo_list[2] = int(window_geo_list[2] * 2.0)

    if (chosen_window == window_file_select_box):
        # shrinks the window as it is not meant to be a main window
        window_geo_list[0] = int(window_geo_list[0] * 0.6)
        window_geo_list[1] = int(window_geo_list[1] * 0.5)
        # sets the offset for the window to be left of the main window
        window_geo_list[2] = int(window_geo_list[2] * 0.4)

    # converted back to a tuple
    window_geo = window_geo_list[0], window_geo_list[1], window_geo_list[2], window_geo_list[3]

    chosen_window.geometry(f"{window_geo[0]}x{window_geo[1]}+{window_geo[2]}+{window_geo[3]}")


def box_contents():
    """
    The function which obtains all the info that goes into the window box
    and the stuff that affects the appearance because of the contents
    """
    # obtain the contents of the file to be used in the window box
    window_contents = pull_file_contents()
    # 'cleans' the string by removing excess / that are automatically put in (eg. \\n -> \n)
    cleaned_contents: str = bytes(window_contents, "utf-8").decode("unicode_escape")
    
    # set window box contents (replaces what is there)
    content_label.config(text=f"{cleaned_contents}")

    # button to edit the JSON file
    edit_btn = ttk.Button(window_box, text="Edit", command=lambda: create_or_edit_file())
    edit_btn.grid(column=0, row=2, padx=10, sticky=E)
    # button to open file selection
    file_select_btn = ttk.Button(window_box, text="Select File", command=lambda: select_JSON_file())
    file_select_btn.grid(column=1, row=2, padx=10, sticky=W)

    # makes the columns split the window 50/50 down the middle no matter the size
    window_box.grid_columnconfigure(0, weight=1)
    window_box.grid_columnconfigure(1, weight=1)


def pull_file_contents() -> str:
    """
    Obtain the data from the specified file
    """
    # the "window_contents" for this function (done to prevent possible errors)
    file_data = "No JSON file found to read."

    # get file path to find file, separate line to make it easier to follow
    file_path = file_system_stuff(file_name)
    # looks for JSON file and takes contents
    try:
        with open(file_path, "r") as contents:
            file_data = json.load(contents)
            ttk.Label(window_box, text=f"{file_name} contents:").grid(column=0, row=0, columnspan=2)
        print("Obtained JSON file")
    except FileNotFoundError:
        print("JSON file not found, reverting to fallback contents.")
        ttk.Label(window_box, text=f"{file_name} not found").grid(column=0, row=0, columnspan=2)
        create_or_edit_file()
    except json.decoder.JSONDecodeError:
        print("JSON file is empty, reverting to fallback contents.")
        ttk.Label(window_box, text=f"{file_name} contents not found").grid(column=0, row=0, columnspan=2)
        create_or_edit_file()

    return file_data


def create_or_edit_file():
    """
    This function triggers if there is no JSON file found to read from
    it allows the user to create a new file to read from 
    """
    # brings the window into view if it has been withdrawn previously
    window_input_box.deiconify()

    user_file_input = StringVar(window_input_box)

    # create new window box to let user create a file
    box_appearance(window_input_box, 0, 4, get_screen_dimensions())
    window_input_box.title("String input window")

    # text input appearance
    ttk.Label(window_input_box, text="Input new text below").grid(column=0, row=0, sticky=S)
    user_input = ttk.Entry(window_input_box, width=43, textvariable = user_file_input)
    user_input.grid(column=0, row=1, padx=30, pady=20)

    # file input confirmation button
    ttk.Button(window_input_box, text="Save", command=lambda: create_file(user_file_input.get())).grid(column=0, row=2)
    # close the window without killing it so it can be brought back again
    ttk.Button(window_input_box, text="Close Window", command=lambda: window_input_box.withdraw()).grid(column=0, row=3)


def create_file(user_str: str):
    """
    Creates the JSON file and saves it to the correct directory location
    """
    # get file path
    file_path = file_system_stuff(file_name)

    with open(file_path, "w") as contents:
        json.dump(user_str, contents)
        print(f"File contents '{user_str}' have been successfully saved in the file named '{file_name}'.")

    # updates the main window contents
    box_contents()


def select_JSON_file():
    """
    Creates a window which gets the name of the JSON file the user wants to load
    """
    select_file_input = StringVar(window_file_select_box)
    window_file_select_box.title("File Selection")

    # set the window size and location 
    box_appearance(window_file_select_box, 0, 1, get_screen_dimensions())

    # sets contents of the window
    ttk.Label(window_file_select_box, text="input file name to select\n(no .json extension)").grid(column=0, row=0, sticky=N)
    file_input = ttk.Entry(window_file_select_box, width=14, textvariable = select_file_input)
    file_input.grid(column=0, row=1, padx=30, pady=20)

    # button to confirm name of file
    ttk.Button(window_file_select_box, text="Select File", command=lambda: set_file(select_file_input.get())).grid(column=0, row=2)


def set_file(file_input_name):
    """
    Sets the JSON file to the user's selected file if it is in the directory
    Creates the JSON file if it does not exist
    """
    # get file path
    file_name: str = file_input_name+".json"
    file_path = file_system_stuff(file_name)

    if (os.path.isfile(file_name)):
        # if the file currently exists
        print(f"File '{file_name}' has been located successfully")
    else:
        # if the file does not exist yet it will be created in the directory
        print(f"The file named '{file_name}' does not exist in the current directory, the file will be created")
        with open(file_path, "w") as contents:
            json.dump("", contents)
            print(f"File '{file_name}' has been created successfully")

    print(file_name)
    box_contents()

def main():
    """
    The main block where all other main functions are called through
    for easy access and modification of the program
    """
    # first set appearance (gets the monitor dimensions for sizing)
    box_appearance(window_box, 1, 2, get_screen_dimensions())
    # then set contents (in case of override)
    box_contents()

    window_box.mainloop()
    # just a little print statement informing the user that the entire program has stopped
    print("program successfully shut down")


if __name__ == "__main__":
    main()
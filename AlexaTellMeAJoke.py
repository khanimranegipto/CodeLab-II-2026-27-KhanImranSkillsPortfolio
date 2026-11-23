from tkinter import *
from PIL import *
from pathlib import *
import random

DELIMITER = "?" # used as the marker for separating the jokes from the punchline in randomJokes.txt 
FILE_PATH = Path("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt") # file path to randomJokes.txt, to be used in the load_entries function

def load_entries(path: Path, delimiter: str) -> list[tuple[str, str]]: # the function for loading the jokes from the file. 
    entries: list[tuple[str, str]] = [] 
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            first, second = line.rstrip("\r\n").split(delimiter, maxsplit=1) # separates the joke and punchline along the question mark
            entries.append((first.strip(), second.strip()))
    return entries # returns the joke and punchline now as two separate strings

class AlexaTellMeAJoke: # the central logic behind the app, builds the gui and takes the loaded entries from the previous function to be used
    def __init__(self, root: Tk, entries: list[tuple[str, str]]): # the gui settings
        self.root = root
        self.root.title("Alexa, Tell Me A Joke") 
        self.root.geometry("480x480")

        self.entries = entries
        self.current_entry: tuple[str, str] # defines the selected random entry as a tuple consisting of two strings.
        self.showing_punchline = False # for deciding whether the button should read "Show punchline" or "Next joke". by default it's false

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=True)

        center_group = Frame(main_frame)
        center_group.place(relx=0.5, rely=0.5, anchor="center")

        self.display_label = Label(center_group,text="Alexa...", justify="center", font=("Verdana", 16), wraplength=360) # header text 
        self.display_label.pack(pady=(0, 12))

        button_row = Frame(center_group) # keeps the buttons in the middle, attached to the same frame as the header text so both are in the middle of the screen.
        button_row.pack()

        self.action_button = Button(button_row,text="Tell me a joke", command=self.on_button_click) # calls the function for showing the joke and punchline. the text will change later depending on the state of self.showing_punchline.
        self.action_button.pack(side=LEFT, padx=(0, 10))
        Button(button_row, text="Quit", command=self.root.destroy).pack(side=LEFT) # button for closing the app

    def on_button_click(self):
        if not self.showing_punchline: # if the punchline is yet to be revealed
            self.current_entry = random.choice(self.entries) # selects a random line from the txt file
            self.display_label.config(text=self.current_entry[0]) # selects the first string from the tuple of each line (as defined in load_entries)
            self.action_button.config(text="Show punchline") # changes button text to "Show punchline"
            self.showing_punchline = True # flips the boolean to true
        else: # if the punchline has already been revealed
            self.display_label.config(text=self.current_entry[1]) # selects the second string from the tuple (which should be the punchline now)
            self.action_button.config(text="Next joke") # changes the button text to "Next joke"
            self.showing_punchline = False # flips the boolean back to false to return to if not self.showing_punchline

root = Tk()
root.iconbitmap('icons/alexatellmeajokeicon.ico') # icon
AlexaTellMeAJoke(root, load_entries(FILE_PATH, DELIMITER)) # calls the class for the app logic along with initialising the txt file
root.mainloop()
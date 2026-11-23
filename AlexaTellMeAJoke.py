from tkinter import *
from PIL import *
from pathlib import *
import random

DELIMITER = "?"
FILE_PATH = Path("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt")

def load_entries(path: Path, delimiter: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            first, second = line.rstrip("\r\n").split(delimiter, maxsplit=1)
            entries.append((first.strip(), second.strip()))
    return entries

class AlexaTellMeAJoke:
    def __init__(self, root: Tk, entries: list[tuple[str, str]]):
        self.root = root
        self.root.title("Alexa, Tell Me A Joke")
        self.root.geometry("480x480")

        self.entries = entries
        self.current_entry: tuple[str, str]|None = None
        self.showing_punchline = False

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=True)

        center_group = Frame(main_frame)
        center_group.place(relx=0.5, rely=0.5, anchor="center")

        self.display_label = Label(center_group,text="Alexa...", justify="center", font=("Verdana", 16), wraplength=360)
        self.display_label.pack(pady=(0, 12))

        button_row = Frame(center_group)
        button_row.pack()

        self.action_button = Button(button_row,text="Tell me a joke", command=self.on_button_click)
        self.action_button.pack(side=LEFT, padx=(0, 10))
        Button(button_row, text="Quit", command=self.root.destroy).pack(side=LEFT)

    def on_button_click(self):
        if not self.showing_punchline:
            self.current_entry = random.choice(self.entries)
            self.display_label.config(text=self.current_entry[0])
            self.action_button.config(text="Show Punchline")
            self.showing_punchline = True
        elif self.current_entry is not None:
            self.display_label.config(text=self.current_entry[1])
            self.action_button.config(text="Next Joke")
            self.showing_punchline = False

def main():
    root = Tk()
    root.iconbitmap('icons/alexatellmeajokeicon.ico')
    AlexaTellMeAJoke(root, load_entries(FILE_PATH, DELIMITER))
    root.mainloop()

main()
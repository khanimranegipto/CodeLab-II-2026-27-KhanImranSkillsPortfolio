from tkinter import *
from PIL import ImageTk, Image
def displayMenu(frame):
    frame.tkraise()
root = Tk()

root.title("Maths Quiz")
root.iconbitmap('icons/mathquizlogo2.ico')
root.config(bg="#F2F0EF")
root.geometry("848x480")

difficulty_selection = Frame(root, bg="#F2F0EF")
difficulty_selection.place(relx=0.5, rely=0.5, anchor="center")

original_img = Image.open("media/arithmeticsymbols.png")
scaling = 0.4
new_size = (int(original_img.width * scaling), int(original_img.height * scaling))

resized_img = original_img.resize(new_size, Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(resized_img)

img_banner = Label(difficulty_selection, image=img, bg="#F2F0EF", bd=0, highlightthickness=0)
img_banner.pack(pady=(0, 15))

label_title = Label(difficulty_selection, text="Welcome to the Math Quiz!", font=("Verdana", 32, "bold"), fg="black", bg="#F2F0EF")
label_title.pack(pady=(0, 15))

label_subtitle = Label(difficulty_selection, text="Select Difficulty", font=("Roboto", 18, "bold"), fg="black", bg="#F2F0EF")
label_subtitle.pack(pady=(0, 30))

difficulty_buttons = Frame(difficulty_selection, bg="#F2F0EF")
difficulty_buttons.pack()

button_style = {
    "font": ("Verdana", 12, "bold"),
    "fg": "white",
    "bg": "#32814e",
    "activebackground": "#b4befe",
    "width": 12,
    "pady": 10,
    "cursor": "hand2",
}

easy_button = Button(difficulty_buttons, text="Easy", **button_style)
easy_button.pack(side="left", padx=10)

moderate_button = Button(difficulty_buttons, text="Moderate", **button_style)
moderate_button.pack(side="left", padx=10)

advanced_button = Button(difficulty_buttons, text="Advanced", **button_style)
advanced_button.pack(side="left", padx=10)

exit_button = Button(difficulty_selection, text="Exit", font=("Verdana", 12, "bold"), fg="white", bg="#32814e", cursor="hand2", command=root.destroy, width=25)
exit_button.pack(pady=(50, 0))

root.mainloop()
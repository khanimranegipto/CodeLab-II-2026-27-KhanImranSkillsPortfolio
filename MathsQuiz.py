from tkinter import *
from PIL import ImageTk, Image
def displayMenu(frame):
    frame.tkraise()
root = Tk()

root.title("Maths Quiz")
root.config(bg="#234567")
root.geometry("848x480")

label_title = Label(root, text="Maths Quiz", font=("Roboto", 18, "bold"), bg="#234567", fg="#ffffff")
label_title.pack(anchor="center", pady=8)

frame1 = Frame(root, bg="#234567")

label = Label(frame1, text="", font=("Roboto", 10, "bold"), bg="#234567", fg="#ffffff")
label.pack(anchor="center", pady=10)
button1 = Button(frame1, text = "Enter", foreground="#ffffff", background="#234567", font=("Roboto", 12), command=lambda: displayMenu(frame2), width=20)
button1.pack(pady=10)

frame2 = Frame(root, bg="white")

label1 = Label(frame2, text="", font=("Roboto", 18, "bold"), bg="white", fg="#234567")
label1.pack(anchor="center")

button2 = Button(frame2, text = "Easy", foreground="#ffffff", background="#234567", font=("Roboto", 12), width=15)
button2.pack(pady=10, anchor="center")

button3 = Button(frame2, text = "Intermediate", foreground="#ffffff", background="#234567", font=("Roboto", 12), width=15)
button3.pack(pady=10, anchor="center")

button4 = Button(frame2, text = "Hard", foreground="#ffffff", background="#234567", font=("Roboto", 12), width=15)
button4.pack(pady=10, anchor="center")

button5 = Button(frame2, text = "Back", foreground="#ffffff", background="#234567", font=("Roboto", 12), command=lambda: displayMenu(frame1), width=5)
button5.pack(pady=35, anchor="center")

frame1.place(x=0, y=50, width=848, height=480)
frame2.place(x=0, y=50, width=848, height=480)

displayMenu(frame1)
root.mainloop()
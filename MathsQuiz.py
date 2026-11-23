from tkinter import *
from PIL import ImageTk, Image
import random

def displayMenu():
    difficulty_selection.tkraise()
def startQuiz(max_val):
    quiz.setDifficulty(max_val)
    quiz_frame.tkraise()

root = Tk()

root.title("Maths Quiz")
root.iconbitmap('icons/mathquizlogo2.ico')
root.config(bg="#DED1CA")
root.geometry("848x480")

container = Frame(root)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

quiz_frame = Frame(container)
bg_color = "#DED1CA"
quiz_frame.configure(bg=bg_color)
quiz_frame.grid(row=0, column=0, sticky="nsew")

difficulty_selection = Frame(container, bg="#DED1CA")
difficulty_selection.grid(row=0, column=0, sticky="nsew")

inner = Frame(difficulty_selection, bg="#DED1CA")
inner.place(relx=0.5, rely=0.5, anchor="center")

original_img = Image.open("media/arithmeticsymbols.png")
scaling = 0.4
new_size = (int(original_img.width * scaling), int(original_img.height * scaling))

resized_img = original_img.resize(new_size, Image.Resampling.LANCZOS) # uses the lanczos algorithm to resize the image while retaining quality
img = ImageTk.PhotoImage(resized_img)
img_banner = Label(inner, image=img, bg="#DED1CA", bd=0, highlightthickness=0)
img_banner.pack(pady=(0, 15))

label_title = Label(inner, text="Welcome to the Math Quiz!", font=("Verdana", 32, "bold"), fg="black", bg="#DED1CA") 
label_title.pack(pady=(0, 15))

label_subtitle = Label(inner, text="Select Difficulty", font=("Roboto", 18, "bold"), fg="black", bg="#DED1CA")
label_subtitle.pack(pady=(0, 30))

difficulty_buttons = Frame(inner, bg="#DED1CA")
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

easy_button = Button(difficulty_buttons, text="Easy", command=lambda: startQuiz(9), **button_style)
easy_button.pack(side="left", padx=10)

moderate_button = Button(difficulty_buttons, text="Moderate", command=lambda: startQuiz(99), **button_style)
moderate_button.pack(side="left", padx=10)

advanced_button = Button(difficulty_buttons, text="Advanced", command=lambda: startQuiz(9999), **button_style)
advanced_button.pack(side="left", padx=10)

exit_button = Button(inner, text="Exit", font=("Verdana", 12, "bold"), fg="white", bg="#32814e", cursor="hand2", command=root.destroy, width=25)
exit_button.pack(pady=(50, 0))

for f in (difficulty_selection,quiz_frame):
    f.grid(row=0, column=0, sticky="nsew")

class MathsQuiz(Frame): # the logic of the quiz
    def __init__(self, parent, total=10, max_val=9, **kwargs):
        bg = kwargs.get("bg") or kwargs.get("background") or "#DED1CA"
        super().__init__(parent, **{**kwargs, "bg": bg})
        self.configure(bg=bg)
        font_md = ("Roboto", 12)

        self.total, self.max_val = total, max_val
        self.max_score = self.total * 10
        self.q_num = self.score = self.answer = 0
        self.attempts = 0
        self.max_attempts = 2

        self.problem = Label(self, bg=bg, font=("Roboto", 26, "bold"), pady=14)
        self.problem.pack()

        self.quiz_controls = Frame(self, bg=bg)
        self.quiz_controls.pack()

        self.status = Label(self.quiz_controls, bg=bg, font=("Roboto", 12))
        self.status.pack(pady=(0, 8))

        self.entry = Entry(self.quiz_controls, font=("Roboto", 16), width=10, justify="center")
        self.entry.pack()
        self.entry.bind("<Return>", self.submit)

        self.btn = Button(self.quiz_controls, text="Enter", font=font_md, command=self.submit)
        self.btn.pack(pady=8)

        self.feedback = Label(self, bg=bg, font=("Roboto", 12))
        self.feedback.pack()

        self.end_btn_row = Frame(self, bg=bg)
        Button(self.end_btn_row, text="Play Again?", font=font_md, command=self.restart).pack(side="left", padx=(0, 8))
        Button(self.end_btn_row, text="Return to Menu", font=font_md, command=displayMenu).pack(side="left")

        self.nextQuestion()

    def randomInt(self):
        return random.randint(0, self.max_val), random.randint(0, self.max_val)

    def decideOperation(self):
        return random.choice(["+", "-"])

    def computeAnswer(self, a, b, op):
        return a + b if op == "+" else a - b

    def isCorrect(self, guess):
        if guess == self.answer:
            points = 10 if self.attempts == 0 else 5
            self.score += points
            if self.attempts == 0:
                msg = "Correct!" 
            else:
                msg = "Correct, second time's the charm!"
            self.feedback.config(text=msg)
            self.nextQuestion()
            return True

        self.attempts += 1
        if self.attempts < self.max_attempts:
            self.feedback.config(text="Answer was wrong. Try again one more time.")
            self.entry.delete(0, END)
            self.entry.focus_set()
            return False

        self.feedback.config(text=f"Wrong answer, but keep going.")
        self.nextQuestion()
        return False

    def displayResults(self):
        full_score = (self.score / self.max_score) * 100 if self.max_score else 0
        grade = (
            "A" if full_score > 90 else
            "B" if full_score > 75 else
            "C" if full_score > 60 else
            "D" if full_score > 40 else
            "F"
        )
        self.quiz_controls.pack_forget()
        self.problem.config(text=f"Quiz Complete! Score: {self.score}/{self.max_score} (Grade: {grade})")
        self.feedback.config(text="")
        self.end_btn_row.pack(pady=(4, 10))

    def setDifficulty(self, max_val):
        self.max_val = max_val
        self.restart()

    def nextQuestion(self): # formulating the next question
        if self.q_num >= self.total: # calls displayResults instead if the quiz has already finished
            self.displayResults()
            return

        a, b = self.randomInt() # calls the function to decide the values for each operand depending on difficulty selected
        op = self.decideOperation() #calls the function to decide the operation used, whether it is plus or minus
        self.answer = self.computeAnswer(a, b, op) # generates the correct answer key for the quiz to refer the user's answer to
        self.attempts = 0 # tracks the number of attempts the user has made at answering a question, to be added on when the user makes a mistake.
        self.q_num += 1 # adds 1 to the q_num variable, which tracks the number of questions the user has answered. will be referred to to terminate the quiz when above 10

        self.status.config(text=f"Question {self.q_num} of {self.total}  /  Score: {self.score}/{self.max_score}") # displays the question number, total number of questions and the score so far out of 100
        self.problem.config(text=f"{a} {op} {b} = ?") # the question
        self.entry.delete(0, END)  # clears the entry box for the new question
        self.entry.focus_set()

    def submit(self):
        try:
            guess = int(self.entry.get().strip())
        except ValueError:
            self.feedback.config(text="Please enter a whole number.")
            self.entry.delete(0, END)
            self.entry.focus_set()
            return
        self.isCorrect(guess)

    def restart(self):
        self.end_btn_row.pack_forget()
        self.q_num = self.score = self.attempts = 0
        self.feedback.config(text="")
        self.entry.config(state="normal")
        self.quiz_controls.pack(before=self.feedback)
        self.nextQuestion()

quiz = MathsQuiz(quiz_frame, max_val=9, bg=bg_color)
quiz.place(relx=0.5, rely=0.5, anchor="center")
displayMenu()
root.mainloop()
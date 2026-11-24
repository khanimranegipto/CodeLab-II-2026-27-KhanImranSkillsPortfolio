from tkinter import *
from PIL import ImageTk, Image
import random

def displayMenu(): # for displaying the difficulty selection menu
    difficulty_selection.tkraise()
def startQuiz(max_val): # brings the quiz frame to the top. max_val will be from the selected mode of difficulty
    quiz.setDifficulty(max_val)
    quiz_frame.tkraise()

root = Tk()
root.title("Maths Quiz")
root.iconbitmap('icons/mathquizlogo2.ico') # icon
root.config(bg="#DED1CA") # main bg
root.geometry("848x480") # default dimensions of the gui

container = Frame(root) # for holding the frames
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

quiz_frame = Frame(container) # for holding the quiz itself
bg = "#DED1CA"
quiz_frame.configure(bg=bg)
quiz_frame.grid(row=0, column=0, sticky="nsew")

difficulty_selection = Frame(container, bg="#DED1CA") 
difficulty_selection.grid(row=0, column=0, sticky="nsew")

inner = Frame(difficulty_selection, bg="#DED1CA")
inner.place(relx=0.5, rely=0.5, anchor="center")

original_img = Image.open("media/arithmeticsymbols.png") # resizing this image soon
scaling = 0.4
new_size = (int(original_img.width * scaling), int(original_img.height * scaling))

resized_img = original_img.resize(new_size, Image.Resampling.LANCZOS) # using the lanczos algorithm to resize the image while retaining quality
img = ImageTk.PhotoImage(resized_img)
img_banner = Label(inner, image=img, bg="#DED1CA", bd=0, highlightthickness=0) # bd and highlight thickness are used here to remove the default borders tk tends to add to images
img_banner.pack(pady=(0, 15))

label_title = Label(inner, text="Welcome to the Math Quiz!", font=("Verdana", 32, "bold"), fg="black", bg="#DED1CA") # introductory header text
label_title.pack(pady=(0, 15))

label_subtitle = Label(inner, text="Select Difficulty", font=("Roboto", 18, "bold"), fg="black", bg="#DED1CA")
label_subtitle.pack(pady=(0, 30))

difficulty_buttons = Frame(inner, bg="#DED1CA") # the button row frame for the difficulty selection
difficulty_buttons.pack()

button_style = { # dictionary for the style of all difficulty selection buttons.
    "font": ("Verdana", 12, "bold"),
    "fg": "white",
    "bg": "#32814e",
    "activebackground": "#b4befe",
    "width": 12,
    "pady": 10,
    "cursor": "hand2",
}

easy_button = Button(difficulty_buttons, text="Easy", command=lambda: startQuiz(9), **button_style) # button that starts the easy quiz. calls the startQuiz function and tells the quiz to load only one digit operands.
easy_button.pack(side="left", padx=10)

moderate_button = Button(difficulty_buttons, text="Moderate", command=lambda: startQuiz(99), **button_style) # medium quiz, this time two digit operands.
moderate_button.pack(side="left", padx=10)

advanced_button = Button(difficulty_buttons, text="Advanced", command=lambda: startQuiz(9999), **button_style) # hard quiz, four digit operands.
advanced_button.pack(side="left", padx=10)

exit_button = Button(inner, text="Exit", font=("Verdana", 12, "bold"), fg="white", bg="#32814e", cursor="hand2", command=root.destroy, width=25) # button for exiting the quiz
exit_button.pack(pady=(50, 0))

class MathsQuiz(Frame): # the logic of the quiz
    def __init__(self, parent, total=10, max_val=9, **kwargs): # the overall functionality of the quiz
        bg = ("#DED1CA")
        super().__init__(parent, **{**kwargs, "bg": bg}) # a fix suggested by google gemini for problems with bg colours during the quiz
        font = ("Roboto", 12)

        self.total, self.max_val = total, max_val 
        self.max_score = self.total * 10 # total questions x 10 = 100, the max score
        self.q_num = self.score = self.answer = 0 # initialises the variables to start with 0 by default
        self.attempts = 0 # starts at 0 by default, intended to increase by 1 with every attempt at a question
        self.max_attempts = 2 # max number of allowed attempts per question

        self.problem = Label(self, bg=bg, font=("Roboto", 26, "bold"), pady=14) # the math problem text
        self.problem.pack()

        self.quiz_controls = Frame(self, bg=bg) # frame for handling the entry box, quiz status, and the enter answer button
        self.quiz_controls.pack()

        self.status = Label(self.quiz_controls, bg=bg, font=("Roboto", 12)) # text intended to display the question # and score
        self.status.pack(pady=(0, 8))

        self.entry = Entry(self.quiz_controls, font=("Roboto", 16), width=10, justify="center") # entry field for the answer
        self.entry.pack()
        self.entry.bind("<Return>", self.submit)

        self.btn = Button(self.quiz_controls, text="Enter", font=font, command=self.submit) # button for submission of the answer
        self.btn.pack(pady=8)

        self.feedback = Label(self, bg=bg, font=("Roboto", 12)) # text to be displayed in response to the user's actions (i.e. getting an answer correct)
        self.feedback.pack()

        self.end_btn_row = Frame(self, bg=bg) # button row intended to appear at the end of the quiz
        Button(self.end_btn_row, text="Play Again?", font=font, command=self.restart).pack(side="left", padx=(0, 8))
        Button(self.end_btn_row, text="Return to Menu", font=font, command=displayMenu).pack(side="left")

        self.nextQuestion() # calls the function to refresh the question after the user has finished answering it

    def randomInt(self): # picks a random integer up to the total amount of digits in accordance with the selected difficulty
        return random.randint(0, self.max_val), random.randint(0, self.max_val)

    def decideOperation(self): # decides between making the question an addition or subtraction problem
        return random.choice(["+", "-"])

    def computeAnswer(self, a, b, op): # creates the answer key by which the app would refer to when checking the user's answer
        return a + b if op == "+" else a - b

    def isCorrect(self, guess): # if the user's answer is correct
        if guess == self.answer: 
            points = 10 if self.attempts == 0 else 5
            self.score += points
            if self.attempts == 0: # if correct on first attempt
                msg = "Correct!" 
            else: # if correct on second attempt
                msg = "Correct, second time's the charm!"
            self.feedback.config(text=msg) # displays the appropriate message according to # of attempts
            self.nextQuestion() # proceeds to the next question
            return True

        self.attempts += 1 # updates number of attempts
        if self.attempts < self.max_attempts: # if the user still fails to answer correctly the first try
            self.feedback.config(text="Answer was wrong. Try again one more time.")
            self.entry.delete(0, END) # clears the entry box
            self.entry.focus_set()
            return False
        else: # if the user still fails to answer correctly the second time
            self.feedback.config(text=f"Wrong answer, but keep going.")
        self.nextQuestion() # displays the next question
        return False

    def displayResults(self): # at the end of the quiz
        full_score = (self.score / self.max_score) * 100 if self.max_score else 0 #  calculates full score
        grade = ( # defines the grade the user would get based on their full_score
            "A" if full_score > 90 else
            "B" if full_score > 75 else
            "C" if full_score > 60 else
            "D" if full_score > 40 else
            "F"
        )
        self.quiz_controls.pack_forget() # removes the quiz ui
        self.problem.config(text=f"Quiz Complete! Score: {self.score}/{self.max_score} (Grade: {grade})") # quiz completion and score text
        self.feedback.config(text="") # clears the feedback
        self.end_btn_row.pack(pady=(4, 10)) # buttons for retrying and returning to the difficulty selection screen moved up

    def setDifficulty(self, max_val): # to be called by startQuiz, in reference to the difficulty selected, of which max_val would be based upon.
        self.max_val = max_val
        self.restart() # calls to reset the quiz to now rely on the new max_val in respect to the difficulty selected

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

    def submit(self): # handles validity of user submission
        try:
            guess = int(self.entry.get().strip())
        except ValueError:
            self.feedback.config(text="Please enter a whole number.")
            self.entry.delete(0, END)
            self.entry.focus_set()
            return
        self.isCorrect(guess) # passes the user's answer to isCorrect if guess is valid

    def restart(self): # clears everything and starts fresh
        self.end_btn_row.pack_forget()
        self.q_num = self.score = self.attempts = 0
        self.feedback.config(text="")
        self.entry.config(state="normal")
        self.quiz_controls.pack(before=self.feedback)
        self.nextQuestion()

quiz = MathsQuiz(quiz_frame) # placing the quiz within the quiz frame
quiz.place(relx=0.5, rely=0.5, anchor="center")
displayMenu() # places the menu at top
root.mainloop() 
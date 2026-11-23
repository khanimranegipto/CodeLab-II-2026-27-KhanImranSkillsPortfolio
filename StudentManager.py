from tkinter import *
from tkinter import messagebox

root = Tk()
FILE = "Assessment 1 - Skills Portfolio/A1 - Resources/studentMarks.txt" # the reference file

class StudentManagementSystem: # the logic
    def __init__(self, root: Tk, file_path: str = FILE): # app configuration
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("650x450")
        self.file_path = file_path
        self.records: list[dict] = []

        self.gui()
        self.load_records(show_warning=False)

    def gui(self):
        menu = LabelFrame(self.root, text="Menu", padx=8, pady=6)
        menu.pack(fill="x", padx=10, pady=4)

        row1 = Frame(menu)
        row1.pack(fill="x")
        for text, cmd in [
            ("1. Display All Data", self.display_all),
            ("2. Highest Marks", lambda: self.show_extreme(True)),
            ("3. Lowest Marks", lambda: self.show_extreme(False)),
        ]:
            Button(row1, text=text, width=16, command=cmd).pack(side="left", padx=(0, 8))

        row2 = Frame(menu)
        row2.pack(fill="x", pady=(6, 0))
        Label(row2, text="View Specific Student (ID or Name):").pack(side="left")
        Button(row2, text="Clear Output", command=lambda: self.show("")).pack(side="right")

        self.search_var = StringVar()
        entry = Entry(row2, textvariable=self.search_var, width=24)
        entry.pack(side="left", padx=6)
        entry.bind("<Return>", lambda: self.search_student())

        Button(row2, text="Search Record", command=self.search_student).pack(side="left")

        output_frame = LabelFrame(self.root, text="Output", padx=8, pady=6)
        output_frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        self.output = Text(output_frame, wrap=WORD, font=("Roboto", 10), state=DISABLED)
        self.output.pack(fill="both", expand=True)

    def show(self, text: str) -> None:
        self.output.config(state=NORMAL)
        self.output.delete("1.0", END)
        self.output.insert(END, text)
        self.output.config(state=DISABLED)

    @staticmethod
    def _num(val: float) -> str:
        return str(int(val)) if val.is_integer() else f"{val:.2f}"

    def _fmt(self, r: dict) -> str:
        course_marks = ", ".join(self._num(s) for s in r["course_marks"])
        return f"{r['name']} - #{r['id']} - Coursework Marks: [{course_marks}] - Examination Marks: {self._num(r['exam_marks'])}"

    def load_records(self, show_warning: bool = True) -> None:
        self.records = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines[1:]:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) == 6:
                try:
                    rec_id, name, s1, s2, s3, full = parts
                    self.records.append({
                        "id": rec_id,
                        "name": name,
                        "course_marks": [float(s1), float(s2), float(s3)],
                        "exam_marks": float(full)
                    })
                except ValueError:
                    pass

    def display_all(self) -> None:
        lines = [f"{i}. {self._fmt(r)}" for i, r in enumerate(self.records, 1)]
        sep = "-" * 72
        self.show(f"Total number of students: {len(self.records)}\n{sep}\n" + "\n".join(lines) + "\n")

    def search_student(self) -> None:
        q = self.search_var.get().strip().lower()
        if not q:
            messagebox.showinfo("Input Needed", "Please enter a student's Name or ID to search.")
            return
        matches = [r for r in self.records if r["id"].lower() == q or r["name"].lower() == q] or [r for r in self.records if q in r["id"].lower() or q in r["name"].lower()]
        if not matches:
            self.show(f"No record found matching '{self.search_var.get().strip()}'.\n")
            return
        body = "\n".join(self._fmt(r) for r in matches)
        self.show(f"Search Results For '{self.search_var.get().strip()}' ({len(matches)} match(es))\n" + "-" * 72 + f"\n{body}\n")

    def show_extreme(self, highest: bool) -> None:
        if not self.records:
            self.show("No records available.")
            return
        target = (max if highest else min)(r["exam_marks"] for r in self.records)
        found = [r for r in self.records if r["exam_marks"] == target]
        label = "HIGHEST" if highest else "LOWEST"
        body = "\n".join(self._fmt(r) for r in found)
        self.show(f"{label} overall marks: {self._num(target)} ({len(found)} student(s))\n" + "-" * 72 + f"\n{body}\n")

root.iconbitmap("icons/studentmanagericon.ico")
StudentManagementSystem(root, FILE)
root.mainloop()
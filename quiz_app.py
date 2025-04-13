# let user choose between 
# 1. An administrator interface for managing quiz content (password-protected)
# 2. A user interface for taking quizzes

import tkinter as tk
from tkinter import messagebox, simpledialog

# --- Simulated Question Database ---
quiz_data = {
    "What is the capital of France?": "Paris",
    "What is 2 + 2?": "4",
}

ADMIN_PASSWORD = "admin123"

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")
        self.main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to the Quiz App!", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Admin Interface", command=self.admin_login, width=25).pack(pady=10)
        tk.Button(self.root, text="User Interface", command=self.user_interface, width=25).pack(pady=10)

    # -------- Admin Login --------
    def admin_login(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Admin Password", font=("Arial", 14)).pack(pady=20)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(self.root, text="Login", command=self.check_password).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def check_password(self):
        if self.password_entry.get() == ADMIN_PASSWORD:
            self.admin_dashboard()
        else:
            messagebox.showerror("Access Denied", "Incorrect password!")

    # -------- Admin Dashboard --------
    def admin_dashboard(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Add New Question", command=self.add_question_form).pack(pady=5)
        tk.Button(self.root, text="View All Questions", command=self.view_questions).pack(pady=5)
        tk.Button(self.root, text="Modify/Delete Questions", command=self.modify_questions).pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=20)

    # -------- Add Question --------
    def add_question_form(self):
        self.clear_window()
        tk.Label(self.root, text="Add New Question", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Question:").pack()
        self.new_question = tk.Entry(self.root, width=50)
        self.new_question.pack(pady=5)

        tk.Label(self.root, text="Answer:").pack()
        self.new_answer = tk.Entry(self.root, width=50)
        self.new_answer.pack(pady=5)

        tk.Button(self.root, text="Add Question", command=self.add_question).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

    def add_question(self):
        question = self.new_question.get().strip()
        answer = self.new_answer.get().strip()

        if question and answer:
            quiz_data[question] = answer
            messagebox.showinfo("Success", "Question added.")
            self.new_question.delete(0, tk.END)
            self.new_answer.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both question and answer.")

    # -------- View Questions --------
    def view_questions(self):
        self.clear_window()
        tk.Label(self.root, text="All Questions", font=("Arial", 14)).pack(pady=10)

        for q, a in quiz_data.items():
            tk.Label(self.root, text=f"Q: {q}\nA: {a}", justify="left", wraplength=400).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=10)

    # -------- Modify/Delete Questions --------
    def modify_questions(self):
        self.clear_window()
        tk.Label(self.root, text="Modify or Delete Questions", font=("Arial", 14)).pack(pady=10)

        self.question_listbox = tk.Listbox(self.root, width=60, height=10)
        for q in quiz_data.keys():
            self.question_listbox.insert(tk.END, q)
        self.question_listbox.pack(pady=10)

        tk.Button(self.root, text="Edit Selected", command=self.edit_selected_question).pack()
        tk.Button(self.root, text="Delete Selected", command=self.delete_selected_question).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=10)

    def edit_selected_question(self):
        selected = self.question_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a question to edit.")
            return

        question = self.question_listbox.get(selected)
        answer = quiz_data[question]

        new_question = simpledialog.askstring("Edit Question", "Enter new question:", initialvalue=question)
        new_answer = simpledialog.askstring("Edit Answer", "Enter new answer:", initialvalue=answer)

        if new_question and new_answer:
            del quiz_data[question]
            quiz_data[new_question] = new_answer
            messagebox.showinfo("Updated", "Question updated.")
            self.modify_questions()

    def delete_selected_question(self):
        selected = self.question_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a question to delete.")
            return

        question = self.question_listbox.get(selected)
        if messagebox.askyesno("Confirm Delete", f"Delete the question:\n\n{question}?"):
            del quiz_data[question]
            self.modify_questions()

    # -------- User Interface --------
    def user_interface(self):
        self.clear_window()
        self.questions = list(quiz_data.items())
        self.current_question_index = 0
        self.score = 0
        self.ask_question()

    def ask_question(self):
        if self.current_question_index < len(self.questions):
            question, _ = self.questions[self.current_question_index]
            tk.Label(self.root, text=f"Question {self.current_question_index + 1}: {question}", wraplength=400, font=("Arial", 12)).pack(pady=20)

            self.user_answer = tk.Entry(self.root, width=40)
            self.user_answer.pack(pady=10)

            tk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=10)
        else:
            messagebox.showinfo("Quiz Complete", f"Your score: {self.score}/{len(self.questions)}")
            self.main_menu()

    def check_answer(self):
        user_input = self.user_answer.get().strip()
        correct_answer = self.questions[self.current_question_index][1]

        if user_input.lower() == correct_answer.lower():
            self.score += 1

        self.current_question_index += 1
        self.clear_window()
        self.ask_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
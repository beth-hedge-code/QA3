# let user choose between 
# 1. An administrator interface for managing quiz content (password-protected)
# 2. A user interface for taking quizzes

import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Function to get questions from database
def get_questions_from_database(course_name):
    database_name = f"{course_name.replace(' ', '_')}.db"
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT question_text, option_A, option_B, option_C, option_D, correct_answer FROM questions")
    questions = cursor.fetchall()
    conn.close()

    question_list = []
    for q in questions:
        question_list.append({
            'question_text': q[0],
            'option_A': q[1],
            'option_B': q[2],
            'option_C': q[3],
            'option_D': q[4],
            'correct_answer': q[5]
        })
    return question_list

# Admin Login

def check_password():
    if password_entry.get() == "admin123":
        login_window.destroy()
        admin_interface()
    else:
        messagebox.showerror("Error", "Incorrect password")

# Admin Features

def add_question_gui():
    def submit_question():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return

        data = (question_entry.get(), option_a.get(), option_b.get(), option_c.get(), option_d.get(), correct_answer.get())
        if not all(data):
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return

        db_name = f"{course.replace(' ', '_')}.db"
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question_text TEXT,
                            option_A TEXT,
                            option_B TEXT,
                            option_C TEXT,
                            option_D TEXT,
                            correct_answer TEXT)''')
        cursor.execute("""INSERT INTO questions
                       (question_text, option_A, option_B, option_C, option_D, correct_answer)
                        VALUES (?, ?, ?, ?, ?, ?)""", data)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Question added!")
        window.destroy()

    window = Toplevel(root)
    window.title("Add New Question")

    courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
               "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]

    Label(window, text="Select Course:").pack()
    course_combobox = ttk.Combobox(window, values=courses, width=50, state="readonly")
    course_combobox.pack()

    Label(window, text="Question:").pack()
    question_entry = Entry(window, width=100)
    question_entry.pack()

    option_a = Entry(window, width=50)
    option_b = Entry(window, width=50)
    option_c = Entry(window, width=50)
    option_d = Entry(window, width=50)
    correct_answer = Entry(window, width=5)

    for lbl, widget in zip(["Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"], [option_a, option_b, option_c, option_d, correct_answer]):
        Label(window, text=lbl).pack()
        widget.pack()

    Button(window, text="Submit Question", command=submit_question).pack(pady=10)

def view_questions_gui():
    def load_questions():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return

        try:
            questions = get_questions_from_database(course)
            questions_listbox.delete(0, END)
            for i, q in enumerate(questions, 1):
                display_text = (
                    f"{i}. {q['question_text']}\n"
                    f"    A. {q['option_A']}  B. {q['option_B']}  "
                    f"C. {q['option_C']}  D. {q['option_D']}  "
                    f"(Answer: {q['correct_answer']})\n"
                )
                questions_listbox.insert(END, display_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    window = Toplevel(root)
    window.title("View Questions")
    window.geometry("800x500")

    Label(window, text="Select Course:", font=("Arial", 12)).pack(pady=10)

    courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
               "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]

    course_combobox = ttk.Combobox(window, values=courses, width=50, state="readonly")
    course_combobox.pack()

    Button(window, text="Load Questions", command=load_questions).pack(pady=10)

    questions_listbox = Listbox(window, width=110, height=20, font=("Courier", 10))
    questions_listbox.pack(pady=10)

def modify_question_gui():
    def load_questions():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return
        try:
            nonlocal db_name
            db_name = f"{course.replace(' ', '_')}.db"
            nonlocal questions
            questions = get_questions_from_database(course)
            questions_listbox.delete(0, END)
            for i, q in enumerate(questions, 1):
                questions_listbox.insert(END, f"{i}. {q['question_text']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def modify_selected():
        idx = questions_listbox.curselection()
        if not idx:
            messagebox.showwarning("No Selection", "Please select a question to modify.")
            return

        selected_question = questions[idx[0]]
        modify_window = Toplevel(root)
        modify_window.title("Modify Question")

        Label(modify_window, text="Question:").pack()
        question_entry = Entry(modify_window, width=100)
        question_entry.insert(0, selected_question['question_text'])
        question_entry.pack()

        option_a = Entry(modify_window, width=50)
        option_b = Entry(modify_window, width=50)
        option_c = Entry(modify_window, width=50)
        option_d = Entry(modify_window, width=50)
        correct_answer = Entry(modify_window, width=5)

        for lbl, widget in zip(["Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"],
                               [option_a, option_b, option_c, option_d, correct_answer]):
            Label(modify_window, text=lbl).pack()
            widget.pack()

        def view_questions_gui():
            def load_questions():
                course = course_combobox.get()
                if not course:
                    messagebox.showwarning("No Course Selected", "Please select a course.")
                    return

                try:
                    questions = get_questions_from_database(course)
                    questions_listbox.delete(0, END)
                    for i, q in enumerate(questions, 1):
                        display_text = (
                            f"{i}. {q['question_text']}\n"
                            f"    A. {q['option_A']}  B. {q['option_B']}  "
                            f"C. {q['option_C']}  D. {q['option_D']}  "
                            f"(Answer: {q['correct_answer']})\n"
                        )
                        questions_listbox.insert(END, display_text)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            window = Toplevel(root)
            window.title("View Questions")
            window.geometry("800x500")

            Label(window, text="Select Course:", font=("Arial", 12)).pack(pady=10)

            courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
                    "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]

            course_combobox = ttk.Combobox(window, values=courses, width=50, state="readonly")
            course_combobox.pack()

            Button(window, text="Load Questions", command=load_questions).pack(pady=10)

            questions_listbox = Listbox(window, width=110, height=20, font=("Courier", 10))
            questions_listbox.pack(pady=10)

        def submit_modifications():
            data = (question_entry.get(), option_a.get(), option_b.get(), option_c.get(), option_d.get(), correct_answer.get())
            if not all(data):
                messagebox.showwarning("Missing Info", "Please fill all fields.")
                return

            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("""UPDATE questions SET question_text = ?, option_A = ?, option_B = ?, option_C = ?, 
                              option_D = ?, correct_answer = ? WHERE question_text = ?""",
                           (*data, selected_question['question_text']))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Question modified!")
            modify_window.destroy()
            load_questions()

        Button(modify_window, text="Submit Modifications", command=submit_modifications).pack(pady=10)

    window = Toplevel(root)
    window.title("Modify Questions")
    window.geometry("700x500")

    db_name = ""
    questions = []

    Label(window, text="Select Course:").pack()
    courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
               "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]

    course_combobox = ttk.Combobox(window, values=courses, width=50, state="readonly")
    course_combobox.pack()

    Button(window, text="Load Questions", command=load_questions).pack(pady=5)

    questions_listbox = Listbox(window, width=100, height=20)
    questions_listbox.pack(pady=10)
    Button(window, text="Modify Selected Question", command=modify_selected).pack(pady=5)

def delete_question_gui():
    def load_questions():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return
        try:
            nonlocal db_name
            db_name = f"{course.replace(' ', '_')}.db"
            nonlocal questions
            questions = get_questions_from_database(course)
            questions_listbox.delete(0, END)
            for i, q in enumerate(questions, 1):
                questions_listbox.insert(END, f"{i}. {q['question_text']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected():
        idx = questions_listbox.curselection()
        if not idx:
            return
        question_text = questions[idx[0]]['question_text']
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE question_text = ?", (question_text,))
        conn.commit()
        conn.close()
        load_questions()
        messagebox.showinfo("Deleted", "Question deleted successfully.")

    window = Toplevel(root)
    window.title("Delete Questions")
    window.geometry("700x500")

    db_name = ""
    questions = []

    Label(window, text="Select Course:").pack()
    courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
               "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]

    course_combobox = ttk.Combobox(window, values=courses, width=50, state="readonly")
    course_combobox.pack()

    Button(window, text="Load Questions", command=load_questions).pack(pady=5)

    questions_listbox = Listbox(window, width=100, height=20)
    questions_listbox.pack(pady=10)
    Button(window, text="Delete Selected Question", command=delete_selected).pack(pady=5)

# Admin Interface
def admin_interface():
    window = Toplevel(root)
    window.title("Admin Dashboard")
    window.geometry("300x300")

    Button(window, text="Add Question", width=25, command=add_question_gui).pack(pady=10)
    Button(window, text="View Questions", width=25, command=view_questions_gui).pack(pady=10)
    Button(window, text="Modify Questions", width=25, command=modify_question_gui).pack(pady=10)
    Button(window, text="Delete Questions", width=25, command=delete_question_gui).pack(pady=10)

def start_quiz():
    def next_question():
        nonlocal index, score
        if index < len(questions):
            q = questions[index]
            question_label.config(text=q['question_text'])
            var.set(None)
            for i, opt in enumerate(['A', 'B', 'C', 'D']):
                options[i].config(text=f"{opt}. {q[f'option_{opt}']}")
        else:
            messagebox.showinfo("Quiz Finished", f"Your score: {score}/{len(questions)}")
            quiz_window.destroy()

    def submit_answer():
        nonlocal index, score
        selected = var.get()
        if selected:
            if selected == questions[index]['correct_answer']:
                score += 1
            index += 1
            next_question()
        else:
            messagebox.showwarning("No Selection", "Please select an answer.")

    def load_questions_and_start():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course", "Select a course to start quiz.")
            return

        nonlocal questions
        questions = get_questions_from_database(course)
        if not questions:
            messagebox.showinfo("No Questions", "No questions found for this course.")
            return
        quiz_selector.destroy()
        next_question()

    quiz_selector = Toplevel(root)
    quiz_selector.title("Choose Course")
    Label(quiz_selector, text="Select Course to Begin Quiz").pack(pady=10)

    courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
               "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]
    course_combobox = ttk.Combobox(quiz_selector, values=courses, width=50, state="readonly")
    course_combobox.pack(pady=10)

    Button(quiz_selector, text="Start Quiz", command=load_questions_and_start).pack(pady=10)

    quiz_window = Toplevel(root)
    quiz_window.title("Quiz")
    quiz_window.geometry("700x400")

    question_label = Label(quiz_window, text="", wraplength=600, font=("Arial", 12))
    question_label.pack(pady=20)

    var = StringVar()
    options = [Radiobutton(quiz_window, text="", variable=var, value=opt) for opt in ["A", "B", "C", "D"]]
    for opt in options:
        opt.pack(anchor=W)

    Button(quiz_window, text="Submit", command=submit_answer).pack(pady=20)

    questions = []
    index = 0
    score = 0


# Root Window
root = Tk()
root.title("Quiz Application")
root.geometry("400x300")

Label(root, text="Select Mode", font=("Arial", 14)).pack(pady=30)
Button(root, text="Administrator", width=20, command=lambda: show_password_prompt()).pack(pady=10)
Button(root, text="Take a Quiz", width=20, command=start_quiz).pack(pady=10)

# Password Prompt
def show_password_prompt():
    global login_window, password_entry
    login_window = Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x150")

    Label(login_window, text="Enter Admin Password:").pack(pady=10)
    password_entry = Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    Button(login_window, text="Login", command=check_password).pack(pady=10)

root.mainloop()

# let user choose between 
# 1. An administrator interface for managing quiz content (password-protected)
# 2. A user interface for taking quizzes

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ======== Database Utilities ========
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

# ======== Admin Panel ========
def view_questions_gui():
    def load_questions():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return

        try:
            questions = get_questions_from_database(course)
            questions_listbox.delete(0, tk.END)
            for i, q in enumerate(questions, 1):
                display_text = (
                    f"{i}. {q['question_text']}\n"
                    f"    A. {q['option_A']}  B. {q['option_B']}  "
                    f"C. {q['option_C']}  D. {q['option_D']}  "
                    f"(Answer: {q['correct_answer']})\n"
                )
                questions_listbox.insert(tk.END, display_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    window = tk.Toplevel(root)
    window.title("View Questions")
    window.geometry("800x500")

    tk.Label(window, text="Select Course:", font=("Arial", 12)).pack(pady=10)

    courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
               "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]
    
    course_combobox = ttk.Combobox(window, values=courses, width=50, state="readonly")
    course_combobox.pack()

    tk.Button(window, text="Load Questions", command=load_questions).pack(pady=10)

    questions_listbox = tk.Listbox(window, width=110, height=20, font=("Courier", 10))
    questions_listbox.pack(pady=10)

def open_admin_interface():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("400x200")
    tk.Button(admin_window, text="View Questions", command=view_questions_gui, font=("Arial", 14)).pack(pady=50)

def check_credentials():
    if password_entry.get() == "admin123":
        login_window.destroy()
        open_admin_interface()
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")

def open_login_window():
    global login_window, password_entry
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x150")
    tk.Label(login_window, text="Enter Admin Password:").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    tk.Button(login_window, text="Login", command=check_credentials).pack(pady=10)

# ======== Quiz for User ========
def take_quiz():
    def start_quiz():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return

        try:
            questions = get_questions_from_database(course)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not questions:
            messagebox.showinfo("No Questions", "No questions found for this course.")
            return

        quiz_window = tk.Toplevel(root)
        quiz_window.title("Take Quiz")
        quiz_window.geometry("700x400")

        index = {'current': 0}
        user_answers = []

        def show_question():
            q = questions[index['current']]
            question_label.config(text=f"{index['current'] + 1}. {q['question_text']}")
            var.set(None)
            option_a.config(text="A. " + q['option_A'], value='A')
            option_b.config(text="B. " + q['option_B'], value='B')
            option_c.config(text="C. " + q['option_C'], value='C')
            option_d.config(text="D. " + q['option_D'], value='D')

        def next_question():
            answer = var.get()
            user_answers.append(answer)
            index['current'] += 1

            if index['current'] < len(questions):
                show_question()
            else:
                score = sum(
                    1 for i, q in enumerate(questions)
                    if user_answers[i] == q['correct_answer']
                )
                messagebox.showinfo("Quiz Complete", f"You scored {score} out of {len(questions)}")
                quiz_window.destroy()

        question_label = tk.Label(quiz_window, text="", wraplength=650, font=("Arial", 12))
        question_label.pack(pady=20)

        var = tk.StringVar()

        option_a = tk.Radiobutton(quiz_window, text="", variable=var, value='A', font=("Arial", 11))
        option_a.pack(anchor="w")

        option_b = tk.Radiobutton(quiz_window, text="", variable=var, value='B', font=("Arial", 11))
        option_b.pack(anchor="w")

        option_c = tk.Radiobutton(quiz_window, text="", variable=var, value='C', font=("Arial", 11))
        option_c.pack(anchor="w")

        option_d = tk.Radiobutton(quiz_window, text="", variable=var, value='D', font=("Arial", 11))
        option_d.pack(anchor="w")

        tk.Button(quiz_window, text="Next", command=next_question).pack(pady=20)

        show_question()

    quiz_setup_window = tk.Toplevel(root)
    quiz_setup_window.title("Take Quiz")
    quiz_setup_window.geometry("400x200")

    tk.Label(quiz_setup_window, text="Select Course:", font=("Arial", 12)).pack(pady=10)
    courses = ["Principles of Managerial Finance", "Mgmt Organizational Behavior", 
               "Business Applications Develop", "Business Database Mgmt", "Principles of Marketing"]

    course_combobox = ttk.Combobox(quiz_setup_window, values=courses, width=40, state="readonly")
    course_combobox.pack(pady=10)

    tk.Button(quiz_setup_window, text="Start Quiz", command=start_quiz).pack(pady=20)

# ======== Main Menu ========
root = tk.Tk()
root.title("Quiz App")
root.geometry("400x250")

tk.Label(root, text="Choose Interface", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="Administrator", command=open_login_window, width=20, font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Take Quiz", command=take_quiz, width=20, font=("Arial", 12)).pack(pady=10)

root.mainloop()
# let user choose between 
# 1. An administrator interface for managing quiz content (password-protected)
# 2. A user interface for taking quizzes

import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def get_questions_from_database(course_name):
    # Now, each course corresponds to a separate database file
    database_name = f"{course_name.replace(' ', '_')}.db"  # Format the course name as the database file name
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

def view_questions_gui():
    def load_questions():
        course = course_combobox.get()
        if not course:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return

        db_course_name = course.replace(" ", "_")
        try:
            questions = get_questions_from_database(db_course_name)
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

# ======================
# Main window to test it
# ======================

root = Tk()
root.title("Admin Panel")
root.geometry("400x200")

Button(root, text="View Questions", command=view_questions_gui, font=("Arial", 14)).pack(pady=50)

root.mainloop()
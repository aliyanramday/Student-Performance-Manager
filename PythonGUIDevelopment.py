import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk
# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="StudentPerformanceDB"
)
cursor = db.cursor()

class StudentPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Management System")
        self.root.geometry("450x350")

        self.root.state('zoomed')
        
        self.login_screen()
    
    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="System Login", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(frame, width=30)
        self.email_entry.grid(row=1, column=1)

        tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1)

        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(button_frame, text="Login", width=10, command=self.validate_login).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Exit", width=10, command=self.root.quit).grid(row=0, column=1, padx=5)

    def validate_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT * FROM SystemAccessors WHERE Email=%s AND Password=%s", (email, password))
        result = cursor.fetchone()

        if result:
            self.service_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    def service_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#C0C0C0")

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#C0C0C0")
        frame.pack(expand=True, fill="both")

        header = tk.Label(frame, text="Service Request", font=("Arial", 12, "bold"), bg="#A0A0A0", fg="black", padx=100, pady=5)
        header.pack(fill="x")

        tk.Label(frame, text="What do you want to access?", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(pady=10)

        self.service_choice = tk.StringVar()
        self.service_choice.set(None)

        options = [("Add student record", "student"),
                   ("Add A System Accessor", "accessor"),
                   ("Students Performance", "performance")]

        for text, value in options:
            tk.Radiobutton(frame, text=text, variable=self.service_choice, value=value, font=("Arial", 10), bg="#C0C0C0").pack(anchor="w", padx=50)

        button_frame = tk.Frame(frame, bg="#C0C0C0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", command=self.process_service).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.login_screen).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=2, padx=5)

    def process_service(self):
        selection = self.service_choice.get()
        if selection == "student":
            self.add_student_record()
        elif selection == "accessor":
            self.add_system_accessor()
        elif selection == "performance":
            self.student_performance_menu()
        else:
            messagebox.showwarning("Selection Required", "Please select an option.")

    def add_student_record(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text="Add Student Record", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(frame, text="Student's First Name:").pack()
        self.first_name = tk.Entry(frame)
        self.first_name.pack()

        tk.Label(frame, text="Student's Middle Name (Optional):").pack()
        self.middle_name = tk.Entry(frame)
        self.middle_name.pack()

        tk.Label(frame, text="Student's Passport Size Photo:").pack()
        self.photo_path = tk.Entry(frame, width=30)
        self.photo_path.pack()
        tk.Button(frame, text="Upload", command=self.upload_photo).pack()
        
        tk.Label(frame, text="\nNote: The student's email will be generated automatically based on the Institution's policy.", font=("Arial", 10, "italic"), fg="blue").pack()

        tk.Button(frame, text="Submit", command=self.save_student).pack(pady=10)
        tk.Button(frame, text="Back", command=self.service_menu).pack()

    def upload_photo(self):
        file_path = filedialog.askopenfilename()
        self.photo_path.delete(0, tk.END)
        self.photo_path.insert(0, file_path)

    def save_student(self):
        first_name = self.first_name.get()
        middle_name = self.middle_name.get()
        photo = self.photo_path.get()

        cursor.execute("INSERT INTO Students (FirstName, MiddleName, Photo) VALUES (%s, %s, %s)", 
                       (first_name, middle_name, photo))
        db.commit()
        messagebox.showinfo("Success", "Student Record Added")
        self.service_menu()
    def add_system_accessor(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text="Add System Accessor", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(frame, text="Email").pack()
        email = tk.Entry(frame)
        email.pack()

        tk.Label(frame, text="Password").pack()
        password = tk.Entry(frame, show="*")
        password.pack()

        def submit():
            cursor.execute("INSERT INTO SystemAccessors (Email, Password) VALUES (%s, %s)", 
                           (email.get(), password.get()))
            db.commit()
            messagebox.showinfo("Success", "System Accessor Added Successfully")
            self.service_menu()

        tk.Button(frame, text="Submit", command=submit).pack(pady=10)
        tk.Button(frame, text="Back", command=self.service_menu).pack()
    def student_performance_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#C0C0C0")

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#C0C0C0")
        frame.pack(expand=True, fill="both")

        header = tk.Label(frame, text="Students Performance", font=("Arial", 12, "bold"), 
                          bg="#A0A0A0", fg="black", padx=100, pady=5)
        header.pack(fill="x")

        tk.Label(frame, text="What do you want to do?", font=("Arial", 10, "bold"), 
                 bg="#C0C0C0").pack(pady=10)

        self.performance_choice = tk.StringVar()
        self.performance_choice.set(None)

        options = [
            ("Add student's grades", "add_grades"),
            ("Access students' performance report", "performance_report")
        ]

        for text, value in options:
            tk.Radiobutton(frame, text=text, variable=self.performance_choice, value=value, 
                           font=("Arial", 10), bg="#C0C0C0").pack(anchor="w", padx=50)

        button_frame = tk.Frame(frame, bg="#C0C0C0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", 
                  command=self.process_performance_request).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", 
                  command=self.service_menu).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", 
                  command=self.root.quit).grid(row=0, column=2, padx=5)
    
    def process_performance_request(self):
        selection = self.performance_choice.get()
        if selection == "add_grades":
            self.add_grades()
        elif selection == "performance_report":
            self.performance_report()
        else:
            messagebox.showwarning("Selection Required", "Please select an option.")
    def add_grades(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#C0C0C0")

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#C0C0C0")
        frame.pack(expand=True, fill="both")

        header = tk.Label(frame, text="Adding Student's Grades", font=("Arial", 12, "bold"), 
                          bg="#A0A0A0", fg="black", padx=100, pady=5)
        header.pack(fill="x")

        tk.Label(frame, text="Student ID:", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20, pady=5)
        self.student_id_entry = tk.Entry(frame, width=30)
        self.student_id_entry.pack(padx=20, pady=5)

        tk.Label(frame, text="Select Term:", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20, pady=5)
        self.term_var = tk.StringVar()
        self.term_var.set("Term 1")
        term_dropdown = ttk.Combobox(frame, textvariable=self.term_var, values=["Term 1", "Term 2", "Term 3"])
        term_dropdown.pack(padx=20, pady=5)

        cursor.execute("SELECT SubjectCode FROM Subjects")
        subjects = cursor.fetchall()
        self.subject_entries = {}

        for subject in subjects:
            subject_code = subject[0]
            tk.Label(frame, text=f"{subject_code}:", font=("Arial", 10), bg="#C0C0C0").pack(anchor="w", padx=20, pady=3)
            entry = tk.Entry(frame, width=10)
            entry.pack(padx=20, pady=3)
            self.subject_entries[subject_code] = entry

        tk.Label(frame, text="\nNote: Grades are in percentages", font=("Arial", 9, "italic"), fg="blue", bg="#C0C0C0").pack(pady=5)

        button_frame = tk.Frame(frame, bg="#C0C0C0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", command=self.save_grades).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="CLEAR", width=12, relief="ridge", command=self.clear_grade_entries).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.student_performance_menu).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=3, padx=5)

    def clear_grade_entries(self):
        self.student_id_entry.delete(0, tk.END)
        for entry in self.subject_entries.values():
            entry.delete(0, tk.END)
    def save_grades(self):
        student_id = self.student_id_entry.get()
        term = self.term_var.get()

        term_number = int(term.split(" ")[1])  # Ensure term is stored as an INT

        if not student_id:
            messagebox.showwarning("Missing Information", "Please enter a Student ID.")
            return

        for subject_code, entry in self.subject_entries.items():
            grade = entry.get()
            if grade:
                try:
                    cursor.execute("INSERT INTO StudentGrades (StudentID, SubjectCode, Term, Grade) VALUES (%s, %s, %s, %s)", 
                                   (student_id, subject_code, term_number, float(grade)))
                    db.commit()
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error saving grades: {str(e)}")
                    return

        messagebox.showinfo("Success", "Grades added successfully!")
        self.student_performance_menu()
    
        
    def performance_report(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#C0C0C0")
        frame.pack(expand=True, fill="both")

        header = tk.Label(frame, text="Students Performance", font=("Arial", 12, "bold"), bg="#A0A0A0", fg="black", padx=100, pady=5)
        header.pack(fill="x")

        tk.Label(frame, text="What do you want to do?", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(pady=10)

        self.report_choice = tk.StringVar()
        self.report_choice.set(None)

        options = [("Analysis of students' Performances", "analysis"),
                   ("Access students' performance report", "report")]

        for text, value in options:
            tk.Radiobutton(frame, text=text, variable=self.report_choice, value=value, font=("Arial", 10), bg="#C0C0C0").pack(anchor="w", padx=50)

        button_frame = tk.Frame(frame, bg="#C0C0C0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", command=self.process_report_request).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.student_performance_menu).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=2, padx=5)

    def process_report_request(self):
        selection = self.report_choice.get()
        if selection == "analysis":
            self.performance_analysis()
        elif selection == "report":
            self.access_student_performance()
        else:
            messagebox.showwarning("Selection Required", "Please select an option.")
    def performance_report(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text="Students Performance", font=("Arial", 14, "bold")).pack(pady=10)

        self.performance_choice = tk.StringVar()
        self.performance_choice.set(None)

        options = [
            ("Analysis of students' Performances", "analysis"),
            ("Access students' performance report", "report")
        ]

        for text, value in options:
            tk.Radiobutton(frame, text=text, variable=self.performance_choice, value=value, font=("Arial", 10)).pack(anchor="w", padx=50)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", command=self.process_report_request).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.student_performance_menu).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=2, padx=5)

    def process_report_request(self):
        selection = self.performance_choice.get()
        if selection == "analysis":
            self.performance_analysis()
        elif selection == "report":
            self.show_performance_report_selection()
        else:
            messagebox.showwarning("Selection Required", "Please select an option.")

    def performance_analysis(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text="Performance Analysis", font=("Arial", 14, "bold")).pack(pady=10)

        self.analysis_choice = tk.StringVar()
        self.analysis_choice.set(None)

        self.term_choice = tk.StringVar()
        self.term_choice.set("Term 1")

        self.year_choice = tk.StringVar()
        self.year_choice.set("Yearly")

        tk.Label(frame, text="What do you want to do?", font=("Arial", 10, "bold")).pack(anchor="w", padx=50)

        tk.Radiobutton(frame, text="Individual Student Performance Analysis", variable=self.analysis_choice, value="individual", font=("Arial", 10)).pack(anchor="w", padx=50)
        term_dropdown = ttk.Combobox(frame, textvariable=self.term_choice, values=["Term 1", "Term 2", "Term 3"], state="readonly")
        term_dropdown.pack(anchor="w", padx=120)

        tk.Radiobutton(frame, text="Class Performance Analysis", variable=self.analysis_choice, value="class", font=("Arial", 10)).pack(anchor="w", padx=50)
        year_dropdown = ttk.Combobox(frame, textvariable=self.year_choice, values=["Yearly", "Term 1", "Term 2", "Term 3"], state="readonly")
        year_dropdown.pack(anchor="w", padx=120)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", command=self.display_chart_options).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.performance_report).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=2, padx=5)

    def display_chart_options(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True)

        analysis_type = self.analysis_choice.get()
        if analysis_type == "class":
            heading_text = "Yearly Class Performance Analysis"
        else:
            heading_text = "Term-wise Student Performance Analysis"

        tk.Label(frame, text=heading_text, font=("Arial", 14, "bold")).pack(pady=10)

        self.chart_choice = tk.StringVar()
        self.chart_choice.set("line")

        tk.Label(frame, text="Display:", font=("Arial", 10, "bold")).pack(anchor="w", padx=50)

        tk.Radiobutton(frame, text="A bar chart", variable=self.chart_choice, value="bar", font=("Arial", 10)).pack(anchor="w", padx=50)
        tk.Radiobutton(frame, text="A line plot", variable=self.chart_choice, value="line", font=("Arial", 10)).pack(anchor="w", padx=50)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", command=self.display_performance_chart).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.performance_analysis).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=2, padx=5)

    def display_performance_chart(self):
        chart_type = self.chart_choice.get()
        term_selected = self.term_choice.get()

        try:
            term_number = int(term_selected.split(" ")[1])  
        except ValueError:
            messagebox.showerror("Invalid Selection", "Please select a valid term.")
            return

        cursor.execute("SELECT SubjectCode, AVG(Grade) FROM StudentGrades WHERE Term=%s GROUP BY SubjectCode", (term_number,))
        data = cursor.fetchall()

        subjects = [row[0] for row in data]
        grades = [row[1] for row in data]

        if not subjects or not grades:
            messagebox.showerror("No Data", "No data available for the selected term.")
            return

        plt.figure(figsize=(8, 5))
        plt.title(f"{term_selected} {chart_type.capitalize()} Performance Analysis")

        if chart_type == "bar":
            plt.bar(subjects, grades, color='blue')
            plt.ylabel("Average Grades (%)")
        else:
            plt.plot(subjects, grades, marker='o', linestyle='-', color='red')
            plt.ylabel("Average Grades (%)")

        plt.xlabel("Subjects")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
    def show_performance_report_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#C0C0C0")
        frame.pack(expand=True, fill="both")

        header = tk.Label(frame, text="Students Performance Report", font=("Arial", 12, "bold"), 
                          bg="#A0A0A0", fg="black", padx=100, pady=5)
        header.pack(fill="x")

        tk.Label(frame, text="What information do you want to access?", font=("Arial", 10, "bold"), 
                 bg="#C0C0C0").pack(pady=10)

        self.performance_type = tk.StringVar()
        self.performance_type.set("individual")  

        self.term_var_individual = tk.StringVar()
        self.term_var_individual.set("Term 1")
    
        self.term_var_class = tk.StringVar()
        self.term_var_class.set("Term 1")

        ind_frame = tk.Frame(frame, bg="#C0C0C0")
        ind_frame.pack(anchor="w", padx=50)

        tk.Radiobutton(ind_frame, text="Individual students performance", variable=self.performance_type, 
                       value="individual", font=("Arial", 10), bg="#C0C0C0").grid(row=0, column=0)

        ttk.Combobox(ind_frame, textvariable=self.term_var_individual, values=["Term 1", "Term 2", "Term 3"], 
                     state="readonly").grid(row=0, column=1)

        class_frame = tk.Frame(frame, bg="#C0C0C0")
        class_frame.pack(anchor="w", padx=50)

        tk.Radiobutton(class_frame, text="Class Performance", variable=self.performance_type, 
                       value="class", font=("Arial", 10), bg="#C0C0C0").grid(row=0, column=0)

        ttk.Combobox(class_frame, textvariable=self.term_var_class, values=["Term 1", "Term 2", "Term 3"], 
                     state="readonly").grid(row=0, column=1)

        button_frame = tk.Frame(frame, bg="#C0C0C0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", 
                  command=self.process_performance_selection).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", 
                  command=self.student_performance_menu).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", 
                  command=self.root.quit).grid(row=0, column=2, padx=5)

    def process_performance_selection(self):
        selection = self.performance_type.get()
        term = self.term_var_individual.get() if selection == "individual" else self.term_var_class.get()

        if selection == "individual":
            self.show_individual_performance_input(term)
        elif selection == "class":
            self.show_class_performance(term)
        else:
            messagebox.showwarning("Selection Required", "Please select an option.")
    def show_individual_performance_input(self, term):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text=f"{term} Students Assessment", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(frame, text="Student ID:").pack()
        self.student_id_entry = tk.Entry(frame, width=30)
        self.student_id_entry.pack()

        self.display_average_var = tk.BooleanVar(value=True)

        cursor.execute("SELECT SubjectCode FROM Subjects")
        subjects = cursor.fetchall()
        self.subject_vars = {}

        for subject in subjects:
            subject_code = subject[0]
            self.subject_vars[subject_code] = tk.BooleanVar(value=True)
            tk.Checkbutton(frame, text=subject_code, variable=self.subject_vars[subject_code]).pack(anchor="w")

        tk.Checkbutton(frame, text="Display the average as well", variable=self.display_average_var).pack(anchor="w")

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="SUBMIT", width=12, relief="ridge", 
                  command=lambda: self.display_student_report(term)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", 
                  command=self.show_performance_report_selection).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", 
                  command=self.root.quit).grid(row=0, column=2, padx=5)
    from PIL import Image, ImageTk

    def display_student_report(self, term):
        student_id = self.student_id_entry.get()

        if not student_id:
            messagebox.showwarning("Missing Information", "Please enter a Student ID.")
            return

        cursor.execute("SELECT FirstName, MiddleName, Photo FROM Students WHERE StudentID=%s", (student_id,))
        student_data = cursor.fetchone()

        if not student_data:
            messagebox.showerror("Error", "No student found with the given ID.")
            return

        first_name, middle_name, photo_path = student_data

        cursor.execute("SELECT SubjectCode, Grade FROM StudentGrades WHERE StudentID=%s AND Term=%s", (student_id, term.split(" ")[1]))
        grades = cursor.fetchall()

        if not grades:
            messagebox.showerror("No Data", "No grades found for the selected student in this term.")
            return

        if self.display_average_var.get() and grades:
            avg_grade = sum(g[1] for g in grades) / len(grades)
        else:
            avg_grade = None

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#C0C0C0")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text=f"{term} Students Assessment", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(frame, text="Student ID:", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20)
        tk.Label(frame, text=student_id, font=("Arial", 10), bg="#C0C0C0").pack(anchor="w", padx=40)

        tk.Label(frame, text="Student First Name:", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20)
        tk.Label(frame, text=first_name, font=("Arial", 10), bg="#C0C0C0").pack(anchor="w", padx=40)

        if middle_name:
            tk.Label(frame, text="Student Middle Name (optional):", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20)
            tk.Label(frame, text=middle_name, font=("Arial", 10), bg="#C0C0C0").pack(anchor="w", padx=40)

        if photo_path:
            try:
                image = Image.open(photo_path)
                image = image.resize((100, 100))  
                photo = ImageTk.PhotoImage(image)

                photo_label = tk.Label(frame, image=photo, bg="#C0C0C0")
                photo_label.image = photo  
                photo_label.pack(anchor="e", padx=20, pady=10)
            except Exception as e:
                messagebox.showerror("Image Error", f"Could not load student image: {str(e)}")

        for subject, grade in grades:
            tk.Label(frame, text=f"{subject}: {grade} %", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20)

        if avg_grade is not None:
            tk.Label(frame, text=f"Average: {round(avg_grade, 2)} %", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20)

        button_frame = tk.Frame(frame, bg="#C0C0C0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="<< HOME", width=12, relief="ridge", command=self.student_performance_menu).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.show_individual_performance_input).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=2, padx=5)
    def show_class_performance(self, term):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#C0C0C0")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text=f"{term} Class Performance", font=("Arial", 14, "bold")).pack(pady=10)

        cursor.execute("SELECT SubjectCode, AVG(Grade) FROM StudentGrades WHERE Term=%s GROUP BY SubjectCode", (term.split(" ")[1],))
        class_performance_data = cursor.fetchall()

        if not class_performance_data:
            messagebox.showerror("No Data", "No performance data available for this class.")
            return

        for subject, avg_grade in class_performance_data:
            tk.Label(frame, text=f"{subject}: {round(avg_grade, 2)} %", font=("Arial", 10, "bold"), bg="#C0C0C0").pack(anchor="w", padx=20)

        button_frame = tk.Frame(frame, bg="#C0C0C0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="<< BACK", width=12, relief="ridge", command=self.performance_report).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="EXIT", width=12, relief="ridge", command=self.root.quit).grid(row=0, column=1, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPerformanceApp(root)
    root.mainloop()

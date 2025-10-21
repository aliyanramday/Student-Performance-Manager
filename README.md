# 🎓 Student Performance Management System (Python + MySQL)

A GUI-based student performance management tool built using **Python (Tkinter)** and **MySQL**.  
It allows teachers or administrators to record, update, and analyze student results.

---

## 🧠 Overview
This system provides:
- A Tkinter-based graphical interface  
- Database storage for students, grades, and subjects  
- Data retrieval and report generation  
- Easy connection to MySQL (via XAMPP or local server)

---

## ⚙️ Technologies Used
- Python 3.x  
- Tkinter GUI  
- MySQL (XAMPP / phpMyAdmin)  
- pandas & matplotlib (for analytics and charting)

---

## 📂 Files Included
- `PythonGUIDevelopment.py` → main GUI application  
- `CREATE DATABASE StudentPerformanceDB.sql` → database schema  
- `ARamday-Term2_Task1CS1OOP.docx` → documentation / report  

---

## 💡 How to Run

1. **Start MySQL**
   - Open **XAMPP Control Panel** and start **MySQL**.

2. **Create the database**
   - In **phpMyAdmin**, open the SQL tab and run:
     ```sql
     SOURCE CREATE DATABASE StudentPerformanceDB.sql;
     ```

3. **Run the Python program**
   - In your terminal (Mac) or command prompt (Windows), navigate to the folder containing the file and run:
     ```bash
     python3 PythonGUIDevelopment.py
     ```
     *(Use `python` instead of `python3` on Windows if needed.)*

4. The GUI window will open — from here you can add, view, or update student performance records.

---

Developed by **Aliyan Ali Ramday**  
OnCampus Aston – IYO BSc (Hons) Computer Science

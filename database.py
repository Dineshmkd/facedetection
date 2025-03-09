import sqlite3

def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, roll_number TEXT, image_path TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, date TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def add_student(name, roll_number, image_path):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, roll_number, image_path) VALUES (?, ?, ?)", (name, roll_number, image_path))
    conn.commit()
    conn.close()

def mark_attendance(student_id):
    from datetime import datetime
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, datetime.now().date(), "Present"))
    conn.commit()
    conn.close()

def get_student_id_by_name(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE roll_number =" +student_id)
    row = cursor.fetchone()
    conn.commit()
    conn.close()

    return row


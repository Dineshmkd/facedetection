import sqlite3

def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, roll_number TEXT, image_path TEXT)''')
    conn.commit()
    conn.close()

def add_student(name, roll_number, image_path):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, roll_number, image_path) VALUES (?, ?, ?)", (name, roll_number, image_path))
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


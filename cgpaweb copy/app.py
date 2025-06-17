from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create SQLite table
def init_db():
    conn = sqlite3.connect('cgpa.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cgpa_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        reg_no TEXT NOT NULL,
        semester INTEGER NOT NULL,
        prev_cgpa REAL,
        sgpa REAL,
        cgpa REAL,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name'].strip()
        reg_no = request.form['reg_no'].strip()
        semester = int(request.form['semester'])

        if not name or not reg_no.isdigit() or len(reg_no) != 12:
            return render_template('index.html', error="Please enter a valid 12-digit Registration Number and Name.")

        prev_cgpa = float(request.form['prev_cgpa']) if semester > 1 else 0.0
        num_subjects = int(request.form['num_subjects'])

        total_points = 0
        total_credits = 0

        grade_map = {'H': 10, 'S': 9, 'A': 8, 'B': 7, 'C': 6, 'F': 0, 'RA': 0, 'K': 0}

        for i in range(1, num_subjects + 1):
            grade = request.form.get(f'grade_{i}', '').strip().upper()
            credit = float(request.form.get(f'credit_{i}', 0))

            if grade not in grade_map:
                return render_template('index.html', error=f"Invalid grade '{grade}' for Subject {i}.")
            point = grade_map[grade]
            total_points += point * credit
            total_credits += credit

        sgpa = round(total_points / total_credits, 2) if total_credits else 0.0
        if semester == 1:
            cgpa = sgpa
        else:
            cgpa = round(((prev_cgpa * (semester - 1)) + sgpa) / semester, 2)

        # Save to database
        conn = sqlite3.connect('cgpa.db')
        c = conn.cursor()
        c.execute("INSERT INTO cgpa_records (name, reg_no, semester, prev_cgpa, sgpa, cgpa, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (name, reg_no, semester, prev_cgpa, sgpa, cgpa, datetime.now().isoformat()))
        conn.commit()
        conn.close()

        return render_template('result.html', name=name, reg_no=reg_no, semester=semester, sgpa=sgpa, cgpa=cgpa)

    return render_template('index.html', error=None)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

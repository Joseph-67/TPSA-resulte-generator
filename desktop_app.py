import csv
import importlib
import io
import math
import os
import sqlite3
import sys
from datetime import datetime
from contextlib import contextmanager, redirect_stdout

import customtkinter as ctk
from openpyxl import load_workbook
from tkinter import BooleanVar, filedialog, messagebox
from werkzeug.security import check_password_hash, generate_password_hash
from grade import generate_grade_workbook
from classes.js.subject import js1_subjects, js2_and_js3_subjects
from classes.ss.subject import (
    ss1_subjects,
    ss2_and_ss3_art_subjects,
    ss2_and_ss3_science_subjects,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.environ.get("TPSA_DATABASE", os.path.join(BASE_DIR, "tpsa.db"))
OUTPUT_DIR = os.path.join(BASE_DIR, "final_3term_results")
SECONDARY_STUDENT_MODULES = (
    "classes.js.js1D",
    "classes.js.js1G",
    "classes.js.js2D",
    "classes.js.js2G",
    "classes.js.js3",
    "classes.ss.SS1D",
    "classes.ss.ss1",
    "classes.ss.ss1art",
    "classes.ss.ss1science",
    "classes.ss.ss2art",
    "classes.ss.ss2d",
    "classes.ss.ss2g",
    "classes.ss.ss2science",
    "classes.ss.ss3",
)


def load_secondary_students():
    students = []
    with redirect_stdout(io.StringIO()):
        for module_name in SECONDARY_STUDENT_MODULES:
            module = importlib.import_module(module_name)
            students.extend(module.students_data)
    return students


def secondary_subjects_for(class_name):
    if class_name.startswith("JS 1"):
        return js1_subjects
    if class_name.startswith(("JS 2", "JS 3")):
        return js2_and_js3_subjects
    if class_name.startswith("SS 1"):
        return ss1_subjects
    if class_name.endswith("Art"):
        return ss2_and_ss3_art_subjects
    if class_name.endswith("Science"):
        return ss2_and_ss3_science_subjects
    if class_name.startswith(("SS 2", "SS 3")):
        return list(dict.fromkeys(
            ss2_and_ss3_art_subjects + ss2_and_ss3_science_subjects
        ))
    raise ValueError(f"No secondary subjects are configured for {class_name}.")


@contextmanager
def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                section TEXT NOT NULL DEFAULT 'General',
                active INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class_id INTEGER,
                active INTEGER NOT NULL DEFAULT 1,
                UNIQUE(name, class_id),
                FOREIGN KEY(class_id) REFERENCES classes(id)
            );
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                admission_no TEXT UNIQUE NOT NULL,
                class_id INTEGER NOT NULL,
                sex TEXT DEFAULT 'Unknown',
                session TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY(class_id) REFERENCES classes(id)
            );
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                term INTEGER NOT NULL CHECK(term BETWEEN 1 AND 3),
                ca1 REAL DEFAULT 0,
                ca2 REAL DEFAULT 0,
                ca3 REAL DEFAULT 0,
                exam REAL DEFAULT 0,
                UNIQUE(student_id, subject_id, term),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            );
            CREATE TABLE IF NOT EXISTS assessment_columns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                max_score REAL NOT NULL,
                sort_order INTEGER NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                UNIQUE(class_id, name),
                FOREIGN KEY(class_id) REFERENCES classes(id)
            );
            CREATE TABLE IF NOT EXISTS result_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                term INTEGER NOT NULL CHECK(term BETWEEN 1 AND 3),
                assessment_id INTEGER NOT NULL,
                score REAL NOT NULL DEFAULT 0,
                UNIQUE(student_id, subject_id, term, assessment_id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id),
                FOREIGN KEY(assessment_id) REFERENCES assessment_columns(id)
            );
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
        """)
        if not db.execute("SELECT 1 FROM admins WHERE username='admin'").fetchone():
            db.execute(
                "INSERT INTO admins(username, password_hash, created_at) VALUES (?, ?, ?)",
                ("admin", generate_password_hash("admin123"), datetime.now().isoformat())
            )
        for key, value in {
            "session": "2026/2027",
            "school_name": "TOPSTEPS ACADEMY",
            "resumption_date": "2026-09-01",
            "closing_date": "2027-07-01",
            "ca1_max": "20",
            "ca2_max": "20",
            "ca3_max": "20",
            "exam_max": "40",
            "grade_a_min": "75",
            "grade_b_min": "60",
            "grade_c_min": "50",
            "grade_d_min": "45",
            "grade_e_min": "40",
            "report_field_subject_average": "1",
            "report_field_first_term": "1",
            "report_field_second_term": "1",
            "report_field_cumulative": "1",
            "report_field_grade": "1",
            "report_field_position": "1",
            "report_field_remark": "1",
        }.items():
            db.execute("INSERT OR IGNORE INTO config(key, value) VALUES (?, ?)", (key, value))
        admin_columns = {
            row["name"] for row in db.execute("PRAGMA table_info(admins)").fetchall()
        }
        if "is_active" not in admin_columns:
            db.execute("ALTER TABLE admins ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1")

        classes = [
            ("Pre-Nursery One", "General"),
            ("Grade One Diamond", "Diamond"),
            ("Grade One Gold", "Gold"),
            ("Grade Two Gold", "Gold"),
            ("Grade Two Diamond", "Diamond"),
            ("Grade Three Diamond", "Diamond"),
            ("Grade Three Gold", "Gold"),
            ("Grade Four", "General"),
            ("Grade Five", "General"),
        ]
        legacy_pre_nursery = db.execute(
            "SELECT id FROM classes WHERE name='Pre-Nursery Ode'"
        ).fetchone()
        pre_nursery_one = db.execute(
            "SELECT id FROM classes WHERE name='Pre-Nursery One'"
        ).fetchone()
        if legacy_pre_nursery and not pre_nursery_one:
            db.execute(
                "UPDATE classes SET name='Pre-Nursery One' WHERE id=?",
                (legacy_pre_nursery["id"],),
            )
        legacy_grade_one = db.execute(
            "SELECT id FROM classes WHERE name='Grade One'"
        ).fetchone()
        grade_one_diamond = db.execute(
            "SELECT id FROM classes WHERE name='Grade One Diamond'"
        ).fetchone()
        if legacy_grade_one and not grade_one_diamond:
            db.execute(
                "UPDATE classes SET name='Grade One Diamond', section='Diamond' "
                "WHERE id=?",
                (legacy_grade_one["id"],),
            )
        for name, section in classes:
            db.execute("INSERT OR IGNORE INTO classes(name, section) VALUES (?, ?)", (name, section))

        assessment_defaults = (
            ("CA1", float(db.execute("SELECT value FROM config WHERE key='ca1_max'").fetchone()[0])),
            ("CA2", float(db.execute("SELECT value FROM config WHERE key='ca2_max'").fetchone()[0])),
            ("CA3", float(db.execute("SELECT value FROM config WHERE key='ca3_max'").fetchone()[0])),
            ("EXAM", float(db.execute("SELECT value FROM config WHERE key='exam_max'").fetchone()[0])),
        )
        for class_row in db.execute("SELECT id FROM classes").fetchall():
            for sort_order, (name, max_score) in enumerate(assessment_defaults, 1):
                db.execute(
                    "INSERT OR IGNORE INTO assessment_columns(class_id, name, max_score, sort_order) "
                    "VALUES (?, ?, ?, ?)",
                    (class_row["id"], name, max_score, sort_order)
                )

        for name, legacy_column in (
            ("CA1", "ca1"), ("CA2", "ca2"), ("CA3", "ca3"), ("EXAM", "exam")
        ):
            for class_row in db.execute("SELECT id FROM classes").fetchall():
                assessment = db.execute(
                    "SELECT id FROM assessment_columns WHERE class_id=? AND name=?",
                    (class_row["id"], name)
                ).fetchone()
                if assessment:
                    db.execute(f"""
                        INSERT OR IGNORE INTO result_scores
                            (student_id, subject_id, term, assessment_id, score)
                        SELECT r.student_id, r.subject_id, r.term, ?, r.{legacy_column}
                        FROM results r
                        JOIN students st ON st.id=r.student_id
                        WHERE st.class_id=?
                    """, (assessment["id"], class_row["id"]))

        primary = [
            "English Studies", "Mathematics", "Phonics", "Basic Science & Technology",
            "Pre-Vocational Studies", "Social & Citizenship Studies", "French",
            "Basic Digital Literacy", "Cultural & Creative Art",
            "Physical & Health Education", "CRS/IRS", "Hausa", "History", "Handwriting"
        ]
        nursery_subjects = [
            "Literacy", "Numeracy", "Phonics", "Basic Science", "Health Habit",
            "Social Habit", "Civic Education", "Personal Development",
            "Handwriting", "Creativity", "Rhymes", "CRS",
        ]
        pre_nursery_subjects = [
            "Literacy", "Numeracy", "Handwriting", "Health Habit",
            "Social Habit", "Science Skill", "Rhymes",
        ]
        lower_primary = [name for name in primary if name not in (
            "Pre-Vocational Studies", "Basic Digital Literacy"
        )]
        nursery_subjects_migrated = db.execute(
            "SELECT value FROM config WHERE key='nursery_subjects_migrated'"
        ).fetchone()
        migrate_nursery_subjects = not nursery_subjects_migrated
        primary_class_names = {name for name, _ in classes}
        pre_nursery_subjects_migrated = db.execute(
            "SELECT value FROM config WHERE key='pre_nursery_one_subjects_migrated'"
        ).fetchone()
        if not pre_nursery_subjects_migrated:
            pre_nursery_class = db.execute(
                "SELECT id FROM classes WHERE name='Pre-Nursery One'"
            ).fetchone()
            if pre_nursery_class:
                for subject_name in nursery_subjects:
                    if subject_name not in pre_nursery_subjects:
                        db.execute(
                            "UPDATE subjects SET active=0 WHERE class_id=? AND name=?",
                            (pre_nursery_class["id"], subject_name),
                        )
            db.execute(
                "INSERT INTO config(key, value) "
                "VALUES ('pre_nursery_one_subjects_migrated', '1')"
            )
        for row in db.execute("SELECT id, name FROM classes").fetchall():
            if row["name"] not in primary_class_names:
                continue
            if row["name"] == "Pre-Nursery One":
                names = pre_nursery_subjects
                if migrate_nursery_subjects:
                    for subject_name in primary:
                        db.execute(
                            "UPDATE subjects SET active=0 WHERE class_id=? AND name=?",
                            (row["id"], subject_name)
                        )
            else:
                names = primary if row["name"] in ("Grade Four", "Grade Five") else lower_primary
            for subject_name in names:
                db.execute(
                    "INSERT OR IGNORE INTO subjects(name, class_id) VALUES (?, ?)",
                    (subject_name, row["id"])
                )
                if row["name"] == "Pre-Nursery One" and migrate_nursery_subjects:
                    db.execute(
                        "UPDATE subjects SET active=1 WHERE class_id=? AND name=?",
                        (row["id"], subject_name)
                    )
        if migrate_nursery_subjects:
            db.execute(
                "INSERT INTO config(key, value) VALUES ('nursery_subjects_migrated', '1')"
            )

        secondary_classes = {}
        for student in load_secondary_students():
            class_name = student["Class"].strip()
            section = student.get("Section", "").strip()
            if section and not class_name.casefold().endswith(section.casefold()):
                class_name = f"{class_name} {section}"
            class_data = secondary_classes.setdefault(
                class_name,
                {"section": section or "General", "students": []},
            )
            class_data["students"].append(student)

        for class_name, class_data in secondary_classes.items():
            db.execute(
                "INSERT OR IGNORE INTO classes(name, section) VALUES (?, ?)",
                (class_name, class_data["section"]),
            )
            class_id = db.execute(
                "SELECT id FROM classes WHERE name=?", (class_name,)
            ).fetchone()["id"]
            for subject_name in secondary_subjects_for(class_name):
                db.execute(
                    "INSERT OR IGNORE INTO subjects(name, class_id) VALUES (?, ?)",
                    (subject_name, class_id),
                )
            for sort_order, (assessment_name, maximum) in enumerate(
                assessment_defaults, 1
            ):
                db.execute(
                    "INSERT OR IGNORE INTO assessment_columns"
                    "(class_id, name, max_score, sort_order) VALUES (?, ?, ?, ?)",
                    (class_id, assessment_name, maximum, sort_order),
                )
            for student in class_data["students"]:
                db.execute(
                    "INSERT OR IGNORE INTO students"
                    "(name, admission_no, class_id, sex, session) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        student["Name"],
                        student["Admission No"],
                        class_id,
                        student.get("Sex", "Unknown"),
                        student.get("Session", "2026/2027"),
                    ),
                )

        try:
            from classes.student_data_2026_27 import students as initial_students
        except ImportError:
            initial_students = {}
        for class_name, names in initial_students.items():
            class_row = db.execute(
                "SELECT id FROM classes WHERE name=?", (class_name,)
            ).fetchone()
            if not class_row:
                continue
            admission_prefix = {
                "Pre-Nursery One": "PN",
                "Grade One Diamond": "G1",
                "Grade One Gold": "G1G",
                "Grade Two Gold": "G2G",
                "Grade Two Diamond": "G2D",
                "Grade Three Diamond": "G3D",
                "Grade Three Gold": "G3G",
                "Grade Four": "G4",
                "Grade Five": "G5",
            }.get(class_name, "STU")
            for index, name in enumerate(names, 1):
                db.execute(
                    "INSERT OR IGNORE INTO students(name, admission_no, class_id, session) "
                    "VALUES (?, ?, ?, ?)",
                    (name, f"{admission_prefix}/{index:03d}", class_row["id"], "2026/2027")
                )


class LoginFrame(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.configure(fg_color="#f2f5f7")

        card = ctk.CTkFrame(self, width=400, corner_radius=12)
        card.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(card, text="TPSA RESULT ADMIN", font=ctk.CTkFont(size=22, weight="bold")).pack(padx=30, pady=(30, 5))
        ctk.CTkLabel(card, text="Administrator Sign In").pack(pady=(0, 20))
        self.username = ctk.CTkEntry(card, width=300, placeholder_text="Username")
        self.username.pack(padx=30, pady=8)
        self.password = ctk.CTkEntry(card, width=300, placeholder_text="Password", show="*")
        self.password.pack(padx=30, pady=8)
        ctk.CTkButton(card, text="Sign In", width=300, command=self.sign_in).pack(padx=30, pady=(18, 30))
        self.password.bind("<Return>", lambda event: self.sign_in())

    def sign_in(self):
        username = self.username.get().strip()
        password = self.password.get()
        with get_db() as db:
            admin = db.execute(
                "SELECT * FROM admins WHERE username=? AND is_active=1", (username,)
            ).fetchone()
        if admin and check_password_hash(admin["password_hash"], password):
            self.app.current_admin_id = admin["id"]
            self.app.show_main()
        else:
            messagebox.showerror("Sign In Failed", "Invalid username or password.")


class MainFrame(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        sidebar = ctk.CTkFrame(self, width=210, corner_radius=0, fg_color="#12304a")
        sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(sidebar, text="TPSA ADMIN", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(pady=(24, 30), padx=16)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Students", self.show_students),
            ("Results", self.show_results),
            ("Result Configuration", self.show_config),
            ("Manage Admins", self.show_admins),
        ]
        for label, command in buttons:
            ctk.CTkButton(sidebar, text=label, fg_color="#1f6694", hover_color="#1a5579", command=command).pack(padx=16, pady=5, fill="x")
        ctk.CTkButton(sidebar, text="Sign Out", fg_color="#8a3434", hover_color="#702727", command=self.app.show_login).pack(side="bottom", padx=16, pady=20, fill="x")

        self.content = ctk.CTkFrame(self, fg_color="#f2f5f7")
        self.content.grid(row=0, column=1, sticky="nsew", padx=18, pady=18)
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=12, pady=(8, 18))
        with get_db() as db:
            counts = [
                ("Students", db.execute("SELECT COUNT(*) FROM students WHERE active=1").fetchone()[0]),
                ("Classes", db.execute("SELECT COUNT(*) FROM classes WHERE active=1").fetchone()[0]),
                ("Subjects", db.execute("SELECT COUNT(*) FROM subjects WHERE active=1").fetchone()[0]),
                ("Result Records", db.execute("SELECT COUNT(*) FROM result_scores").fetchone()[0]),
            ]
        cards = ctk.CTkFrame(self.content, fg_color="transparent")
        cards.pack(fill="x", padx=8)
        for label, value in counts:
            card = ctk.CTkFrame(cards)
            card.pack(side="left", padx=8, pady=8, expand=True, fill="x")
            ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(14, 2))
            ctk.CTkLabel(card, text=label).pack(pady=(0, 14))
        ctk.CTkLabel(self.content, text="Generate 3-Term Workbook", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=(30, 8))
        with get_db() as db:
            class_names = [row["name"] for row in db.execute("SELECT name FROM classes WHERE active=1 ORDER BY name")]
        self.generate_class = ctk.CTkComboBox(self.content, values=class_names, width=300)
        self.generate_class.pack(anchor="w", padx=12, pady=5)
        ctk.CTkLabel(self.content, text="Generates a workbook with first-, second-, and third-term sheets for every active student.").pack(anchor="w", padx=12, pady=4)
        ctk.CTkButton(self.content, text="Generate Workbook", command=self.generate_workbook).pack(anchor="w", padx=12, pady=8)

    def show_students(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Students", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=12, pady=(8, 12))

        form = ctk.CTkFrame(self.content)
        form.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(form, text="Name").grid(row=0, column=0, padx=8, pady=8)
        name_entry = ctk.CTkEntry(form, width=240)
        name_entry.grid(row=0, column=1, padx=8, pady=8)
        ctk.CTkLabel(form, text="Admission No").grid(row=0, column=2, padx=8, pady=8)
        admission_entry = ctk.CTkEntry(form, width=160)
        admission_entry.grid(row=0, column=3, padx=8, pady=8)

        with get_db() as db:
            class_rows = db.execute("SELECT * FROM classes WHERE active=1 ORDER BY name").fetchall()
            session_name = db.execute("SELECT value FROM config WHERE key='session'").fetchone()[0]
        class_names = [row["name"] for row in class_rows]
        class_combo = ctk.CTkComboBox(form, values=class_names, width=180)
        if class_names:
            class_combo.set(class_names[0])
        class_combo.grid(row=0, column=4, padx=8, pady=8)

        def add_student():
            name = name_entry.get().strip()
            admission_no = admission_entry.get().strip()
            class_name = class_combo.get()
            if not name or not admission_no or not class_name:
                messagebox.showwarning("Missing Information", "Name, admission number and class are required.")
                return
            class_id = next(row["id"] for row in class_rows if row["name"] == class_name)
            try:
                with get_db() as db:
                    db.execute(
                        "INSERT INTO students(name, admission_no, class_id, sex, session) VALUES (?, ?, ?, 'Unknown', ?)",
                        (name, admission_no, class_id, session_name)
                    )
                    db.commit()
                messagebox.showinfo("Student Added", f"{name} was added.")
                self.show_students()
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate Admission Number", "This admission number already exists.")

        ctk.CTkButton(form, text="Add Student", command=add_student).grid(row=0, column=5, padx=8, pady=8)
        ctk.CTkButton(form, text="Upload CSV/XLSX", command=lambda: self.upload_students(class_combo.get())).grid(row=1, column=5, padx=8, pady=8)

        table_frame = ctk.CTkScrollableFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=12, pady=12)
        with get_db() as db:
            students = db.execute(
                "SELECT s.*, c.name AS class_name FROM students s "
                "JOIN classes c ON c.id=s.class_id WHERE s.active=1 ORDER BY c.name, s.name"
            ).fetchall()
        for column, title in enumerate(("Name", "Admission No", "Class", "Session", "Action")):
            ctk.CTkLabel(table_frame, text=title, font=ctk.CTkFont(weight="bold")).grid(row=0, column=column, padx=12, pady=6, sticky="w")
        for row_number, student in enumerate(students, 1):
            ctk.CTkLabel(table_frame, text=student["name"]).grid(row=row_number, column=0, padx=12, pady=4, sticky="w")
            ctk.CTkLabel(table_frame, text=student["admission_no"]).grid(row=row_number, column=1, padx=12, pady=4, sticky="w")
            ctk.CTkLabel(table_frame, text=student["class_name"]).grid(row=row_number, column=2, padx=12, pady=4, sticky="w")
            ctk.CTkLabel(table_frame, text=student["session"]).grid(row=row_number, column=3, padx=12, pady=4, sticky="w")

            def deactivate_student(student_id=student["id"], student_name=student["name"]):
                if not messagebox.askyesno("Deactivate Student", f"Deactivate {student_name}? Existing results will be retained."):
                    return
                with get_db() as db:
                    db.execute("UPDATE students SET active=0 WHERE id=?", (student_id,))
                    db.commit()
                self.show_students()

            ctk.CTkButton(
                table_frame, text="Deactivate", width=90, fg_color="#8a3434",
                command=deactivate_student
            ).grid(row=row_number, column=4, padx=8, pady=4)

    def upload_students(self, selected_class):
        path = filedialog.askopenfilename(filetypes=[("Student Data", "*.csv *.xlsx")])
        if not path:
            return
        with get_db() as db:
            class_rows = db.execute("SELECT id, name FROM classes WHERE active=1").fetchall()
            session_name = db.execute("SELECT value FROM config WHERE key='session'").fetchone()[0]

        if not selected_class:
            messagebox.showwarning("Select Class", "Select the class in the student form before uploading.")
            return
        class_row = next((row for row in class_rows if row["name"] == selected_class), None)
        if not class_row:
            messagebox.showerror("Unknown Class", "The entered class name was not found.")
            return

        try:
            if path.lower().endswith(".csv"):
                with open(path, "r", encoding="utf-8-sig", newline="") as file:
                    records = list(csv.DictReader(file))
            else:
                workbook = load_workbook(path, read_only=True)
                worksheet = workbook.active
                headers = [str(cell.value).strip().lower() if cell.value else "" for cell in worksheet[1]]
                records = [
                    dict(zip(headers, [str(cell.value).strip() if cell.value is not None else "" for cell in row]))
                    for row in worksheet.iter_rows(min_row=2)
                ]
            added = 0
            with get_db() as db:
                for record in records:
                    name = record.get("name") or record.get("student name") or ""
                    admission_no = record.get("admission no") or record.get("admission_no") or ""
                    sex = record.get("sex") or "Unknown"
                    if not name or not admission_no:
                        continue
                    try:
                        db.execute(
                            "INSERT INTO students(name, admission_no, class_id, sex, session) VALUES (?, ?, ?, ?, ?)",
                            (name.strip(), admission_no.strip(), class_row["id"], sex, session_name)
                        )
                        added += 1
                    except sqlite3.IntegrityError:
                        pass
                db.commit()
            messagebox.showinfo("Upload Complete", f"{added} student(s) uploaded.")
            self.show_students()
        except Exception as exc:
            messagebox.showerror("Upload Failed", str(exc))

    def show_results(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Manage Results", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=12, pady=(8, 12))
        with get_db() as db:
            class_names = [row["name"] for row in db.execute("SELECT name FROM classes WHERE active=1 ORDER BY name")]
        class_combo = ctk.CTkComboBox(self.content, values=class_names, width=250)
        class_combo.pack(anchor="w", padx=12)
        if class_names:
            class_combo.set(class_names[0])
        term_combo = ctk.CTkComboBox(self.content, values=["First Term", "Second Term", "Third Term"], width=180)
        term_combo.set("First Term")
        term_combo.pack(anchor="w", padx=12, pady=8)
        table_frame = ctk.CTkScrollableFrame(self.content)
        table_frame.pack(fill="both", expand=True, padx=12, pady=10)

        entries = {}

        def load_results():
            for widget in table_frame.winfo_children():
                widget.destroy()
            entries.clear()
            class_name = class_combo.get()
            term = term_combo.get()
            term_number = {"First Term": 1, "Second Term": 2, "Third Term": 3}[term]
            with get_db() as db:
                session_name = db.execute(
                    "SELECT value FROM config WHERE key='session'"
                ).fetchone()[0]
                class_row = db.execute("SELECT id FROM classes WHERE name=?", (class_name,)).fetchone()
                if not class_row:
                    return
                assessments = db.execute(
                    "SELECT * FROM assessment_columns WHERE class_id=? AND active=1 ORDER BY sort_order, id",
                    (class_row["id"],)
                ).fetchall()
                subjects = db.execute(
                    "SELECT * FROM subjects WHERE class_id=? AND active=1 ORDER BY id",
                    (class_row["id"],)
                ).fetchall()
                students = db.execute(
                    "SELECT * FROM students WHERE class_id=? AND active=1 AND session=? ORDER BY name",
                    (class_row["id"], session_name)
                ).fetchall()
            titles = ["Student", "Subject"] + [row["name"] for row in assessments]
            for column, title in enumerate(titles):
                ctk.CTkLabel(table_frame, text=title, font=ctk.CTkFont(weight="bold")).grid(row=0, column=column, padx=8, pady=6)
            row_number = 1
            with get_db() as db:
                for student in students:
                    for subject in subjects:
                        saved_scores = {
                            row["assessment_id"]: row["score"]
                            for row in db.execute(
                                "SELECT assessment_id, score FROM result_scores "
                                "WHERE student_id=? AND subject_id=? AND term=?",
                                (student["id"], subject["id"], term_number)
                            ).fetchall()
                        }
                        ctk.CTkLabel(table_frame, text=student["name"]).grid(row=row_number, column=0, padx=8, pady=4, sticky="w")
                        ctk.CTkLabel(table_frame, text=subject["name"]).grid(row=row_number, column=1, padx=8, pady=4, sticky="w")
                        for offset, assessment in enumerate(assessments, 2):
                            entry = ctk.CTkEntry(table_frame, width=70)
                            entry.insert(0, str(saved_scores.get(assessment["id"], 0)))
                            entry.grid(row=row_number, column=offset, padx=4, pady=4)
                            entries[(student["id"], subject["id"], assessment["id"])] = entry
                        row_number += 1

        def save_results():
            term_number = {"First Term": 1, "Second Term": 2, "Third Term": 3}[term_combo.get()]
            try:
                submitted = []
                with get_db() as db:
                    class_id = db.execute(
                        "SELECT id FROM classes WHERE name=?", (class_combo.get(),)
                    ).fetchone()["id"]
                    assessment_maxima = {
                        row["id"]: (row["name"], row["max_score"])
                        for row in db.execute(
                            "SELECT id, name, max_score FROM assessment_columns "
                            "WHERE class_id=? AND active=1",
                            (class_id,)
                        ).fetchall()
                    }
                    for (student_id, subject_id, assessment_id), entry in entries.items():
                        value = float(entry.get())
                        if assessment_id not in assessment_maxima:
                            raise ValueError("An assessment column changed. Reload the results before saving.")
                        name, maximum = assessment_maxima[assessment_id]
                        if value < 0 or value > maximum:
                            raise ValueError(f"{name} must be between 0 and {maximum:g}.")
                        submitted.append((student_id, subject_id, term_number, assessment_id, value))
                    for student_id, subject_id, term, assessment_id, value in submitted:
                        db.execute("""
                            INSERT INTO result_scores(student_id, subject_id, term, assessment_id, score)
                            VALUES (?, ?, ?, ?, ?)
                            ON CONFLICT(student_id, subject_id, term, assessment_id)
                            DO UPDATE SET score=excluded.score
                        """, (student_id, subject_id, term, assessment_id, value))
                    db.commit()
                messagebox.showinfo("Saved", "Results saved successfully.")
            except ValueError as exc:
                messagebox.showerror("Invalid Score", str(exc) or "Scores must be numeric.")

        controls = ctk.CTkFrame(self.content, fg_color="transparent")
        controls.pack(anchor="w", padx=12, pady=8)
        ctk.CTkButton(controls, text="Load Results", command=load_results).pack(side="left", padx=4)
        ctk.CTkButton(controls, text="Save Results", command=save_results).pack(side="left", padx=4)

    def show_config(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Result Configuration", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=12, pady=(8, 12))
        with get_db() as db:
            values = dict(db.execute("SELECT key, value FROM config").fetchall())
            classes = db.execute(
                "SELECT * FROM classes WHERE active=1 ORDER BY name"
            ).fetchall()
            subjects = db.execute("""
                SELECT s.*, c.name AS class_name
                FROM subjects s LEFT JOIN classes c ON c.id=s.class_id
                WHERE s.active=1 ORDER BY c.name, s.name
            """).fetchall()
        scroll = ctk.CTkScrollableFrame(self.content)
        scroll.pack(fill="both", expand=True, padx=8, pady=8)
        form = ctk.CTkFrame(scroll)
        form.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(form, text="School and Session", font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w"
        )
        fields = {}
        labels = [
            ("session", "Academic Session"),
            ("school_name", "School Name"),
            ("resumption_date", "Resumption Date"),
            ("closing_date", "Closing Date"),
        ]
        for index, (key, label) in enumerate(labels, 1):
            ctk.CTkLabel(form, text=label).grid(row=index, column=0, padx=8, pady=6, sticky="w")
            entry = ctk.CTkEntry(form, width=240)
            entry.insert(0, values.get(key, ""))
            entry.grid(row=index, column=1, padx=8, pady=6, sticky="w")
            fields[key] = entry

        assessment_frame = ctk.CTkFrame(scroll)
        assessment_frame.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(
            assessment_frame,
            text="Assessment Columns (active maximums must total 100)",
            font=ctk.CTkFont(size=17, weight="bold"),
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        assessment_class = ctk.CTkComboBox(
            assessment_frame, values=[row["name"] for row in classes], width=220
        )
        if classes:
            assessment_class.set(classes[0]["name"])
        assessment_class.grid(row=1, column=0, padx=8, pady=8, sticky="w")
        assessment_rows_frame = ctk.CTkFrame(assessment_frame, fg_color="transparent")
        assessment_rows_frame.grid(row=2, column=0, columnspan=4, padx=8, pady=4, sticky="ew")
        assessment_widgets = []

        def load_assessment_rows(selected_class=None):
            for widget in assessment_rows_frame.winfo_children():
                widget.destroy()
            assessment_widgets.clear()
            class_name = selected_class or assessment_class.get()
            class_row = next((row for row in classes if row["name"] == class_name), None)
            if not class_row:
                return
            with get_db() as db:
                configured_assessments = db.execute(
                    "SELECT * FROM assessment_columns WHERE class_id=? ORDER BY sort_order, id",
                    (class_row["id"],)
                ).fetchall()
            ctk.CTkLabel(assessment_rows_frame, text="Column name").grid(row=0, column=0, padx=8, pady=4, sticky="w")
            ctk.CTkLabel(assessment_rows_frame, text="Maximum mark").grid(row=0, column=1, padx=8, pady=4)
            ctk.CTkLabel(assessment_rows_frame, text="Included").grid(row=0, column=2, padx=8, pady=4)
            for row_number, assessment in enumerate(configured_assessments, 1):
                name_entry = ctk.CTkEntry(assessment_rows_frame, width=220)
                name_entry.insert(0, assessment["name"])
                name_entry.grid(row=row_number, column=0, padx=8, pady=4)
                maximum_entry = ctk.CTkEntry(assessment_rows_frame, width=100)
                maximum_entry.insert(0, f"{assessment['max_score']:g}")
                maximum_entry.grid(row=row_number, column=1, padx=8, pady=4)
                active_var = BooleanVar(value=bool(assessment["active"]))
                ctk.CTkCheckBox(assessment_rows_frame, text="", variable=active_var).grid(
                    row=row_number, column=2, padx=8, pady=4
                )
                assessment_widgets.append(
                    (assessment["id"], name_entry, maximum_entry, active_var)
                )

        assessment_class.configure(command=load_assessment_rows)
        load_assessment_rows()

        new_assessment_name = ctk.CTkEntry(
            assessment_frame, width=220, placeholder_text="New scored column"
        )
        new_assessment_name.grid(row=3, column=0, padx=8, pady=8)
        new_assessment_maximum = ctk.CTkEntry(
            assessment_frame, width=120, placeholder_text="Maximum mark"
        )
        new_assessment_maximum.grid(row=3, column=1, padx=8, pady=8)
        assessment_status = ctk.CTkLabel(assessment_frame, text="")
        assessment_status.grid(row=4, column=0, columnspan=3, padx=8, pady=4, sticky="w")

        def add_assessment_column():
            name = new_assessment_name.get().strip()
            class_row = next(
                (row for row in classes if row["name"] == assessment_class.get()),
                None,
            )
            try:
                maximum = float(new_assessment_maximum.get())
                if not name or not class_row or not math.isfinite(maximum) or maximum <= 0:
                    raise ValueError("Enter a column name and a positive maximum mark.")
                with get_db() as db:
                    sort_order = db.execute(
                        "SELECT COALESCE(MAX(sort_order), 0) + 1 FROM assessment_columns WHERE class_id=?",
                        (class_row["id"],)
                    ).fetchone()[0]
                    db.execute(
                        "INSERT INTO assessment_columns(class_id, name, max_score, sort_order) "
                        "VALUES (?, ?, ?, ?)",
                        (class_row["id"], name, maximum, sort_order)
                    )
                    db.commit()
                new_assessment_name.delete(0, "end")
                new_assessment_maximum.delete(0, "end")
                load_assessment_rows()
                messagebox.showinfo(
                    "Column Added",
                    "Adjust the included maximum marks so they total 100, then save the columns."
                )
            except ValueError as exc:
                messagebox.showerror("Invalid Column", str(exc))
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate Column", "That scored column already exists for this class.")

        def save_assessment_columns():
            try:
                updates = []
                included_total = 0
                for assessment_id, name_entry, maximum_entry, active_var in assessment_widgets:
                    name = name_entry.get().strip()
                    maximum = float(maximum_entry.get())
                    if not name or not math.isfinite(maximum) or maximum <= 0:
                        raise ValueError("Every column needs a name and a maximum greater than zero.")
                    active = bool(active_var.get())
                    if active:
                        included_total += maximum
                    updates.append((name, maximum, int(active), assessment_id))
                if not updates or not math.isfinite(included_total) or abs(included_total - 100) > 0.000001:
                    raise ValueError(
                        f"Included assessment maximums must total 100 (currently {included_total:g})."
                    )
                with get_db() as db:
                    db.executemany(
                        "UPDATE assessment_columns SET name=?, max_score=?, active=? WHERE id=?",
                        updates
                    )
                    db.commit()
                assessment_status.configure(text="Assessment columns saved; active maximums total 100.")
            except ValueError as exc:
                messagebox.showerror("Invalid Assessment Setup", str(exc))
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate Column", "Column names must be unique within the selected class.")

        grade_frame = ctk.CTkFrame(scroll)
        grade_frame.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(grade_frame, text="Grade Boundaries (minimum score)", font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, columnspan=5, padx=10, pady=10, sticky="w"
        )
        grade_fields = {}
        for column, (key, label) in enumerate((
            ("grade_a_min", "A"),
            ("grade_b_min", "B"),
            ("grade_c_min", "C"),
            ("grade_d_min", "D"),
            ("grade_e_min", "E"),
        )):
            ctk.CTkLabel(grade_frame, text=label).grid(row=1, column=column, padx=8, pady=4)
            entry = ctk.CTkEntry(grade_frame, width=80)
            entry.insert(0, values.get(key, "0"))
            entry.grid(row=2, column=column, padx=8, pady=(0, 10))
            grade_fields[key] = entry

        report_frame = ctk.CTkFrame(scroll)
        report_frame.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(
            report_frame,
            text="Optional Report Columns (Subject and Total are required)",
            font=ctk.CTkFont(size=17, weight="bold"),
        ).pack(anchor="w", padx=10, pady=10)
        report_field_labels = [
            ("report_field_subject_average", "Subject average"),
            ("report_field_first_term", "1st term score"),
            ("report_field_second_term", "2nd term score"),
            ("report_field_cumulative", "Cumulative score"),
            ("report_field_grade", "Grade"),
            ("report_field_position", "Position"),
            ("report_field_remark", "Remark"),
        ]
        report_field_vars = {}
        report_field_controls = ctk.CTkFrame(report_frame, fg_color="transparent")
        report_field_controls.pack(anchor="w", padx=8, pady=(0, 8))
        for index, (key, label) in enumerate(report_field_labels):
            variable = BooleanVar(value=values.get(key, "1") == "1")
            report_field_vars[key] = variable
            ctk.CTkCheckBox(
                report_field_controls,
                text=label,
                variable=variable,
            ).grid(row=index // 3, column=index % 3, padx=8, pady=6, sticky="w")

        management = ctk.CTkFrame(scroll)
        management.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(management, text="Classes and Subjects", font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w"
        )
        class_entry = ctk.CTkEntry(management, width=220, placeholder_text="New class name")
        class_entry.grid(row=1, column=0, padx=8, pady=8)
        section_entry = ctk.CTkEntry(management, width=140, placeholder_text="Section")
        section_entry.insert(0, "General")
        section_entry.grid(row=1, column=1, padx=8, pady=8)
        class_combo = ctk.CTkComboBox(management, values=[row["name"] for row in classes], width=200)
        if classes:
            class_combo.set(classes[0]["name"])
        class_combo.grid(row=2, column=0, padx=8, pady=8)
        subject_entry = ctk.CTkEntry(management, width=220, placeholder_text="New subject")
        subject_entry.grid(row=2, column=1, padx=8, pady=8)
        subject_combo = ctk.CTkComboBox(
            management,
            values=[f"{row['class_name']}: {row['name']}" for row in subjects],
            width=280,
        )
        if subjects:
            subject_combo.set(f"{subjects[0]['class_name']}: {subjects[0]['name']}")
        subject_combo.grid(row=3, column=0, columnspan=2, padx=8, pady=8, sticky="w")

        def persist_config():
            try:
                session_value = fields["session"].get().strip()
                session_parts = session_value.split("/")
                if len(session_parts) != 2 or not all(part.isdigit() for part in session_parts):
                    raise ValueError("Academic session must use the format YYYY/YYYY.")
                if int(session_parts[1]) != int(session_parts[0]) + 1:
                    raise ValueError("The second session year must follow the first by one year.")
                updated_values = {key: entry.get().strip() for key, entry in fields.items()}
                updated_values.update({key: entry.get().strip() for key, entry in grade_fields.items()})
                updated_values.update({
                    key: str(int(variable.get()))
                    for key, variable in report_field_vars.items()
                })
                grade_minima = [float(updated_values[key]) for key in grade_fields]
                if any(value < 0 or value > 100 for value in grade_minima):
                    raise ValueError("Grade boundaries must be between 0 and 100.")
                if grade_minima != sorted(grade_minima, reverse=True):
                    raise ValueError("Grade boundaries must descend from A through E.")
                for key in ("resumption_date", "closing_date"):
                    datetime.strptime(updated_values[key], "%Y-%m-%d")
                with get_db() as db:
                    for key, value in updated_values.items():
                        db.execute(
                            "INSERT INTO config(key, value) VALUES (?, ?) "
                            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                            (key, value)
                        )
                    db.commit()
                messagebox.showinfo("Saved", "Result configuration saved.")
            except ValueError as exc:
                messagebox.showerror("Invalid Configuration", str(exc))

        def add_class():
            name = class_entry.get().strip()
            section = section_entry.get().strip() or "General"
            if not name:
                messagebox.showwarning("Class Required", "Enter a class name.")
                return
            try:
                with get_db() as db:
                    cursor = db.execute("INSERT INTO classes(name, section) VALUES (?, ?)", (name, section))
                    class_id = cursor.lastrowid
                    is_upper_primary = name in ("Grade Four", "Grade Five")
                    default_subjects = [
                        "English Studies", "Mathematics", "Phonics", "Basic Science & Technology",
                        "Social & Citizenship Studies", "French", "Cultural & Creative Art",
                        "Physical & Health Education", "CRS/IRS", "History", "Hausa", "Handwriting",
                    ]
                    if is_upper_primary:
                        default_subjects.extend(["Pre-Vocational Studies", "Basic Digital Literacy"])
                    for subject_name in default_subjects:
                        db.execute(
                            "INSERT OR IGNORE INTO subjects(name, class_id) VALUES (?, ?)",
                            (subject_name, class_id)
                        )
                    for sort_order, (assessment_name, maximum_key) in enumerate((
                        ("CA1", "ca1_max"),
                        ("CA2", "ca2_max"),
                        ("CA3", "ca3_max"),
                        ("EXAM", "exam_max"),
                    ), 1):
                        maximum = float(
                            db.execute(
                                "SELECT value FROM config WHERE key=?", (maximum_key,)
                            ).fetchone()[0]
                        )
                        db.execute(
                            "INSERT INTO assessment_columns(class_id, name, max_score, sort_order) "
                            "VALUES (?, ?, ?, ?)",
                            (class_id, assessment_name, maximum, sort_order)
                        )
                    db.commit()
                messagebox.showinfo("Added", "Class and its default subjects were added.")
                self.show_config()
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate Class", "That class already exists.")

        def add_subject():
            name = subject_entry.get().strip()
            selected = class_combo.get()
            class_row = next((row for row in classes if row["name"] == selected), None)
            if not name or not class_row:
                messagebox.showwarning("Subject Required", "Choose a class and enter a subject name.")
                return
            try:
                with get_db() as db:
                    db.execute("INSERT INTO subjects(name, class_id) VALUES (?, ?)", (name, class_row["id"]))
                    db.commit()
                messagebox.showinfo("Added", f"{name} added to {selected}.")
                self.show_config()
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate Subject", "That subject already exists for the selected class.")

        def deactivate_subject():
            selected = subject_combo.get()
            subject = next(
                (row for row in subjects if f"{row['class_name']}: {row['name']}" == selected),
                None
            )
            if not subject:
                return
            if not messagebox.askyesno("Remove Subject", f"Remove {subject['name']} from active results for {subject['class_name']}?"):
                return
            with get_db() as db:
                db.execute("UPDATE subjects SET active=0 WHERE id=?", (subject["id"],))
                db.commit()
            self.show_config()

        ctk.CTkButton(form, text="Save School / Session", command=persist_config).grid(row=4, column=1, padx=8, pady=12, sticky="w")
        ctk.CTkButton(
            assessment_frame, text="Save Assessment Columns",
            command=save_assessment_columns
        ).grid(row=3, column=2, padx=8, pady=8)
        ctk.CTkButton(
            assessment_frame, text="Add Scored Column",
            command=add_assessment_column
        ).grid(row=3, column=3, padx=8, pady=8)
        ctk.CTkButton(grade_frame, text="Save Grade Rules", command=persist_config).grid(row=3, column=0, columnspan=5, padx=8, pady=(0, 12))
        ctk.CTkButton(management, text="Add Class", command=add_class).grid(row=1, column=2, padx=8, pady=8)
        ctk.CTkButton(management, text="Add Subject to Class", command=add_subject).grid(row=2, column=2, padx=8, pady=8)
        ctk.CTkButton(management, text="Deactivate Selected Subject", fg_color="#8a3434", command=deactivate_subject).grid(row=3, column=2, padx=8, pady=8)

    def show_admins(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Manage Administrators", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=12, pady=(8, 12))
        form = ctk.CTkFrame(self.content)
        form.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(form, text="Create admin account", font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=8, pady=8, sticky="w"
        )
        username = ctk.CTkEntry(form, width=200, placeholder_text="Username")
        username.grid(row=1, column=0, padx=8, pady=8)
        password = ctk.CTkEntry(form, width=200, placeholder_text="Temporary password", show="*")
        password.grid(row=1, column=1, padx=8, pady=8)

        def create_admin():
            new_username = username.get().strip()
            new_password = password.get()
            if not new_username or len(new_password) < 12:
                messagebox.showwarning("Invalid Account", "Enter a username and a password of at least 12 characters.")
                return
            try:
                with get_db() as db:
                    db.execute(
                        "INSERT INTO admins(username, password_hash, created_at, is_active) VALUES (?, ?, ?, 1)",
                        (new_username, generate_password_hash(new_password), datetime.now().isoformat())
                    )
                    db.commit()
                messagebox.showinfo("Admin Created", f"Account {new_username} is ready.")
                self.show_admins()
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate Username", "That username is already in use.")

        ctk.CTkButton(form, text="Create Admin", command=create_admin).grid(row=1, column=2, padx=8, pady=8)

        password_form = ctk.CTkFrame(self.content)
        password_form.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(password_form, text="Change my password", font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=8, pady=8, sticky="w"
        )
        current_password = ctk.CTkEntry(password_form, width=200, placeholder_text="Current password", show="*")
        current_password.grid(row=1, column=0, padx=8, pady=8)
        new_password = ctk.CTkEntry(password_form, width=200, placeholder_text="New password (12+ chars)", show="*")
        new_password.grid(row=1, column=1, padx=8, pady=8)

        def change_password():
            if len(new_password.get()) < 12:
                messagebox.showwarning("Weak Password", "Use at least 12 characters for the new password.")
                return
            with get_db() as db:
                admin = db.execute(
                    "SELECT * FROM admins WHERE id=? AND is_active=1",
                    (self.app.current_admin_id,)
                ).fetchone()
                if not admin or not check_password_hash(admin["password_hash"], current_password.get()):
                    messagebox.showerror("Incorrect Password", "The current password is incorrect.")
                    return
                db.execute(
                    "UPDATE admins SET password_hash=? WHERE id=?",
                    (generate_password_hash(new_password.get()), self.app.current_admin_id)
                )
                db.commit()
            messagebox.showinfo("Password Changed", "Your password was updated.")
            self.show_admins()

        ctk.CTkButton(password_form, text="Change Password", command=change_password).grid(row=1, column=2, padx=8, pady=8)

        listing = ctk.CTkScrollableFrame(self.content)
        listing.pack(fill="both", expand=True, padx=12, pady=8)
        with get_db() as db:
            admins = db.execute("SELECT id, username, is_active FROM admins ORDER BY username").fetchall()
        for row_index, admin in enumerate(admins):
            ctk.CTkLabel(listing, text=admin["username"]).grid(row=row_index, column=0, padx=10, pady=6, sticky="w")
            ctk.CTkLabel(listing, text="Active" if admin["is_active"] else "Inactive").grid(row=row_index, column=1, padx=10, pady=6)

            def reset_password(admin_id=admin["id"], admin_name=admin["username"]):
                dialog = ctk.CTkInputDialog(
                    text=f"Enter a temporary password for {admin_name} (12+ characters):",
                    title="Reset Admin Password",
                )
                temporary_password = dialog.get_input()
                if temporary_password is None:
                    return
                if len(temporary_password) < 12:
                    messagebox.showwarning("Weak Password", "Use at least 12 characters.")
                    return
                with get_db() as db:
                    db.execute(
                        "UPDATE admins SET password_hash=? WHERE id=?",
                        (generate_password_hash(temporary_password), admin_id)
                    )
                    db.commit()
                messagebox.showinfo("Password Reset", f"{admin_name}'s password was reset.")

            ctk.CTkButton(
                listing, text="Reset Password", width=120,
                command=reset_password
            ).grid(row=row_index, column=2, padx=6, pady=6)

            if admin["id"] != self.app.current_admin_id and admin["is_active"]:
                def deactivate(admin_id=admin["id"], admin_name=admin["username"]):
                    with get_db() as db:
                        active_count = db.execute("SELECT COUNT(*) FROM admins WHERE is_active=1").fetchone()[0]
                        if active_count <= 1:
                            messagebox.showerror("Cannot Deactivate", "At least one active administrator must remain.")
                            return
                        db.execute("UPDATE admins SET is_active=0 WHERE id=?", (admin_id,))
                        db.commit()
                    messagebox.showinfo("Admin Deactivated", f"{admin_name} can no longer sign in.")
                    self.show_admins()
                ctk.CTkButton(
                    listing, text="Deactivate", fg_color="#8a3434",
                    command=deactivate, width=100
                ).grid(row=row_index, column=3, padx=6, pady=6)
            elif not admin["is_active"]:
                def activate(admin_id=admin["id"], admin_name=admin["username"]):
                    with get_db() as db:
                        db.execute("UPDATE admins SET is_active=1 WHERE id=?", (admin_id,))
                        db.commit()
                    messagebox.showinfo("Admin Activated", f"{admin_name} can sign in again.")
                    self.show_admins()
                ctk.CTkButton(
                    listing, text="Activate", width=100,
                    command=activate
                ).grid(row=row_index, column=3, padx=6, pady=6)

    def generate_workbook(self):
        class_name = self.generate_class.get()
        if not class_name:
            messagebox.showwarning("Select Class", "Select a class before generating.")
            return
        try:
            path = generate_workbook(class_name)
            messagebox.showinfo("Workbook Generated", path)
        except Exception as exc:
            messagebox.showerror("Generation Failed", str(exc))


def generate_workbook(class_name):
    with get_db() as db:
        class_row = db.execute("SELECT * FROM classes WHERE name=?", (class_name,)).fetchone()
        if not class_row:
            raise ValueError("Class not found")
        values = dict(db.execute("SELECT key, value FROM config").fetchall())
        subject_rows = db.execute(
            "SELECT * FROM subjects WHERE class_id=? AND active=1 ORDER BY id",
            (class_row["id"],)
        ).fetchall()
        assessment_rows = db.execute(
            "SELECT * FROM assessment_columns WHERE class_id=? AND active=1 ORDER BY sort_order, id",
            (class_row["id"],)
        ).fetchall()
        student_rows = db.execute(
            "SELECT * FROM students WHERE class_id=? AND active=1 AND session=? ORDER BY name",
            (class_row["id"], values["session"])
        ).fetchall()
        all_results = db.execute("""
            SELECT rs.*, s.admission_no, sub.name AS subject_name,
                   ac.name AS assessment_name
            FROM result_scores rs
            JOIN students s ON s.id=rs.student_id
            JOIN subjects sub ON sub.id=rs.subject_id
            JOIN assessment_columns ac ON ac.id=rs.assessment_id
            WHERE s.class_id=? AND s.active=1 AND s.session=?
              AND sub.active=1 AND ac.active=1
        """, (class_row["id"], values["session"])).fetchall()

    if not student_rows:
        raise ValueError(f"No active students are assigned to {class_name}.")
    if not subject_rows:
        raise ValueError(f"No active subjects are configured for {class_name}.")
    if not assessment_rows:
        raise ValueError(f"No active assessment columns are configured for {class_name}.")
    required = ("grade_a_min", "grade_b_min", "grade_c_min", "grade_d_min", "grade_e_min")
    missing = [key for key in required if key not in values]
    if missing:
        raise ValueError(f"Missing result configuration: {', '.join(missing)}.")
    maxima = [float(row["max_score"]) for row in assessment_rows]
    if not all(math.isfinite(maximum) for maximum in maxima) or abs(sum(maxima) - 100) > 0.000001:
        raise ValueError("Active assessment column maximums must total 100.")
    grade_limits = [
        float(values[key]) for key in
        ("grade_a_min", "grade_b_min", "grade_c_min", "grade_d_min", "grade_e_min")
    ]
    if grade_limits != sorted(grade_limits, reverse=True):
        raise ValueError("Grade boundaries must descend from A through E.")

    session_parts = values["session"].split("/")
    if len(session_parts) != 2 or not all(part.isdigit() for part in session_parts):
        raise ValueError("Academic session must use the format YYYY/YYYY.")
    if int(session_parts[1]) != int(session_parts[0]) + 1:
        raise ValueError("The second session year must follow the first by one year.")
    folder_name = f"{session_parts[0]}-{session_parts[1][-2:]}"
    output_folder = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(output_folder, exist_ok=True)
    base_class_name = class_row["name"].replace(" Gold", "").replace(" Diamond", "")
    students_data = [
        {
            "Name": row["name"],
            "Admission No": row["admission_no"],
            "Class": base_class_name,
            "Term": "Third Term",
            "Session": values["session"],
            "Sex": row["sex"],
            "Section": class_row["section"],
        }
        for row in student_rows
    ]
    class_data = {
        "Class": base_class_name,
        "Term": "Third Term",
        "Session": values["session"],
        "Resumption Date": values.get("resumption_date", ""),
        "Closing Date": values.get("closing_date", ""),
        "Total Students": len(students_data),
        "Average Attendance": 95.0,
        "Coordinator": "Head Teacher",
        "Section": class_row["section"],
    }
    score_data = {}
    for row in all_results:
        score_data.setdefault(
            (row["admission_no"], row["subject_name"], row["term"]), {}
        )[row["assessment_name"]] = row["score"] or 0
    report_config = {
        "school_name": values["school_name"],
        **{key: float(values[key]) for key in required},
    }
    report_fields = {
        key.replace("report_field_", "", 1): values.get(key, "1") == "1"
        for key in (
            "report_field_subject_average",
            "report_field_first_term",
            "report_field_second_term",
            "report_field_cumulative",
            "report_field_grade",
            "report_field_position",
            "report_field_remark",
        )
    }
    section_suffix = f"_{class_row['section']}" if class_row["section"] != "General" else ""
    file_name = (
        f"{base_class_name}{section_suffix}_"
        f"COMPLETE_3-TERM_RESULTS_{values['session'].replace('/', '_')}.xlsx"
    )
    path = os.path.join(output_folder, file_name)
    return generate_grade_workbook(
        students_data,
        class_data,
        [row["name"] for row in subject_rows],
        score_data=score_data,
        selected_report_config=report_config,
        selected_assessments=[
            {"name": row["name"], "max_score": float(row["max_score"])}
            for row in assessment_rows
        ],
        selected_report_fields=report_fields,
        output_path=path,
    )


class TPSAApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.title("TOPSTEPS Academy Result Manager")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.login_frame = None
        self.main_frame = None
        self.show_login()

    def show_login(self):
        if self.main_frame:
            self.main_frame.pack_forget()
            self.main_frame.destroy()
            self.main_frame = None
        self.login_frame = LoginFrame(self)
        self.login_frame.pack(fill="both", expand=True)

    def show_main(self):
        if self.login_frame:
            self.login_frame.pack_forget()
            self.login_frame.destroy()
            self.login_frame = None
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    init_db()
    app = TPSAApp()
    app.mainloop()

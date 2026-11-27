import os
import math
import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, send_file, session, url_for
from werkzeug.security import check_password_hash

from desktop_app import generate_workbook, get_db, init_db


app = Flask(__name__)
app.secret_key = os.environ.get("TPSA_SECRET_KEY", os.urandom(32))


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def flash_message(message, category="success"):
    messages = session.setdefault("_messages", [])
    messages.append({"category": category, "text": message})


@app.context_processor
def inject_messages():
    messages = session.pop("_messages", [])
    return {"messages": messages}


@app.before_request
def initialize():
    init_db()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        with get_db() as db:
            admin = db.execute(
                "SELECT * FROM admins WHERE username=? AND is_active=1",
                (username,),
            ).fetchone()
        if admin and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin_id"] = admin["id"]
            session["username"] = admin["username"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    with get_db() as db:
        counts = {
            "students": db.execute("SELECT COUNT(*) FROM students WHERE active=1").fetchone()[0],
            "classes": db.execute("SELECT COUNT(*) FROM classes WHERE active=1").fetchone()[0],
            "subjects": db.execute("SELECT COUNT(*) FROM subject_catalog WHERE active=1").fetchone()[0],
            "results": db.execute("SELECT COUNT(*) FROM result_scores").fetchone()[0],
        }
        classes = db.execute("SELECT name FROM classes WHERE active=1 ORDER BY name").fetchall()
    return render_template("dashboard.html", counts=counts, classes=[row["name"] for row in classes])


@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    with get_db() as db:
        class_rows = db.execute("SELECT id, name FROM classes WHERE active=1 ORDER BY name").fetchall()
        session_name = db.execute("SELECT value FROM config WHERE key='session'").fetchone()[0]
        if request.method == "POST":
            if request.form.get("action") == "toggle":
                student_id = request.form.get("student_id", type=int)
                student = db.execute(
                    "SELECT active FROM students WHERE id=?", (student_id,)
                ).fetchone()
                if student:
                    db.execute(
                        "UPDATE students SET active=? WHERE id=?",
                        (0 if student["active"] else 1, student_id),
                    )
                    flash_message("Student status updated.")
                else:
                    flash_message("Student not found.", "error")
            else:
                name = request.form.get("name", "").strip()
                admission_no = request.form.get("admission_no", "").strip()
                sex = request.form.get("sex", "Unknown").strip()
                class_id = request.form.get("class_id", type=int)
                class_exists = db.execute(
                    "SELECT 1 FROM classes WHERE id=? AND active=1", (class_id,)
                ).fetchone()
                if name and admission_no and class_exists:
                    try:
                        db.execute(
                            "INSERT INTO students(name, admission_no, class_id, sex, session) "
                            "VALUES (?, ?, ?, ?, ?)",
                            (name, admission_no, class_id, sex, session_name),
                        )
                        flash_message("Student added successfully.")
                    except sqlite3.IntegrityError:
                        flash_message("That admission number is already in use.", "error")
                else:
                    flash_message(
                        "Name, admission number, and an active class are required.",
                        "error",
                    )
        rows = db.execute(
            "SELECT s.*, c.name AS class_name FROM students s "
            "JOIN classes c ON c.id=s.class_id "
            "WHERE s.session=? ORDER BY c.name, s.name",
            (session_name,),
        ).fetchall()
    return render_template(
        "students.html",
        students=rows,
        classes=class_rows,
    )


@app.route("/classes", methods=["GET", "POST"])
@login_required
def manage_classes():
    with get_db() as db:
        if request.method == "POST":
            action = request.form.get("action", "add")
            if action == "toggle":
                class_id = request.form.get("class_id", type=int)
                class_row = db.execute(
                    "SELECT active FROM classes WHERE id=?", (class_id,)
                ).fetchone()
                if class_row:
                    db.execute(
                        "UPDATE classes SET active=? WHERE id=?",
                        (0 if class_row["active"] else 1, class_id),
                    )
                    flash_message("Class status updated.")
                else:
                    flash_message("Class not found.", "error")
            else:
                name = request.form.get("name", "").strip()
                section = request.form.get("section", "").strip() or "General"
                if not name:
                    flash_message("Enter a class name.", "error")
                else:
                    try:
                        class_id = db.execute(
                            "INSERT INTO classes(name, section) VALUES (?, ?)",
                            (name, section),
                        ).lastrowid
                        maxima = {
                            row["key"]: float(row["value"])
                            for row in db.execute(
                                "SELECT key, value FROM config WHERE key IN "
                                "('ca1_max','ca2_max','ca3_max','exam_max')"
                            ).fetchall()
                        }
                        for order, (column, key) in enumerate((
                            ("CA1", "ca1_max"), ("CA2", "ca2_max"),
                            ("CA3", "ca3_max"), ("EXAM", "exam_max"),
                        ), 1):
                            db.execute(
                                "INSERT INTO assessment_columns"
                                "(class_id, name, max_score, sort_order) VALUES (?, ?, ?, ?)",
                                (class_id, column, maxima[key], order),
                            )
                        flash_message("Class added. Assign its subjects in Class Subject Assignment.")
                    except sqlite3.IntegrityError:
                        flash_message(
                            "That class already exists. Reactivate it from the class list if needed.",
                            "error",
                        )
        classes = db.execute("""
            SELECT c.*, COUNT(s.id) AS student_count
            FROM classes c LEFT JOIN students s ON s.class_id=c.id AND s.active=1
            GROUP BY c.id ORDER BY c.name
        """).fetchall()
    return render_template("classes.html", classes=classes)


@app.route("/subjects", methods=["GET", "POST"])
@login_required
def manage_subjects():
    with get_db() as db:
        if request.method == "POST":
            action = request.form.get("action", "add")
            if action == "toggle":
                subject_id = request.form.get("subject_id", type=int)
                subject = db.execute(
                    "SELECT id, name, active FROM subject_catalog WHERE id=?",
                    (subject_id,),
                ).fetchone()
                if subject:
                    active = 0 if subject["active"] else 1
                    db.execute(
                        "UPDATE subject_catalog SET active=? WHERE id=?",
                        (active, subject_id),
                    )
                    if not active:
                        db.execute("UPDATE subjects SET active=0 WHERE name=?", (subject["name"],))
                    flash_message("Subject status updated.")
                else:
                    flash_message("Subject not found.", "error")
            else:
                name = request.form.get("name", "").strip()
                if not name:
                    flash_message("Enter a subject name.", "error")
                else:
                    try:
                        db.execute("INSERT INTO subject_catalog(name) VALUES (?)", (name,))
                        flash_message("Subject added to the catalogue.")
                    except sqlite3.IntegrityError:
                        flash_message("That subject already exists in the catalogue.", "error")
        subjects = db.execute("""
            SELECT sc.*, COUNT(s.id) AS assigned_count
            FROM subject_catalog sc
            LEFT JOIN subjects s ON s.name=sc.name AND s.active=1
            GROUP BY sc.id ORDER BY sc.name
        """).fetchall()
    return render_template("subjects.html", subjects=subjects)


@app.route("/assignments", methods=["GET", "POST"])
@login_required
def manage_assignments():
    with get_db() as db:
        if request.method == "POST":
            action = request.form.get("action", "assign")
            if action == "toggle":
                assignment_id = request.form.get("assignment_id", type=int)
                assignment = db.execute(
                    "SELECT active FROM subjects WHERE id=? AND class_id IS NOT NULL",
                    (assignment_id,),
                ).fetchone()
                if assignment:
                    db.execute(
                        "UPDATE subjects SET active=? WHERE id=?",
                        (0 if assignment["active"] else 1, assignment_id),
                    )
                    flash_message("Subject assignment status updated.")
                else:
                    flash_message("Assignment not found.", "error")
            else:
                class_id = request.form.get("class_id", type=int)
                subject_id = request.form.get("subject_id", type=int)
                target_class = db.execute(
                    "SELECT id FROM classes WHERE id=? AND active=1", (class_id,)
                ).fetchone()
                catalogue_subject = db.execute(
                    "SELECT name FROM subject_catalog WHERE id=? AND active=1",
                    (subject_id,),
                ).fetchone()
                if not target_class or not catalogue_subject:
                    flash_message("Choose an active class and catalogue subject.", "error")
                else:
                    existing = db.execute(
                        "SELECT id FROM subjects WHERE class_id=? AND name=?",
                        (class_id, catalogue_subject["name"]),
                    ).fetchone()
                    if existing:
                        db.execute(
                            "UPDATE subjects SET active=1 WHERE id=?", (existing["id"],)
                        )
                    else:
                        db.execute(
                            "INSERT INTO subjects(name, class_id) VALUES (?, ?)",
                            (catalogue_subject["name"], class_id),
                        )
                    flash_message("Subject assigned to class.")
        classes = db.execute(
            "SELECT id, name FROM classes WHERE active=1 ORDER BY name"
        ).fetchall()
        catalogue = db.execute(
            "SELECT id, name FROM subject_catalog WHERE active=1 ORDER BY name"
        ).fetchall()
        assignments = db.execute("""
            SELECT s.id, s.name, s.active, c.name AS class_name
            FROM subjects s JOIN classes c ON c.id=s.class_id
            ORDER BY c.name, s.name
        """).fetchall()
    return render_template(
        "assignments.html",
        classes=classes,
        catalogue=catalogue,
        assignments=assignments,
    )


@app.route("/report-config", methods=["GET", "POST"])
@login_required
def report_config():
    report_fields = (
        ("report_field_subject_average", "Subject average"),
        ("report_field_first_term", "1st term score"),
        ("report_field_second_term", "2nd term score"),
        ("report_field_cumulative", "Cumulative score"),
        ("report_field_grade", "Grade"),
        ("report_field_position", "Position"),
        ("report_field_remark", "Remark"),
    )
    with get_db() as db:
        if request.method == "POST":
            action = request.form.get("action", "save")
            if action == "save":
                values = {
                    key: request.form.get(key, "").strip()
                    for key in ("session", "school_name", "resumption_date", "closing_date")
                }
                values.update({
                    key: request.form.get(key, "").strip()
                    for key in (
                        "grade_a_min", "grade_b_min", "grade_c_min",
                        "grade_d_min", "grade_e_min",
                    )
                })
                try:
                    years = values["session"].split("/")
                    if (
                        len(years) != 2 or not all(year.isdigit() for year in years)
                        or int(years[1]) != int(years[0]) + 1
                    ):
                        raise ValueError("Session must use YYYY/YYYY and consecutive years.")
                    for key in ("resumption_date", "closing_date"):
                        datetime.strptime(values[key], "%Y-%m-%d")
                    grade_values = [
                        float(values[key]) for key in (
                            "grade_a_min", "grade_b_min", "grade_c_min",
                            "grade_d_min", "grade_e_min",
                        )
                    ]
                    if any(value < 0 or value > 100 for value in grade_values):
                        raise ValueError("Grade thresholds must be between 0 and 100.")
                    if grade_values != sorted(grade_values, reverse=True):
                        raise ValueError("Grade thresholds must descend from A through E.")
                    values.update({
                        key: str(int(key in request.form))
                        for key, _label in report_fields
                    })
                    for key, value in values.items():
                        db.execute(
                            "INSERT INTO config(key, value) VALUES (?, ?) "
                            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                            (key, value),
                        )
                    flash_message("Report card configuration saved.")
                except (ValueError, TypeError) as exc:
                    flash_message(str(exc), "error")
            elif action == "save_assessments":
                class_id = request.form.get("class_id", type=int)
                rows = db.execute(
                    "SELECT id, max_score, active FROM assessment_columns WHERE class_id=?",
                    (class_id,),
                ).fetchall()
                try:
                    updates = []
                    total = 0.0
                    for row in rows:
                        maximum = float(request.form.get(f"max_{row['id']}", ""))
                        active = int(f"active_{row['id']}" in request.form)
                        if not math.isfinite(maximum) or maximum <= 0:
                            raise ValueError("Assessment maximums must be greater than zero.")
                        if active:
                            total += maximum
                        updates.append((maximum, active, row["id"]))
                    if (
                        not updates or not math.isfinite(total)
                        or abs(total - 100) > 0.000001
                    ):
                        raise ValueError(f"Active assessment maximums must total 100 (currently {total:g}).")
                    db.executemany(
                        "UPDATE assessment_columns SET max_score=?, active=? WHERE id=?",
                        updates,
                    )
                    flash_message("Assessment columns saved.")
                except ValueError as exc:
                    flash_message(str(exc), "error")
            elif action == "add_assessment":
                class_id = request.form.get("class_id", type=int)
                name = request.form.get("assessment_name", "").strip()
                try:
                    maximum = float(request.form.get("assessment_max", ""))
                    if not name or not math.isfinite(maximum) or maximum <= 0:
                        raise ValueError("Enter a name and a positive maximum mark.")
                    order = db.execute(
                        "SELECT COALESCE(MAX(sort_order),0)+1 FROM assessment_columns WHERE class_id=?",
                        (class_id,),
                    ).fetchone()[0]
                    db.execute(
                        "INSERT INTO assessment_columns(class_id,name,max_score,sort_order) "
                        "VALUES (?,?,?,?)",
                        (class_id, name, maximum, order),
                    )
                    flash_message("Assessment column added. Adjust active maximums to total 100.")
                except ValueError as exc:
                    flash_message(str(exc), "error")
                except sqlite3.IntegrityError:
                    flash_message("That assessment column already exists for the class.", "error")
        values = dict(db.execute("SELECT key, value FROM config").fetchall())
        classes = db.execute(
            "SELECT id, name FROM classes WHERE active=1 ORDER BY name"
        ).fetchall()
        selected_class = request.values.get("class_id", type=int)
        if selected_class not in [row["id"] for row in classes]:
            selected_class = classes[0]["id"] if classes else None
        assessments = db.execute(
            "SELECT * FROM assessment_columns WHERE class_id=? ORDER BY sort_order,id",
            (selected_class,),
        ).fetchall() if selected_class else []
    return render_template(
        "report_config.html",
        values=values,
        report_fields=report_fields,
        classes=classes,
        selected_class=selected_class,
        assessments=assessments,
    )


@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    with get_db() as db:
        class_rows = db.execute("SELECT id, name FROM classes WHERE active=1 ORDER BY name").fetchall()
        session_name = db.execute("SELECT value FROM config WHERE key='session'").fetchone()[0]
        class_id = request.values.get("class_id", type=int) or (class_rows[0]["id"] if class_rows else None)
        term = request.values.get("term", type=int) or 1
        if term not in (1, 2, 3):
            term = 1

        if request.method == "POST":
            assessment_rows = db.execute(
                "SELECT id, name, max_score FROM assessment_columns "
                "WHERE class_id=? AND active=1",
                (class_id,),
            ).fetchall()
            maximums = {row["id"]: (row["name"], float(row["max_score"])) for row in assessment_rows}
            try:
                updates = []
                for key, value in request.form.items():
                    if not key.startswith("score_"):
                        continue
                    _, student_id, subject_id, assessment_id = key.split("_")
                    score = float(value)
                    name, maximum = maximums[int(assessment_id)]
                    if score < 0 or score > maximum:
                        raise ValueError(f"{name} must be between 0 and {maximum:g}.")
                    updates.append((int(student_id), int(subject_id), term, int(assessment_id), score))
                for update in updates:
                    db.execute(
                        "INSERT INTO result_scores(student_id, subject_id, term, assessment_id, score) "
                        "VALUES (?, ?, ?, ?, ?) "
                        "ON CONFLICT(student_id, subject_id, term, assessment_id) "
                        "DO UPDATE SET score=excluded.score",
                        update,
                    )
                flash_message("Results saved successfully.")
            except (TypeError, ValueError) as exc:
                flash_message(str(exc) or "Scores must be numeric.", "error")

        assessments = db.execute(
            "SELECT * FROM assessment_columns WHERE class_id=? AND active=1 ORDER BY sort_order, id",
            (class_id,),
        ).fetchall()
        subjects = db.execute(
            "SELECT * FROM subjects WHERE class_id=? AND active=1 ORDER BY name",
            (class_id,),
        ).fetchall()
        students = db.execute(
            "SELECT * FROM students WHERE class_id=? AND active=1 AND session=? ORDER BY name",
            (class_id, session_name),
        ).fetchall()
        saved = {
            (row["student_id"], row["subject_id"], row["assessment_id"]): row["score"]
            for row in db.execute(
                "SELECT student_id, subject_id, assessment_id, score "
                "FROM result_scores WHERE term=?",
                (term,),
            ).fetchall()
        }
    return render_template(
        "results.html",
        classes=class_rows,
        selected_class=class_id,
        term=term,
        assessments=assessments,
        subjects=subjects,
        students=students,
        saved=saved,
    )


@app.route("/generate", methods=["POST"])
@login_required
def generate():
    class_name = request.form.get("class_name", "")
    try:
        path = generate_workbook(class_name)
        return send_file(path, as_attachment=True)
    except Exception as exc:
        flash_message(str(exc), "error")
        return redirect(url_for("dashboard"))


@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "TPSA Result Manager",
        "short_name": "TPSA Results",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#f2f5f7",
        "theme_color": "#12304a",
        "icons": [
            {"src": "/static/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}
        ],
    })


@app.route("/sw.js")
def service_worker():
    return app.response_class(
        "const CACHE='tpsa-v1';"
        "self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE)));"
        "self.addEventListener('fetch',e=>{if(e.request.method==='GET')e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)));});",
        mimetype="application/javascript",
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=False)

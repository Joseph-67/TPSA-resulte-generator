import os
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
            "subjects": db.execute("SELECT COUNT(*) FROM subjects WHERE active=1").fetchone()[0],
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
            name = request.form.get("name", "").strip()
            admission_no = request.form.get("admission_no", "").strip()
            sex = request.form.get("sex", "Unknown").strip()
            class_id = request.form.get("class_id", type=int)
            if name and admission_no and class_id:
                try:
                    db.execute(
                        "INSERT INTO students(name, admission_no, class_id, sex, session) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (name, admission_no, class_id, sex, session_name),
                    )
                    flash_message("Student added successfully.")
                except Exception as exc:
                    flash_message(str(exc), "error")
            else:
                flash_message("Name, admission number, and class are required.", "error")
        rows = db.execute(
            "SELECT s.*, c.name AS class_name FROM students s "
            "JOIN classes c ON c.id=s.class_id "
            "WHERE s.active=1 AND s.session=? ORDER BY c.name, s.name",
            (session_name,),
        ).fetchall()
    return render_template(
        "students.html",
        students=rows,
        classes=class_rows,
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

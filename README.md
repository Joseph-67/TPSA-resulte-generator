# TPSA Result Manager

CustomTkinter desktop application for managing school users, students, classes,
subjects, term scores, result rules, and Excel report generation.

## Run

```powershell
python -m pip install -r requirements.txt
python desktop_app.py
```

## Desktop downloadable package

On Windows, run:

```powershell
.\build_windows.ps1
```

This creates `dist\TPSA Result Manager.exe`. Copy that executable to another
Windows computer and run it; no Python installation is required.

## Phone and browser installable package

Run the responsive web/PWA server:

```powershell
.\run_web.ps1
```

Open `http://<computer-ip>:8000` on the phone while both devices are on the
same network. In the browser menu choose **Install app** or **Add to Home
Screen**. HTTPS or localhost is required for full PWA installation.

The local SQLite database is `tpsa.db`. On first initialization, the app creates
the default administrator (`admin` / `admin123`) and imports the current
2026/2027 student list if the database has no students. Change the default
password immediately from **Manage Admins**.

## Administration features

- Create, deactivate, reactivate, and reset administrator accounts.
- Change your own password. New and reset passwords must be at least 12
  characters.
- Add students manually or import CSV/XLSX files with `Name` and `Admission No`
  columns (optional `Sex` column).
- Deactivate students without deleting their saved results.
- Configure school name, session, and term dates.
- Configure assessment columns by class: rename or add scored columns, set
  their maximum marks, and deactivate columns while retaining their historical
  scores. The active maximum marks must total 100.
- Choose which optional fields appear in generated report tables (subject
  average, prior-term scores, cumulative score, grade, position, and remark).
- Configure A–F minimum-grade thresholds.
- Add classes and class-specific subjects; deactivate subjects no longer used.
- Load the configured JS and SS student cohorts and subjects into the desktop
  database during initialization, including existing databases with students.
- Enter and save scores separately for each of the three terms.
- Generate an Excel workbook containing first-, second-, and third-term sheets
  for every active student in the selected class and configured session.

Generated workbooks are saved in
`final_3term_results\<start-year>-<end-year-short>\`.

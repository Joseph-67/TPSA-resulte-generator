# List of student names for Pre-Nursery II
preNurseryTwo = [
    "Ameh Telvin",
    "Itodo Prevail Ojumeyi",
    "Echekwu Kristine Chiaodi",
    "Assi Vitallis Abba",
    "Theophilus Ekerini Ekong",
    "Amaizu Bryan Chiemela",
    "Nze Chidiebere Derick",
    "Awa Adriel Obasioma",
    "Dalama David Oluwafemi",
    "Kayode Tiseoluwa",
    "Mgbemena Jidenna Kanu",
    "Oliver Valentine Chimnadindu",
    "Osaywamen Ethan Ehosa",
    "Ismail Habiba",
    "Idris Mohammed Zainab",
    "Sanusi Mohammad Moshood"
]

# Generate student data for Pre-Nursery II
students_data = []
for i, name in enumerate(preNurseryII, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"PN2/{str(i).zfill(3)}",
        "Class": "Pre-Nursery II",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Placeholder for gender
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Pre-Nursery II
class_data = {
    "Class": "Pre-Nursery II",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0
}

# Display the results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

# List of students in JS1D
js3 = [
    "Praise Micheal",
    "Jasmine Malomo",
    "Archiving Splendid",
    "Oigene Dominion",
    "Echekwu Daniella",
    "Awa Wealth",
    "Obe Princess",
    "Dickman Hylekumi",
    "Faith Adibe",
    "Amakoromo Faith",
    "Uchenna Stacie",
    "Adams Enoch",
    "Igbokwe Munachi",
    "Samson Micheal",
    "Sylvester Shalom",
    "Lucas Excel",
    "Alfred Bethel",
    "Ikani Oma-ojo Mabel",
]

# Generate individual student data
students_data = []
for i, name in enumerate(js3, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS3/{str(i).zfill(3)}",
        "Class": "JS 3",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Update if known
        "Section": " "
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 3",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 93.0,  # Adjust if needed
    "Coordinator": "Principal"
}

# Output both data
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

# List of student names for Grade Two
grade_two_diamond = [
    "Abraham Bethel",
    "Ayibaebi Wisdom",
    "Dimka Riyeh",
    "Ejeh Jedidiah",
    "Emubarsa Jared",
    "Ephrraim s. Praise",
    "Freancis chimamanda",
    "Ifedinru Chimamanda",
    "Ikechukwu Munachi",
    "Johnson Juana",
    "Oliver Chimamanda",
    "Raji gift",
    "Sasodje Annabel",
    "Ubah mitchelle"
]

# Generate student data for Grade Two
students_data = []
for i, name in enumerate(grade_two_diamond, start=1):
    student = {
        "Name": name,
        "Admission No": f"G2/{str(i).zfill(3)}",
        "Class": "Grade Two",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Can be updated later
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Grade Two
class_data = {
    "Class": "Grade Two",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0,
    "Coordinator": "Head Teacher" 
}

# Display results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

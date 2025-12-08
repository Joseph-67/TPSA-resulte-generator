# List of student names for Grade One Gold
gradeTwoGold =  [
    "Abraham Bethel",
    "Ayibaebi Wisdom",
    "Dimka Riyel",
    "Ejeh Jedidiah",
    "Emubarsa Jared",
    "Ephraim S. Praise",
    "Francis Chimamanda",
    "Ifediniru Chimamanda",
    "Ikechukwu Munaeli",
    "Johnson Jaana",
    "Oliver Chimamanda",
    "Raji Gift",
    "Sasodje Annabel",
    "Ubah Mitchelle"
]

# Generate student data for Grade One Gold
students_data = []
for i, name in enumerate(gradeTwoGold, start=1):
    student = {
        "Name": name,
        "Admission No": f"G1G/{str(i).zfill(3)}",
        "Class": "Grade Two",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Can be updated later
        "Section": "Gold"
    }
    students_data.append(student)

# Class-level data for Grade One Gold
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

# Displaying the results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

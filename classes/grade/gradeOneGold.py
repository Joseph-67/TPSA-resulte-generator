# List of student names for Grade One Gold
gradeOneGold = [
    "Abraham Odinaka Bethel",
    "Animasahun Abiodun Samirah",
    "Ayibaebi Wisdom",
    "Dimka Riyeh",
    "Ejeh Ihortu Jedidiah",
    "Emubarsa Jared Matthew",
    "Francis Clare Chimamanda",
    "Ikechiuku Treasure Munachi",
    "Johnson Ochanya Jaana",
    "Oliver Valentine Chimamanda",
    "Raji Irewa Gift",
    "Stanley Sasodje Annabel",
    "Ubah Michelle"
]

# Generate student data for Grade One Gold
students_data = []
for i, name in enumerate(gradeOneGold, start=1):
    student = {
        "Name": name,
        "Admission No": f"G1G/{str(i).zfill(3)}",
        "Class": "Grade One",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Can be updated later
        "Section": "Gold"
    }
    students_data.append(student)

# Class-level data for Grade One Gold
class_data = {
    "Class": "Grade One",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
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

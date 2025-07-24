# List of student names
gradeOneDiamond = [
    "Adams Utenojo Kadosh",
    "Akinade Anuoluwapo Dominion",
    "Christopher Daniel",
    "Enang Praise",
    "GoodFriday WoyinTari-Ere Timipah",
    "Haruna Salem Goma",
    "KingJames Wendy Barisua",
    "Kanu-Mgbemena Tobechukwu",
    "Muhammed Bilkisu",
    "Nosakhare Henry Osarodion",
    "Nwokoshiyole Munachi Light of God",
    "Oloniyo Queen-Esther",
    "ANTHONY CHIMAMADA KENDRA"
]

# Generate student data
students_data = []
for i, name in enumerate(gradeOneDiamond, start=1):
    student = {
        "Name": name,
        "Admission No": f"G1D/{str(i).zfill(3)}",
        "Class": "Grade One",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder
        "Section": "Diamond"
    }
    students_data.append(student)

# Class-level data
class_data = {
    "Class": "Grade One",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0,  # You can update this value dynamically if needed
    "Coordinator": "Head Teacher",  # Placeholder
}

# Output both variables
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

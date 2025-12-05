# List of students in JS1D
js1D = [
    "Adams Ayodeji ",
    "Adams Emmanuel",
    "Alfred Bethel Oluwafikayomi",
    "Anaele Marvelous",
    "Anaele Micheal",
    "Owulo Onah",
    "Noah Naomi",
    "Matthas Gianne ",
    "Sylvester C. Havilah",
    "Uchenna Stacie",
    "Amakoromo Faith"
]

# Generate individual student data
students_data = []
for i, name in enumerate(js1D, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS1D/{str(i).zfill(3)}",
        "Class": "JS 1 D",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Update if known
        "Section": "General"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 1 D",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
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

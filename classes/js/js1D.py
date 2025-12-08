# List of students in JS1D
js1D = [
    "Abdulmajid S. Nabila",
    "Adegoke O. Joshua",
    "Akobeitopa Susan",
    "Ayodeji E. Precious",
    "Bassey O. Godwin",
    "Chukwudi A. Greta",
    "Ekpe V. Avina",
    "Enoch M. Sharon",
    "Gabriel K. Alvin",
    "Jiriko N. Mathias",
    "Lukas Purity",
    "Seth S. Terry",
    "Simon E. Favour",
    "Sylvester A. Favour"
]

# Generate individual student data
students_data = []
for i, name in enumerate(js1D, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS1D/{str(i).zfill(3)}",
        "Class": "JS 1 ",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Update if known
        "Section": "Diamond"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 1",
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

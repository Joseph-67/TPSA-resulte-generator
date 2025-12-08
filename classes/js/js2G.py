# List of students in JS1D
js1D = [
     "Akwarandu Michael C.",
    "Abah Ehi Pauline",
    "Bamidele Hepzibah O.",
    "Elijah Peniel O.",
    "Enoch Sarah",
    "Femowei Nehemiah O.",
    "Iheanacho J. Uchenna",
    "Jude Gift O.",
    "Noble Mathias",
    "Ojo J. Moyosoreoluwa",
    "Ofurum Michele K.",
    "Sasodje Zoe K.",
    "Tim-Udzer D. Claribel",
    "Zira Divine H."
]

# Generate individual student data
students_data = []
for i, name in enumerate(js1D, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS1D/{str(i).zfill(3)}",
        "Class": "JS 1",
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

ss1art = [
  "Odum Harmony"
]

# Generate student data
students_data = []
for i, name in enumerate(ss1art, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"SS1A/{str(i).zfill(3)}",
        "Class": "SS 1 Art",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",
        "Section": "Art"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "SS 1 Art",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0  # You can adjust this
}

# Output both
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

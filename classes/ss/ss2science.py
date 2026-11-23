ss2science = [
    "Adebayo A. Princess",
    "Emmanuel J. Marcus",
    "Lanloye E. Ololade",
    "Lawrence O. Angel",
    "Mathew E. Grace",
    "Olurotimi O. Emmanuel",
    "Onyealum F. Chioma"
]

# Generate student data for SS 2 Science
students_data = []
for i, name in enumerate(ss2science, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"SS2S/{str(i).zfill(3)}",
        "Class": "SS 2 Science",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # You can update this if known
        "Section": "Science"
    }
    students_data.append(student)

# Create class-level data
class_data = {
    "Class": "SS 2 Science",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0  # Example placeholder
}

# Output results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

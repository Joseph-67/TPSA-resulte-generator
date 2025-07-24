ss2art = [
    "Eze E. Esther",
    "Gopala Victor"
]

# Generate student data for SS 2 Art
students_data = []
for i, name in enumerate(ss2art, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"SS2A/{str(i).zfill(3)}",
        "Class": "SS 2 Art",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Update if known
        "Section": "Art"
    }
    students_data.append(student)

# Create class-level data
class_data = {
    "Class": "SS 2 Art",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0  # Example placeholder
}

# Output results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

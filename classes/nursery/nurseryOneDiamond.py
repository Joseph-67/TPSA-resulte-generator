# List of student names for Nursery One Diamond
nurseryOneDiamond = [
    "Abdulrasaq Afsheen Enehezeyi",
    "Goodfriday Ayibatari-Emitimipah",
    "Aiya Derick Ehizokhar",
    "Solomon James Magodeshekwoyi",
    "Ameh Ejebabi John",
    "Muhammed Ahmed Lukman",
    "Lucky Mishael Ovie",
    "Ubah Michael",
    "Peniel Enang"
]

# Generate student data for Nursery One Diamond
students_data = []
for i, name in enumerate(nurseryOneDiamond, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"N1D/{str(i).zfill(3)}",
        "Class": "Nursery One Diamond",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder for gender
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Nursery One Diamond
class_data = {
    "Class": "Nursery One Diamond",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0
}

# Display the results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

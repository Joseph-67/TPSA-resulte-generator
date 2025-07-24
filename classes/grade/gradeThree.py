# List of student names for Grade Three
gradeThree = [
    "AbdulWaheed Muhsin",
    "Agbonlahor Joy Owen",
    "Akobe Itopa Sharon",
    "Aliu Cherish",
    "Ameh Benedict Ojongungwa",
    "Awa Prudence Nkemruturym",
    "Ayibaebi Brighen",
    "Igbokwe Chibusoma Favour",
    "Lucky Samuel Ejiro",
    "Oigene  Steed Edoh ",
    "Seth Tamara Sambo",
    "Ubah Dominic Kachi",
    "EZEANYA BELUSOCHUKWU FRANKLYN JNR"
]

# Generate student data for Grade Three
students_data = []
for i, name in enumerate(gradeThree, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"G3/{str(i).zfill(3)}",
        "Class": "Grade Three",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Grade Three
class_data = {
    "Class": "Grade Three",
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

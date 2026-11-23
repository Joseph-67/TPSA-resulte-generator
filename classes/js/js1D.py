# List of students in JS1D
js1D = [
    "Samson Michelle Micheal",
    "Kappe Jesselyn Jonathan",
    "Terhember Sedoo Marvis",
    "Munachi Francis Obasi",
    "Gabriella Archiving",
    "Nathaniel Ameh",
    "Ben Oryiman Savior",
    "Precious A. Ajibade",
    "Echekwu Uche Hilda",
    "Delight Daniel",
    "Splendor Chkaima",
    "Alexander Enoabasi Utah",
    "Happiness Uto",
    "Joshua Amucheazi",
    "Emeka Jesse",
    "Success Amos",
    "Prudence Enang",
    "Racheal Tsala Dollars",
]

# Generate individual student data
students_data = []
for i, name in enumerate(js1D, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS1D/{str(i).zfill(3)}",
        "Class": "JS 1 ",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Update if known
        "Section": "Diamond"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 1",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
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

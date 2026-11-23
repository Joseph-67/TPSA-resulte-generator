# List of students in JS1 Gold
js1G = [
    "Olorunleke Melody",
    "Ewe Joana",
    "Yerima Kayla F.",
    "Taiwo Boluwatife",
    "Alexander Mfonabasi Utah",
    "Jesse Lar Nankpan",
    "Martins Johnson",
    "Odebunmi Andrew",
    "Buhari Bashar Zakaria",
    "Opakunle Victor",
    "Ibrahim Yakubu",
    "Gift Stephen",
    "David Adibe",
    "Cherish Monday",
    "Subah Collins",
    "Stephen Osinanchi Immaculate",
    "Jeffrey Solomon",
    "Chimamanda Richard",
]

# Generate individual student data
students_data = []
for i, name in enumerate(js1G, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS1G/{str(i).zfill(3)}",
        "Class": "JS 1",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Update if known
        "Section": "Gold"
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

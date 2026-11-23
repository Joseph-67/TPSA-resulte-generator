# List of students in JS2 Gold
js2G = [
    "Peniel Elijah",
    "Claribel Tim-Udzer",
    "Hephzibah Bamidele",
    "Gift Jude",
    "Nehemiah Femowei",
    "Divine Zira",
    "Sarah Enoch Musa",
    "Unande Vivian",
    "Noble Matthias",
    "Sasodje Zoe",
    "Akwarandu Micheal",
    "Uchenna Justus Iheanacho",
    "Ehi Abah Poline",
    "Chukwuemeka Emmanuella",
    "Kamsy Ofurum",
]

# Generate individual student data
students_data = []
for i, name in enumerate(js2G, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS2G/{str(i).zfill(3)}",
        "Class": "JS 2",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Update if known
        "Section": "Gold"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 2",
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

# List of student names for Nursery Two
nurseryTwo = [
    "Adams Yahaya",
    "Adewumi John Joel",
    "Agida Mildred",
    "Agu Chinedum",
    "Ameh Telvin",
    "Awa Obasioma Adrian",
    "Chigereokwu C. Daniel",
    "Dalamu O. David",
    "Echekwu C. Kristine",
    "Eghosa Ethan",
    "Geofrey Doris",
    "Idris Muhammed Zainab",
    "Ikedichi Ivan-Bright",
    "Indah Nerriah",
    "Ismail Habiba",
    "Jiriko Zuriel",
    "John Joel Ojonemile",
    "Johnson A. Richwell",
    "Kayode C. Oluwatise",
    "Madiagu Herald",
]

# Generate student data for Nursery Two
students_data = []
for i, name in enumerate(nurseryTwo, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"N2/{str(i).zfill(3)}",
        "Class": "Nursery Two",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # You can fill actual gender if known
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Nursery Two
class_data = {
    "Class": "Nursery Two",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0
}

# Display student and class data
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

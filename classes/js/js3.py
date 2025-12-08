# List of students in JS1D
js3 = [
    "Abonyi Collette O",
    "Adegboyega Angel",
    "Adebayo Samuel",
    "Alhamdu Grace",
    "Akwarandu Emmanuel",
    "Ameh Victory",
    "Axel Gabriel",
    "Bamidele Elizabeth",
    "Bassey Miracle",
    "Daniel David",
    "Emekwe Faith",
    "Emmanuel Bettina",
    "Ewe Vanessa",
    "Friday Ekene",
    "Idris Muhammed",
    "Kerry-Taiwo Wonder",
    "Jacob Gracious",
    "Michael Sharon",
    "Obasi Angel",
    "Oche Isabella",
    "Jude Joash",
    "Olurotimi Joshua",
    "Olurotimi Joseph",
    "Enang Prosper",
    "Onuh Samuel",
    "Sasodje Alex"
]

# Generate individual student data
students_data = []
for i, name in enumerate(js3, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS1D/{str(i).zfill(3)}",
        "Class": "JS 3",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Update if known
        "Section": " "
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 3",
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

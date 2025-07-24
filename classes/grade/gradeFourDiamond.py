# List of student names for Grade Four Diamond
gradeFourDiamond = [
    "Abel Loretta Chubiyojo",
    "Adibe Chimeuba David",
    "Ameh Ofowecho Nathaniel",
    "Ayodele Damilare Louis",
    "Echekwu Ucheh Hilda",
    "Ewe Ulyamachuwe Joanna",
    "Eze Amarachi Anastasia",
    "Goodfriday Tarimobowei",
    "Haruna Dasa Stephanie",
    "Ibrahim Olorundare Ismail",
    "Jonathan Kappe Jesslyn",
    "Olorunleke Ogoluwa Melody",
    "Solomon Shekwodeza Jeffery",
    "Uba Chizaram Collins",
    "Uka Onyedikachukwu Emmanuel"
]

# Generate student data for Grade Four Diamond
students_data = []
for i, name in enumerate(gradeFourDiamond, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"G4D/{str(i).zfill(3)}",
        "Class": "Grade Four",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder
        "Section": "Diamond"
    }
    students_data.append(student)

# Class-level data for Grade Four Diamond
class_data = {
    "Class": "Grade Four",
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

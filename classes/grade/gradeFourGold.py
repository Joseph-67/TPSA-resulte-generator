# List of student names for Grade Four Gold
gradeFourGold = [
    "Abraham Bryan Osinachi",
    "Attah Adam Attah",
    "Akpati David Ifeakachukwu",
    "Archibong Gabriella",
    "Assi Alexis Stephen",
    "Daniel Delight Pipkong",
    "Francis Blaise Munachimuso",
    "Lar Nankpah Jesse",
    "Ngene Franklin Ebubechukwu",
    "Raji Oluwapamilerin Gold",
    "Stephen Immaculate Osinachi",
    "Yakubu Ibrahim Udaba",
    "Ige Deborah Mercy"
]

# Generate student data for Grade Four Gold
students_data = []
for i, name in enumerate(gradeFourGold, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"G4G/{str(i).zfill(3)}",
        "Class": "Grade Four",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder
        "Section": "Gold"
    }
    students_data.append(student)

# Class-level data for Grade Four Gold
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

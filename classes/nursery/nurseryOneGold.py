# List of student names for Nursery One Gold
nurseryOneGold = [
    "Abayomi Abdulrasaq Abayomi",
    "Atom Ivan",
    "Ajibola  Khalid Oche",
    "Anyadike Chukwuebuka Elliot",
    "Bukar Jamila",
    "David Joan",
    "Emmanuel Peace Eleojo",
    "Emmanuel Joy Enyojo",
    "Isaac Henrybright Ojochegbe",
    "Mustapha Ahmad Lawal",
    "Nnameka Kambili Chiam",
    "Okafor Amazing",
    "Owulo Olieje Henrick",
    "Oladipopu Anita Adeola",
    "Promise Favour Ojochegbe",
    "Igoche Joan",
    "Anthony E. Kamsiyochukwu"
]

# Generate student data for Nursery One Gold
students_data = []
for i, name in enumerate(nurseryOneGold, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"N1G/{str(i).zfill(3)}",
        "Class": "Nursery One Gold",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder for gender
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Nursery One Gold
class_data = {
    "Class": "Nursery One Gold",
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

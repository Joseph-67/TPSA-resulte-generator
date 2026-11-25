# List of student names for Nursery One Gold
nurseryOneGold = [
    "Josiah Lushan Star",
    "Moses Isabella Eboh",
    "Nwamaka Chisom Kimberly",
    "Okon Deborah",
    "Okaka Charles Chiemerie",
    "Ogunrombi Eliora",
    "Oluwaseyi Florish Mokuneayo",
    "Terseer Beatrice Mesuur",
    "Tongark Ritmwa Sekani",
    "Muhammed Khalid Zakari",
    "Elele Star Souton",
    "Elele Soar Souyo",
    "Oluwatobiloba Evans Okungboye",
    "Samuel Cassiel",
    "Ikechukwu Abraham",
    "Ugwu Osinachi Kendrick",
    "Tana Zephan Ogbohifo",
]

# Generate student data for Nursery One Gold
students_data = []
for i, name in enumerate(nurseryOneGold, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"N1G/{str(i).zfill(3)}",
        "Class": "Nursery One Gold",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Placeholder for gender
        "Section": "Gold"
    }
    students_data.append(student)

# Class-level data for Nursery One Gold
class_data = {
    "Class": "Nursery One Gold",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0
}

# Display the results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

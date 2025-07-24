# List of student names for Pre-Nursery One
preNurseryOne = [ 
    "Agu Chinedum Diewdonne", 
    "Haggai Henry Haruna", 
    "Josiah Lushan Star", 
    "Okon Deborah", 
    "Okoye Brandon Ifeanyichukwu", 
    "Okaka Charles Chinemerie", 
    "Ogunrombi Eliora", 
    "Terseer Mesuur Beatrice", 
    "Okunlola Elijah Morireoluwa"
]

# Generate student data for Pre-Nursery One
students_data = []
for i, name in enumerate(preNurseryOne, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"PN1/{str(i).zfill(3)}",
        "Class": "Pre-Nursery One",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Pre-Nursery One
class_data = {
    "Class": "Pre-Nursery One",
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

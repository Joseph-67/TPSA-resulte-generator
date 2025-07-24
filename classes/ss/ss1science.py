ss1science = [ 
  "Adams Flourish",
  "Akindigh Keziah",
  "Assi Alison",
  "Chukwudi Lucian",
  "Ejigah ThankGod",
  "Innocent Cecilia",
  "Kerry-Taiwo Treasure",
  "Kingjames Bianca",
  "Noah Joseph",
  "Olorunleke Michael"
]

# Generate student data for SS 1 Science
students_data = []
for i, name in enumerate(ss1science, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"SS1S/{str(i).zfill(3)}",
        "Class": "SS 1 Science",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Placeholder; update if known
        "Section": "Science"
    }
    students_data.append(student)

# Create class-level data
class_data = {
    "Class": "SS 1 Science",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0  # Adjust if needed
}

# Display the student data and class data
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

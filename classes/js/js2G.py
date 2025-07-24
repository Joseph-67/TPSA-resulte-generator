js2G = [
  "Agunbiade Peace",
  "Alhamdu Grace",
  "Ameh Victory",
  "Adegboyega Angel",
  "Daniel David",
  "Enang Prosper",
  "Emmanuel Betting",
  "Gabriel Axel",
  "Kerry Taiwo Wonder",
  "Mmaduka Success",
  "Obasi Angel Ndubisi",
  "Olurotimi Joseph",
  "Sanusi Raheemat",
  "Sadaojie  Alexander",
  "Too Chidume Rex Leo"
]

# Generate student data
students_data = []
for i, name in enumerate(js2G, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS2G/{str(i).zfill(3)}",
        "Class": "JS 2 G",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",
        "Section": "General"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 2 G",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 91.5  # Optional placeholder
}

# Return both
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

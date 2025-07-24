js2D = [
  "Ewe Vanessa",
  "Onuh Samuel",
  "Eze Casmir",
  "Adegoke Samuel",
  "Oche Isabella",
  "Davdonald Arella",
  "Michael Sharon",
  "Olurotimi Joshua",
  "Akwaranadu Emmanuel",
  "Jude Joash",
  "Bamidele Elizabeth",
  "Ochi Destiney",
  "Bassey Miracle",
  "Jacob Gracious"
]

# Generate student data
students_data = []
for i, name in enumerate(js2D, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS2D/{str(i).zfill(3)}",
        "Class": "JS 2 D",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",
        "Section": "General"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "JS 2 D",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 93.2  # You can adjust this as needed
}

# Return both
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

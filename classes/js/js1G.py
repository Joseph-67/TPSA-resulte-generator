js1G = [
  "Awa Wealth Chiamanda",
  "Assi Joshua Anderson",
  "Adibe Faith Chinesom",
  "Archibong Splendid A",
  "Hindan Vivian Mimidoo",
  "Michael Praise Oluwadamilola",
  "Malomo Jasmine F.",
  "Mathew Tehillah K.",
  "Obe Princess Miracle",
  "Oigene Dominion Daniels",
  "Owulo Onah Henry",
  "Thomas Great Courage",
  "Echeku Daniella"
]

# Generate student data
students_data = []
for i, name in enumerate(js1G, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"JS1G/{str(i).zfill(3)}",
        "Class": "JS 1 G",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Optional field, update if available
        "Section": "General"
    }
    students_data.append(student)

# Class-wide data dictionary
class_data = {
    "Class": "JS 1 G",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 93.0  # Optional placeholder
}

# Output
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

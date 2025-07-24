# List of student names for Grade Two
gradeTwo = [ 
  "Abel Isabel", 
  "Atom .Z. Adel", 
  "Ayodele Adrian",
  "Ayodele Peniel", 
  "Dickman Hyehirra Crown", 
  "Joseph Meekness", 
  "Lar Chloe", 
  "Mohammed Abdulhameed", 
  "Ndackson Joel", 
  "Nze Ifeoma Mirabel", 
  "Oladipupo Ann", 
  "Onyekachi Precious", 
  "Onyedikachi Mmesoma", 
  "Owulo Harris", 
  "Stephen Somtochukwu", 
  "Friday Kamsiyochukwu Wisdom"
]

# Generate student data for Grade Two
students_data = []
for i, name in enumerate(gradeTwo, start=1):
    student = {
        "Name": name,
        "Admission No": f"G2/{str(i).zfill(3)}",
        "Class": "Grade Two",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Can be updated later
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Grade Two
class_data = {
    "Class": "Grade Two",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0
}

# Display results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

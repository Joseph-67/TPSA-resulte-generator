# List of student names for Grade One Gold
gradeThree = [
    "Abel Isabella",
    "Adebayo Michael",
    "Atom Z. Adel",
    "Ayodele Adrian Ifeoluwa",
    "Dickman Hyeh Hyehhirra",
    "Ekpe Ivaan Hubert",
    "Joseph Meekness",
    "Kayode Boluwatife Gideon",
    "Lar Chloe",
    "Mathew Femiimilayo Paulina",
    "Mohammad Abdulhameed Zakari",
    "Ndackson Joel",
    "Oforium Munachosom M.",
    "Nze Ifeoma Mirabel",
    "Onyedikachi Mmesoma Princess",
    "Olapupo Ann Adesewa",
    "Onyekachi Precious",
    "Owulo Harris",
    "Stephen Somtochukwu",
    "Friday Kamasiochukwu Wisdom",
    "Ayodele Peniel"
]

# Generate student data for Grade One Gold
students_data = []
for i, name in enumerate(gradeThree, start=1):
    student = {
        "Name": name,
        "Admission No": f"G1G/{str(i).zfill(3)}",
        "Class": "Grade Three",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Can be updated later
        "Section": " "
    }
    students_data.append(student)

# Class-level data for Grade One Gold
class_data = {
    "Class": "Grade Three",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0,
    "Coordinator": "Head Teacher"
}

# Displaying the results
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

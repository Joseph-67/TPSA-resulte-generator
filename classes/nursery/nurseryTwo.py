# List of student names for Nursery Two
nurseryTwo = [
    "Amaizu Chisom Barbara",
    "Abdulwaheed Haadiya Onize",
    "Ayodele Pharez Oluwapelumi",
    "Adam Abdulmumin Onimisi",
    "Echekwu Fina Chinyere",
    "Eghosa Umammenosa Nathaniel",
    "Emmanuel Kingjesse Oche",
    "Emezuom Wisdom Obichukwu",
    "Johnson Jaqzah Ojoanya",
    "Kayode Tiwaloluwa Dumebi",
    "Mark Prince-excel",
    "Mohammed Yasir Zakari",
    "Nze Nora Oluchi",
    "Okon Jayden",
    "Uzuegbu Chisom Stanley",
    "Yakubu Mateenah Oko’osu",
    "William Eno Elianagreat",
    "Magnificent Godspower", 
    "Agbo Samuel Chinonso", 
    "Friday Dominion Kosi", 
    "Udogo Stella Oluhi"
]

# Generate student data for Nursery Two
students_data = []
for i, name in enumerate(nurseryTwo, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"N2/{str(i).zfill(3)}",
        "Class": "Nursery Two",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # You can fill actual gender if known
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Nursery Two
class_data = {
    "Class": "Nursery Two",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0
}

# Display student and class data
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

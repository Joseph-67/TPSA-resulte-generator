# List of students in JS1D
SS1D = [
    "Adebayo Moturanyo Mercy",
    "Anyiam Amarachi Goodness",
    "Dominic Oryiman Saviour",
    "Emmanuel Enemona Dean",
    "Lawrence Chinemerem Emelda",
    "Lucky Odamesa Joanna",
    "Ndackson Chinedu Joshua",
    "One Adah Prince",
    "Okpanah Obi Emmanuel",
    "Solomon Shekoyamilo Joan",
    "Sylvester God's Power",
    "Tanko Mohammed Hadiza",
    "David Rejoice Lisa"
]

# Generate individual student data
students_data = []
for i, name in enumerate(ss1D, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"SS1D/{str(i).zfill(3)}",
        "Class": "SS 1 ",
        "Term": "Third Term",
        "Session": "2024/2025",
        "Sex": "Unknown",  # Update if known
        "Section": "Diamond"
    }
    students_data.append(student)

# Class-wide data
class_data = {
    "Class": "SS 1",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Resumption Date": "2024-09-01",
    "Closing Date": "2025-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 93.0,  # Adjust if needed
    "Coordinator": "Principal"
}

# Output both data
print("STUDENTS DATA:")
for student in students_data:
    print(student)

print("\nCLASS DATA:")
print(class_data)

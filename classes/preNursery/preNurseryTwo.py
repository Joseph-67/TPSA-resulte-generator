# List of student names for Pre-Nursery II
preNurseryTwo = [
    "Adakole Asher Frank",
    "Abbey Jesse Excel",
    "Abel Arabella Ojonemile",
    "Ajibola Zeenat",
    "Adewumi Shalom Oluwamurewa",
    "Bulus Elizabeth Excel",
    "Chigereokwu Esther Amarachi",
    "Dalamu Jeshurun Femi",
    "Enyinnaya Josiah Chimeremeze",
    "Emmanuel Arielle En'ada",
    "Ejigah Tiffany",
    "Ismail Rahama",
    "Johnson Uriel",
    "John Eliana Ifeoma",
    "John Jesse Ojochegbe",
    "Mudiaga Eliana",
    "Muhammad Khadija Aroke",
    "Nnanenwu Chinecherem Susan",
    "Nnaemeka Janick",
    "Nkemakolam Peculiar",
    "Nwasike Jesse",
    "Negedu Raphael Enyo-ojo",
    "Okechukwu Chukwudubem Dominion",
    "Oladipupo Anajah",
    "Osagiede Tobechukwu Triumph",
    "Odumah Eugene Odionosele",
    "Onyemaobinna Creed Naetochukwu",
    "Onyekachi Chiamaka Jennifer",
    "Opakunle Victory Olamidunsy",
    "Olufemi Divine-Favour",
    "Solomon Jovani Jakada",
    "Yahaya Abdullahi Adams"
]

# Generate student data for Pre-Nursery II
students_data = []
for i, name in enumerate(preNurseryTwo, start=1):
    student = {
        "Name": name.strip(),
        "Admission No": f"PN2/{str(i).zfill(3)}",
        "Class": "Pre-Nursery II",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",  # Placeholder for gender
        "Section": "General"
    }
    students_data.append(student)

# Class-level data for Pre-Nursery II
class_data = {
    "Class": "Pre-Nursery II",
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

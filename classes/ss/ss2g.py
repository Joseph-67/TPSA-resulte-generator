ss2g = [
    "Tracy Simeon",
    "Testimony Ifeanyi",
    "Jeremiah Ekezie",
    "Fortune Monday",
    "Freedomfrank Ihiale",
    "Judah Adegboyega",
    "Jesse Kappe Jonathan",
    "Marvelous Akubor",
    "Wueseter Praise Barnabas",
    "Leora Chukwudi",
    "Jethro Solomon",
]

students_data = [
    {
        "Name": name,
        "Admission No": f"SS2G/{index:03d}",
        "Class": "SS 2",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",
        "Section": "Gold",
    }
    for index, name in enumerate(ss2g, start=1)
]

class_data = {
    "Class": "SS 2",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 93.0,
    "Coordinator": "Principal",
}

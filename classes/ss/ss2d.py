ss2d = [
    "Lucky Joanna",
    "Mordi Daniella",
    "Lawrence Emelda",
    "David Lisa",
    "Obe Prince",
    "Tanko Hadiza",
    "Sylvester Gods Power",
    "Emmanuel Dean",
    "Anyiam Amarachi",
    "Mercy Adebayo",
    "Solomon Joan",
]

students_data = [
    {
        "Name": name,
        "Admission No": f"SS2D/{index:03d}",
        "Class": "SS 2",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",
        "Section": "Diamond",
    }
    for index, name in enumerate(ss2d, start=1)
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

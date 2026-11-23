ss3 = [
    "Innocent Cecilia",
    "Treasure Kerry-Taiwo",
    "David Ogunleye",
    "Akindigh Keziah Mwuese",
    "Adams Flourish",
    "Oluwatomisin Olubode",
    "Ikeichukwu Harmony Odum",
    "Igbokwe Kelvin",
    "Olorunleke Micheal",
    "Lucian Chukwudi",
    "Dyo Christiana",
]

students_data = [
    {
        "Name": name,
        "Admission No": f"SS3/{index:03d}",
        "Class": "SS 3",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",
        "Section": "",
    }
    for index, name in enumerate(ss3, start=1)
]

class_data = {
    "Class": "SS 3",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 93.0,
    "Coordinator": "Principal",
}

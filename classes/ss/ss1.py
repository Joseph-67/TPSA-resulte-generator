ss1 = [
    "Colette Ogechukwu Abonyi",
    "Jason Gadiama",
    "Miracle Bassey",
    "Obasi Angel",
    "Bamidele Elizabeth",
    "Micheal Sharon",
    "Odebunmi Ololade",
    "Adegboyega Angel",
    "Sasodje Alexander",
    "Christopher Ann Menai",
    "Idris Mohammed",
    "Emeka Prince Peter",
    "Jude Joash Chimela",
    "Kerry-Taiwo Wonder Ayideji",
    "Samuel Adegoke",
    "Enang Prosper",
    "David Shamkong Daniel",
    "Onuh Samuel",
    "Jacob Gracious",
    "Oche Isabella",
    "Emmanuel Bettina",
    "Friday Ekene",
    "Adebayo Ayideji",
    "Alhamdu Grace",
    "Natasha Anjorin",
]

students_data = [
    {
        "Name": name,
        "Admission No": f"SS1/{index:03d}",
        "Class": "SS 1",
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",
        "Section": "",
    }
    for index, name in enumerate(ss1, start=1)
]

class_data = {
    "Class": "SS 1",
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 93.0,
    "Coordinator": "Principal",
}

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, Reference
from datetime import datetime

# --- Sample student data for one student offering 14 subjects ---
subjects = [
    "Mathematics", "English", "Biology", "Physics", "Chemistry", "Geography", "Economics",
    "Agriculture", "Civic Education", "History", "Computer", "Fine Arts", "French", "Physical Education"
]
student_scores = [
    {"Subject": sub, "CA1": 0, "CA2": 0, "CA3": 0, "Exam": 0,
     "1st Term": 0, "2nd Term": 0, "3rd Term": None} for sub in subjects
]
df = pd.DataFrame(student_scores)

wb = Workbook()
ws = wb.active
ws.page_setup.fitToHeight = 1
ws.page_setup.fitToWidth = 1
ws.title = "John Doe"

# --- Set column widths for neat layout ---
col_widths = [18, 7, 7, 7, 7, 13, 10, 10, 13, 8, 8, 15]
for i, w in enumerate(col_widths, 1):
    ws.column_dimensions[chr(64+i)].width = w

# --- Styling ---
header_font = Font(name="Times New Roman", bold=True, size=36, shadow=True)
sub_header_font = Font(name="Times New Roman", bold=True, size=16, shadow=True)
title_font = Font(name="Times New Roman", bold=True, size=12, shadow=True)
section_fill = PatternFill("solid", fgColor="DDDDDD")
center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

# --- 1. Sheet Title & Header ---
ws.merge_cells('A1:L1')
ws['A1'] = "TOPSTEPS ACADEMY"
ws['A1'].font = header_font
ws['A1'].alignment = center_align
ws.row_dimensions[1].height = 30

# --- Sub Header Section ---
ws.merge_cells('A2:L2')
ws['A2'] = "SECOND TERM 2024/2025 SESSION ACADEMIC REPORT"
ws['A2'].font = sub_header_font
ws['A2'].alignment = center_align
ws['A2'].fill = section_fill
ws.row_dimensions[2].height = 22

# Insert logo
logo = Image("tpsa_logo.png")
logo.width, logo.height = 70, 70
ws.add_image(logo, "L1")

# --- 2. Student Bio Data ---
from openpyxl.styles import Alignment
bio_data = {
    "Name": "John Doe",
    "Admission No": "STA/234",
    "Class": "SS2",
    "Term": "Third Term",
    "Session": "2024/2025",
    "Sex": "Male",
    "Age": "16"
}

ws.merge_cells('B3:F3')
ws.merge_cells('G3:H3')
ws.merge_cells('I3:L3')
ws.merge_cells('B4:C4')
ws.merge_cells('E4:F4')
ws.merge_cells('G4:H4')
ws.merge_cells('I4:L4')
ws.merge_cells('B5:L5')
ws.merge_cells('A7:L7')

ws['A3'] = "Student Name: "
ws['B3'] = bio_data["Name"]
ws['A3'].font = title_font
ws['B3'].font = title_font
ws['A3'].alignment = Alignment(horizontal="right")
ws['B3'].alignment = center_align
ws['A3'].border = border
ws['B3'].border = border
ws['C3'].border = border
ws['D3'].border = border
ws['E3'].border = border
ws['F3'].border = border
ws['G3'] = "Admission No: "
ws['I3'] = bio_data["Admission No"]
ws['G3'].font = title_font
ws['I3'].font = title_font
ws['G3'].alignment = Alignment(horizontal="right")
ws['I3'].alignment = center_align
ws['G3'].border = border
ws['I3'].border = border
ws['H3'].border = border
ws['J3'].border = border
ws['K3'].border = border
ws['L3'].border = border
ws['A4'] = "Class: "
ws['B4'] = bio_data["Class"]
ws['A4'].font = title_font
ws['B4'].font = title_font
ws['A4'].alignment = Alignment(horizontal="right")
ws['B4'].alignment = center_align
ws['A4'].border = border
ws['B4'].border = border
ws['C4'].border = border
ws['D4'] = "Section: "
ws['E4'] = "A"
ws['D4'].font = title_font
ws['E4'].font = title_font
ws['D4'].alignment = Alignment(horizontal="right")
ws['E4'].alignment = center_align
ws['D4'].border = border
ws['E4'].border = border
ws['G4'] = "Number In Class: "
ws['I4'] = "30"
ws['G4'].font = title_font
ws['I4'].font = title_font
ws['G4'].alignment = Alignment(horizontal="right")
ws['I4'].alignment = center_align
ws['G4'].border = border
ws['I4'].border = border
ws['H4'].border = border
ws['J4'].border = border
ws['K4'].border = border
ws['L4'].border = border
ws['A5'] = "Resumption Date: "
ws['B5'] = "01-09-2024"
ws['A5'].font = title_font
ws['B5'].font = title_font
ws['A5'].alignment = Alignment(horizontal="right")
ws['B5'].alignment = center_align
ws['A5'].border = border
ws['B5'].border = border
ws['C5'].border = border
ws['D5'].border = border
ws['E5'].border = border
ws['F5'].border = border
ws['G5'].border = border
ws['H5'].border = border
ws['I5'].border = border
ws['J5'].border = border
ws['K5'].border = border
ws['L5'].border = border
# Prepare keys in pairs
items = list(bio_data.items())
row = 3
col_widths = {"A": 20, "B": 15, "C": 15, "D": 20}

for col, width in col_widths.items():
    ws.column_dimensions[col].width = width

for i in range(0, len(items), 2):
    ws.row_dimensions[row].height = 20
    row += 1
# --- 3. Academic Performance Table ---
ws['A7'] = "Academic Performance"
ws['A7'].font = sub_header_font
ws['A7'].fill = section_fill
ws['A7'].alignment = center_align
ws.row_dimensions[7].height = 22
table_start_row = row + 1
columns = ["Subject", "CA1", "CA2", "CA3", "Exam", "Total", "1st Term", "2nd Term", "3rd Term Total", "Grade", "Position", "Remark"]
for col_num, col_name in enumerate(columns, 1):
    cell = ws.cell(row=table_start_row, column=col_num, value=col_name)
    cell.font = title_font
    cell.alignment = center_align
    cell.fill = section_fill
    cell.border = border
ws.row_dimensions[table_start_row].height = 30

for i, subject in enumerate(subjects):
    r = table_start_row + 1 + i
    row_data = df.iloc[i]
    ws.cell(row=r, column=1).value = row_data["Subject"]
    ws.cell(row=r, column=2).value = row_data["CA1"]
    ws.cell(row=r, column=3).value = row_data["CA2"]
    ws.cell(row=r, column=4).value = row_data["CA3"]
    ws.cell(row=r, column=5).value = row_data["Exam"]
    ws.cell(row=r, column=6).value = f"=SUM(B{r}:E{r})"
    ws.cell(row=r, column=7).value = row_data["1st Term"]
    ws.cell(row=r, column=8).value = row_data["2nd Term"]
    ws.cell(row=r, column=9).value = f"=F{r}"
    ws.cell(row=r, column=10).value = f'''=IF(F{r}>=75,"A",IF(F{r}>=60,"B",IF(F{r}>=50,"C",IF(F{r}>=45,"D",IF(F{r}>=40,"E","F")))))'''
    ws.cell(row=r, column=11).value = ""
    ws.cell(row=r, column=12).value = f'''=IF(J{r}="A","Excellent",IF(J{r}="B","Very Good",IF(J{r}="C","Good",IF(J{r}="D","Fair",IF(J{r}="E","Weak","Poor")))))'''
    for c in range(1, 13):
        ws.cell(row=r, column=c).alignment = center_align
        ws.cell(row=r, column=c).border = border

# --- 4. Summary Section ---
summary_row = table_start_row + len(subjects) + 2
ws[f"A{summary_row}"] = "Summary"
ws[f"A{summary_row}"].font = title_font
ws[f"A{summary_row}"].fill = section_fill
ws[f"A{summary_row}"].alignment = center_align
ws.row_dimensions[summary_row].height = 20

ws[f"A{summary_row+1}"] = "Total Score"
ws[f"B{summary_row+1}"] = f"=SUM(F{table_start_row+1}:F{table_start_row+len(subjects)})"
ws[f"A{summary_row+2}"] = "Average Score"
ws[f"B{summary_row+2}"] = f"=AVERAGE(F{table_start_row+1}:F{table_start_row+len(subjects)})"
ws[f"A{summary_row+3}"] = "Position in Class"
ws[f"B{summary_row+3}"] = "To be filled"
for i in range(1, 5):
    ws[f"A{summary_row+i}"].border = border
    ws[f"B{summary_row+i}"].border = border

# --- 5. Graph (Performance Chart) ---
chart_row = summary_row + 5
chart = BarChart()
chart.title = "Performance Chart (Third Term)"
chart.x_axis.title = "Subjects"
chart.y_axis.title = "Scores"
chart.height = 8
chart.width = 18

data = Reference(ws, min_col=6, min_row=table_start_row, max_row=table_start_row + len(subjects))
cats = Reference(ws, min_col=1, min_row=table_start_row + 1, max_row=table_start_row + len(subjects))
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, f"A{chart_row}")

# --- 6. Affective Domain ---
affective_row = chart_row + 18
ws[f"A{affective_row}"] = "Affective Domain"
ws[f"A{affective_row}"].font = title_font
ws[f"A{affective_row}"].fill = section_fill
ws[f"A{affective_row}"].alignment = center_align
affective_traits = ["Punctuality", "Neatness", "Honesty", "Attentiveness", "Politeness"]
for i, trait in enumerate(affective_traits):
    ws[f"A{affective_row+1+i}"] = trait
    ws[f"B{affective_row+1+i}"] = "5"
    ws[f"A{affective_row+1+i}"].border = border
    ws[f"B{affective_row+1+i}"].border = border

# --- 7. Psychomotor Skills ---
psy_row = affective_row + len(affective_traits) + 2
ws[f"A{psy_row}"] = "Psychomotor Skills"
ws[f"A{psy_row}"].font = sub_header_font
ws[f"A{psy_row}"].fill = section_fill
ws[f"A{psy_row}"].alignment = center_align
psy_traits = ["Sports", "Craft", "Drawing", "Music", "Drama"]
for i, trait in enumerate(psy_traits):
    ws[f"A{psy_row+1+i}"] = trait
    ws[f"B{psy_row+1+i}"] = "5"
    ws[f"A{psy_row+1+i}"].border = border
    ws[f"B{psy_row+1+i}"].border = border

# --- 8. Remarks & Signature Section ---
remark_row = psy_row + len(psy_traits) + 2
ws[f"A{remark_row}"] = "Head Teacher's Remark:"
ws[f"A{remark_row+1}"] = "Parent/Guardian's Remark:"
ws[f"A{remark_row+2}"] = "Date:"
ws[f"B{remark_row+2}"] = datetime.today().strftime('%d-%m-%Y')
for i in range(3):
    ws[f"A{remark_row+i}"].border = border
    ws[f"B{remark_row+i}"].border = border

# --- 9. Grading Scale ---
grade_row = remark_row + 4
ws[f"A{grade_row}"] = "Grading Scale (Legend)"
ws[f"A{grade_row}"].font = sub_header_font
ws[f"A{grade_row}"].fill = section_fill
ws[f"A{grade_row}"].alignment = center_align
grades = {
    "A": "75 - 100 (Excellent)",
    "B": "60 - 74 (Very Good)",
    "C": "50 - 59 (Good)",
    "D": "45 - 49 (Fair)",
    "E": "40 - 44 (Weak)",
    "F": "0 - 39 (Poor)"
}
for i, (grade, meaning) in enumerate(grades.items()):
    ws[f"A{grade_row+1+i}"] = grade
    ws[f"B{grade_row+1+i}"] = meaning
    ws[f"A{grade_row+1+i}"].border = border
    ws[f"B{grade_row+1+i}"].border = border

# --- Page Setup for Printing ---
ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_margins.left = 0.3
ws.page_margins.right = 0.3
ws.page_margins.top = 0.5
ws.page_margins.bottom = 0.5

wb.save("John_Doe_Report.xlsx")

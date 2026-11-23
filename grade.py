import os
import sys
import math
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.drawing.image import Image
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter
from datetime import datetime

# Your data
from classes.student_data_2026_27 import students
from classes.grade.subject import primary_subjects_all, primary_subjects_without_g4_5

class_name = sys.argv[1] if __name__ == "__main__" and len(sys.argv) > 1 else "Grade Four"
if class_name not in students:
    raise ValueError(
        f"Unknown class {class_name!r}. Choose one of: {', '.join(students.keys())}"
    )

if "Diamond" in class_name:
    section = "Diamond"
elif "Gold" in class_name:
    section = "Gold"
else:
    section = "General"

base_class_name = class_name.replace(" Gold", "").replace(" Diamond", "")
grade_numbers = {
    "Grade One": 1,
    "Grade Two": 2,
    "Grade Three": 3,
    "Grade Four": 4,
    "Grade Five": 5,
}
grade_number = grade_numbers[base_class_name]
admission_prefix = {
    "Grade One": "G1",
    "Grade Two Gold": "G2G",
    "Grade Two Diamond": "G2D",
    "Grade Three Diamond": "G3D",
    "Grade Three Gold": "G3G",
    "Grade Four": "G4",
    "Grade Five": "G5",
}[class_name]

students_data = [
    {
        "Name": name,
        "Admission No": f"{admission_prefix}/{str(index).zfill(3)}",
        "Class": base_class_name,
        "Term": "Third Term",
        "Session": "2026/2027",
        "Sex": "Unknown",
        "Section": section,
    }
    for index, name in enumerate(students[class_name], start=1)
]

class_data = {
    "Class": base_class_name,
    "Term": "Third Term",
    "Session": "2026/2027",
    "Resumption Date": "2026-09-01",
    "Closing Date": "2027-07-01",
    "Total Students": len(students_data),
    "Average Attendance": 95.0,
    "Coordinator": "Head Teacher",
    "Section": section,
}

subjects = primary_subjects_all if grade_number >= 4 else primary_subjects_without_g4_5

# Styles
header_font = Font(name="Times New Roman", bold=True, size=32)
sub_header_font = Font(name="Times New Roman", bold=True, size=16)
title_font = Font(name="Times New Roman", bold=True, size=14)
left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
border = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))
gray_fill = PatternFill("solid", fgColor="DDDDDD")
section_fill = PatternFill("solid", fgColor="DDDDDD")

# Column widths
col_widths = {"A": 40.71, "B": 15, "C": 15, "D": 25, "E" : 15, "F": 15, "G": 15, "H": 15, "I": 15, "J": 10, "K" : 10, "L": 20, "M": 5}
report_config = {
    "school_name": "TOPSTEPS ACADEMY",
    "ca1_max": 20,
    "ca2_max": 20,
    "ca3_max": 20,
    "exam_max": 40,
    "grade_a_min": 75,
    "grade_b_min": 60,
    "grade_c_min": 50,
    "grade_d_min": 45,
    "grade_e_min": 40,
}
assessment_columns = [
    {"name": "CA1", "max_score": 20},
    {"name": "CA2", "max_score": 20},
    {"name": "CA3", "max_score": 20},
    {"name": "EXAM", "max_score": 40},
]
report_fields = {
    "subject_average": True,
    "first_term": True,
    "second_term": True,
    "cumulative": True,
    "grade": True,
    "position": True,
    "remark": True,
}


def report_columns(term_number):
    columns = [("subject", "SUBJECT")]
    component_spacing = " " if term_number == 1 else ""
    columns.extend(
        (
            ("assessment", assessment["name"]),
            f"{assessment['name'].upper()}{component_spacing}({assessment['max_score']:g}%)",
        )
        for assessment in assessment_columns
    )
    columns.append(("total", "TOTAL"))
    if term_number == 1 and report_fields["subject_average"]:
        columns.append(("subject_average", "SUBJECT AVERAGE"))
    if term_number >= 2 and report_fields["first_term"]:
        columns.append(("first_term", "1ST TERM"))
    if term_number >= 3 and report_fields["second_term"]:
        columns.append(("second_term", "2ND TERM"))
    if term_number >= 2 and report_fields["cumulative"]:
        columns.append(("cumulative", "CUMULATIVE"))
    if report_fields["grade"]:
        columns.append(("grade", "GRADE"))
    if report_fields["position"]:
        columns.append(("position", "POSITION"))
    if report_fields["remark"]:
        columns.append(("remark", "REMARK"))
    return columns

def safe_sheet_name(base, term):
    name = f"{base[:18]}_{term}"
    return name[:31]  # Excel limit

def create_term_sheet(ws, student, term_name, term_num, show_prev=True):
    # Page setup
    ws.page_setup.fitToWidth = 1
    ws.page_margins.left = ws.page_margins.right = 0.3
    ws.page_margins.top = ws.page_margins.bottom = 0.5
    ws.page_setup.horizontalCentered = True

    for col, w in col_widths.items():
        ws.column_dimensions[col].width = w

    row = 1

    # Header
    columns = report_columns(term_num)
    report_width = max(13, len(columns))
    last_column_letter = get_column_letter(report_width)

    ws.merge_cells(f'A1:{last_column_letter}1')
    ws['A1'] = report_config["school_name"].upper()
    ws['A1'].font = header_font
    ws['A1'].alignment = center_align
    ws.row_dimensions[1].height = 38

    ws.merge_cells(f'A2:{last_column_letter}2')
    ws['A2'] = f"{term_name.upper()} TERM {class_data['Session']} SESSION ACADEMIC REPORT"
    ws['A2'].font = sub_header_font
    ws['A2'].alignment = center_align
    ws['A2'].fill = gray_fill
    ws.row_dimensions[2].height = 25

    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tpsa_logo.png")
    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo.width = logo.height = 80
        ws.add_image(logo, "A1")

    row = 3

    # Student Info

    ws.merge_cells('B3:F3')
    ws.merge_cells('G3:H3')
    ws.merge_cells(f'I3:{last_column_letter}3')
    ws.merge_cells('B4:C4')
    ws.merge_cells('E4:F4')
    ws.merge_cells('G4:H4')
    ws.merge_cells(f'I4:{last_column_letter}4')
    ws.merge_cells(f'B5:{last_column_letter}5')
    ws.merge_cells(f'A7:{last_column_letter}7')
    

    ws[f'A{row}'] = "Name:"; ws[f'B{row}'] = student["Name"].upper()
    ws[f'G{row}'] = "Adm No:"; ws[f'I{row}'] = student["Admission No"]
    ws[f'A{row+1}'] = "Class:"; ws[f'B{row+1}'] = class_data["Class"].upper()
    ws[f'D{row+1}'] = "Section:"; ws[f'E{row+1}'] = student["Section"].upper()
    ws[f'G{row+1}'] = "No in Class:"; ws[f'I{row+1}'] = len(students_data)
    ws[f'A{row+2}'] = "Resumption:"; ws[f'B{row+2}'] = class_data["Resumption Date"]

    for r in range(row, row+3):
        for c in range(1, report_width + 1):
            cell = ws.cell(r, c)
            cell.font = title_font
            cell.border = border
            cell.alignment = right_align if c in [1,4,7] else center_align

    row += 4

    # Academic Table
    ws.merge_cells(f'A{row}:{last_column_letter}{row}')
    ws[f'A{row}'] = "ACADEMIC PERFORMANCE"
    ws[f'A{row}'].font = sub_header_font
    ws[f'A{row}'].fill = gray_fill
    ws[f'A{row}'].alignment = center_align
    ws.row_dimensions[row].height = 25
    row += 1

    table_start = row

    column_by_key = {key: index for index, (key, _) in enumerate(columns, 1)}
    for i, (key, header) in enumerate(columns, 1):
        cell = ws.cell(row, i, header)
        cell.font = title_font
        cell.alignment = center_align
        cell.fill = gray_fill
        cell.border = border
        ws.column_dimensions[get_column_letter(i)].width = {
            "subject": 40.71,
            "total": 15,
            "assessment": 15,
            "subject_average": 15,
            "first_term": 15,
            "second_term": 15,
            "cumulative": 15,
            "grade": 10,
            "position": 10,
            "remark": 20,
        }.get(key[0] if isinstance(key, tuple) else key, 15)
    ws.row_dimensions[row].height = 30
    if "remark" in column_by_key:
        remark_column = column_by_key["remark"]
        if remark_column < report_width:
            ws.merge_cells(
                start_row=row, start_column=remark_column,
                end_row=row, end_column=report_width
            )

    # Subject rows
    for idx, subject in enumerate(subjects):
        r = row+1+ idx
        cell = ws.cell(r, column_by_key["subject"])
        cell.value = subject.upper()
        cell.alignment = Alignment(horizontal="left")
        cell.font = title_font
        cell.border = border
        total_col = column_by_key["total"]
        total_letter = get_column_letter(total_col)
        assessment_columns_for_row = [
            column_by_key[("assessment", assessment["name"])]
            for assessment in assessment_columns
        ]
        first_assessment_letter = get_column_letter(min(assessment_columns_for_row))
        last_assessment_letter = get_column_letter(max(assessment_columns_for_row))
        ws.cell(r, total_col).value = (
            f"=ROUND(SUM({first_assessment_letter}{r}:{last_assessment_letter}{r}), 1)"
        )

        if "subject_average" in column_by_key:
            ws.cell(r, column_by_key["subject_average"]).value = f"={total_letter}{r}"

        first_term_sheet = safe_sheet_name(
            student["Name"].upper().replace(" ", "_"), "1ST_TERM"
        )
        second_term_sheet = safe_sheet_name(
            student["Name"].upper().replace(" ", "_"), "2ND_TERM"
        )
        quoted_first_sheet = first_term_sheet.replace("'", "''")
        quoted_second_sheet = second_term_sheet.replace("'", "''")
        if "first_term" in column_by_key:
            ws.cell(r, column_by_key["first_term"]).value = (
                f"='{quoted_first_sheet}'!{total_letter}{r}"
            )
        if "second_term" in column_by_key:
            ws.cell(r, column_by_key["second_term"]).value = (
                f"='{quoted_second_sheet}'!{total_letter}{r}"
            )
        if "cumulative" in column_by_key:
            cumulative_parts = [f"{total_letter}{r}"]
            if term_num >= 2:
                cumulative_parts.append(f"'{quoted_first_sheet}'!{total_letter}{r}")
            if term_num >= 3:
                cumulative_parts.append(f"'{quoted_second_sheet}'!{total_letter}{r}")
            ws.cell(r, column_by_key["cumulative"]).value = (
                "=" + " + ".join(cumulative_parts)
            )

        grade_expression = (
            f'IF({total_letter}{r}>={report_config["grade_a_min"]:g},"A",'
            f'IF({total_letter}{r}>={report_config["grade_b_min"]:g},"B",'
            f'IF({total_letter}{r}>={report_config["grade_c_min"]:g},"C",'
            f'IF({total_letter}{r}>={report_config["grade_d_min"]:g},"D",'
            f'IF({total_letter}{r}>={report_config["grade_e_min"]:g},"E","F")))))'
        )
        if "grade" in column_by_key:
            ws.cell(r, column_by_key["grade"]).value = f"={grade_expression}"
        if "remark" in column_by_key:
            grade_reference = (
                ws.cell(r, column_by_key["grade"]).coordinate
                if "grade" in column_by_key
                else grade_expression
            )
            remark_column = column_by_key["remark"]
            ws.cell(r, remark_column).value = (
                f'=IF({grade_reference}="A","Excellent",'
                f'IF({grade_reference}="B","Very Good",'
                f'IF({grade_reference}="C","Good",'
                f'IF({grade_reference}="D","Fair",'
                f'IF({grade_reference}="E","Weak","Poor")))))'
            )
            if remark_column < report_width:
                ws.merge_cells(
                    start_row=r, start_column=remark_column,
                    end_row=r, end_column=report_width
                )
                for c in range(remark_column, report_width + 1):
                    ws.cell(r, c).border = border

        for c in range(1, len(columns) + 1):
            cell = ws.cell(r, c)
            cell.alignment = center_align
            cell.border = border

    row += len(subjects) + 2

    # Summary Section
    summary_row = table_start + len(subjects) + 2
    ws.merge_cells(f'A{row}:B{row}')
    ws[f'A{row}'] = "SUMMARY"
    ws[f'A{row}'].font = sub_header_font
    ws[f'A{row}'].fill = gray_fill
    ws[f'A{row}'].alignment = Alignment(horizontal="center")

    total_obtainable = len(subjects) * sum(
        assessment["max_score"] for assessment in assessment_columns
    )
    total_row = row + 1
    ws[f'A{total_row}'] = "Total Score Obtainable"
    ws[f'B{total_row}'] = total_obtainable

    ws[f'A{total_row+1}'] = "Total Score Obtained"
    total_column_letter = get_column_letter(column_by_key["total"])
    ws[f'B{total_row+1}'] = (
        f"=SUM({total_column_letter}{table_start+1}:{total_column_letter}{row-2})"
    )

    ws[f'A{total_row+2}'] = "Average"
    ws[f'B{total_row+2}'] = (
        f"=ROUND(AVERAGE({total_column_letter}{table_start+1}:"
        f"{total_column_letter}{row-2}),1)"
    )

    ws[f'A{total_row+3}'] = "Overall Grade"
    if report_fields["grade"]:
        ws[f'B{total_row+3}'] = f'=IF(B{total_row+2}>={report_config["grade_a_min"]:g},"A",IF(B{total_row+2}>={report_config["grade_b_min"]:g},"B",IF(B{total_row+2}>={report_config["grade_c_min"]:g},"C",IF(B{total_row+2}>={report_config["grade_d_min"]:g},"D",IF(B{total_row+2}>={report_config["grade_e_min"]:g},"E","F")))))'
    else:
        ws[f'A{total_row+3}'] = ""

    # ws[f'A{total_row+4}'] = "Position in Class"
    # ws[f'B{total_row+4}'] = "________"

    for i in range(4):
        ws[f'A{total_row+i}'].font = title_font
        ws[f'B{total_row+i}'].font = title_font
        ws[f'B{total_row+i}'].alignment = Alignment(horizontal="right")
        ws[f'A{total_row+i}'].border = border
        ws[f'B{total_row+i}'].border = border


    # Chart (based on term)
    chart_row = total_row + 6
    chart = BarChart()
    chart.title = f"{term_name.upper()} TERM PERFORMANCE"
    chart.y_axis.title = "Score"
    chart.x_axis.title = "Subjects"
    chart.height = 9
    chart.width = 12
    chart.style = 12
    chart.legend = None
    chart.x_axis.majorTickMark = "in"
    chart.x_axis.delete = False
    chart.y_axis.delete = False

    data_col = column_by_key["total"]

    data = Reference(
        ws, min_col=data_col, min_row=table_start,
        max_row=table_start + len(subjects)
    )
    cats = Reference(
        ws, min_col=column_by_key["subject"],
        min_row=table_start + 1, max_row=table_start + len(subjects)
    )
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.x_axis.textRotation = 45
    chart.x_axis.title.txPr = None
    chart.y_axis.title.txPr = None
    chart.title.txPr = None
    chart.x_axis.title.font = Font(size=12, bold=True)
    chart.y_axis.title.font = Font(size=12, bold=True)
    chart.title.font = Font(size=14, bold=True)
    chart.gapWidth = 150

    ws.add_chart(chart, f"A{chart_row}")

    # --- 6. Affective Domain ---
    affective_row = summary_row
    ws[f"D{affective_row}"] = "Effort".upper()
    ws[f"D{affective_row}"].font = title_font
    ws[f"D{affective_row}"].fill = section_fill
    ws[f"D{affective_row}"].alignment = center_align
    ws[f"D{affective_row}"].border = border
    affective_traits = ["Aesthetic Appreciation", "Attendance", "Creativity", "Honesty", "Initiative","Leadership","Neatness","Obedience", "Perserverance","Politeness","Self Control",  "Sense Of Responsibility", "Sociability", "Spirit Of Coordination"]
    for col in range(5):
        ws.cell(row=affective_row, column=5 + col).value = col + 1
        ws.cell(row=affective_row, column=5 + col).alignment = center_align
        ws.cell(row=affective_row, column=5 + col).font = title_font
        ws.cell(row=affective_row, column=5 + col).border = border
    for i, trait in enumerate(affective_traits):
        ws[f"D{affective_row+1+i}"] = trait.upper()
        ws[f"E{affective_row+1}"] = "✓"
        ws[f"D{affective_row+1+i}"].border = border
        for col in range(5):
            ws.cell(row=affective_row+1+i, column=5 + col).border = border


    # --- 7. Psychomotor Skills ---
    psy_row = affective_row + len(affective_traits) + 2
    ws[f"D{psy_row}"] = "Psychomotor Skills".upper()
    ws[f"D{psy_row}"].font = title_font
    ws[f"D{psy_row}"].fill = section_fill
    ws[f"D{psy_row}"].alignment = center_align
    ws[f"D{psy_row}"].border = border
    for col in range(5):
        ws.cell(row=psy_row, column=5 + col).value = col + 1
        ws.cell(row=psy_row, column=5 + col).alignment = center_align
        ws.cell(row=psy_row, column=5 + col).font = title_font
        ws.cell(row=psy_row, column=5 + col).border = border
    psy_traits = ["Communication Skills", "Craft", "Games/Sports", "Handwriting", "Handling Of Tools", "Musical Skills", "Painting/Drawing"]
    for i, trait in enumerate(psy_traits):
        ws[f"D{psy_row+1+i}"] = trait
        ws[f"E{psy_row+1}"] = "✓"
        ws[f"D{psy_row+1+i}"].border = border
        for col in range(5):
            ws.cell(row=psy_row+1+i, column=5 + col).border = border

    # --- 8. Remarks & Signature Section ---
    remark_row = psy_row + len(psy_traits) + 2
    ws[f"A{remark_row}"] = "Teacher's Remark:".upper()
    ws[f"A{remark_row+1}"] = f"{class_data['Coordinator']}'s Remark:".upper()
    ws[f"A{remark_row+2}"] = "Date:".upper()
    ws[f"B{remark_row+2}"] = datetime.today().strftime('%d-%m-%Y')
    for i in range(3):
        ws[f"A{remark_row+i}"].border = border
        ws[f"A{remark_row+i}"].font = title_font
        ws[f"A{remark_row+i}"].alignment = Alignment(horizontal="left")
        ws[f"A{remark_row+i}"].fill = section_fill
        ws.row_dimensions[remark_row + i].height = 22
        ws[f"B{remark_row+i}"].border = border
        ws[f"B{remark_row+i}"].alignment = Alignment(horizontal="left")
        ws[f"B{remark_row+i}"].font = title_font
        ws[f"B{remark_row+i}"].fill = section_fill
        ws[f"B{remark_row+i}"].value = "To be filled".upper()
        ws[f"C{remark_row+i}"].border = border

        ws.merge_cells(
            start_row=remark_row + i, start_column=1,
            end_row=remark_row + i, end_column=report_width
        )

    # --- 9. Grading Scale ---
    if report_fields["grade"]:
        grade_row = summary_row
        legend_column = max(11, report_width - 2)
        legend_letter = get_column_letter(legend_column)
        meaning_letter = get_column_letter(legend_column + 1)
        ws[f"{legend_letter}{grade_row}"] = "Grading Scale (Legend)".upper()
        ws[f"{legend_letter}{grade_row}"].font = title_font
        ws[f"{legend_letter}{grade_row}"].fill = section_fill
        ws[f"{legend_letter}{grade_row}"].alignment = center_align
        ws[f"{legend_letter}{grade_row}"].border = border
        ws.row_dimensions[grade_row].height = 25
        ws.merge_cells(f"{legend_letter}{grade_row}:{meaning_letter}{grade_row}")
        grades = {
            "A": f"{report_config['grade_a_min']:g} - 100 (Excellent)",
            "B": f"{report_config['grade_b_min']:g} - {report_config['grade_a_min'] - 1:g} (Very Good)",
            "C": f"{report_config['grade_c_min']:g} - {report_config['grade_b_min'] - 1:g} (Good)",
            "D": f"{report_config['grade_d_min']:g} - {report_config['grade_c_min'] - 1:g} (Fair)",
            "E": f"{report_config['grade_e_min']:g} - {report_config['grade_d_min'] - 1:g} (Weak)",
            "F": f"0 - {report_config['grade_e_min'] - 1:g} (Poor)"
        }
        for i, (grade, meaning) in enumerate(grades.items()):
            ws[f"{legend_letter}{grade_row+1+i}"] = grade
            ws[f"{meaning_letter}{grade_row+1+i}"] = meaning.upper()
            ws[f"{legend_letter}{grade_row+1+i}"].border = border
            ws[f"{meaning_letter}{grade_row+1+i}"].border = border

    # --- Page Setup for Printing ---
    ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1  # Fit to one page wide
    ws.page_setup.fitToHeight = 0  # Let data stretch vertically (no limit)
    ws.page_setup.horizontalCentered = True
    ws.page_setup.verticalCentered = False
    ws.page_margins.left = 0.3
    ws.page_margins.right = 0.3
    ws.page_margins.top = 0.5
    ws.page_margins.bottom = 0.5
    ws.page_margins.header = 0.2
    ws.page_margins.footer = 0.2

def generate_grade_workbook(
    selected_students,
    selected_class_data,
    selected_subjects,
    score_data=None,
    selected_report_config=None,
    output_path=None,
    selected_assessments=None,
    selected_report_fields=None,
):
    global wb, students_data, class_data, subjects, report_config
    global assessment_columns, report_fields
    students_data = selected_students
    class_data = selected_class_data
    subjects = selected_subjects
    report_config = {
        "school_name": "TOPSTEPS ACADEMY",
        "ca1_max": 20,
        "ca2_max": 20,
        "ca3_max": 20,
        "exam_max": 40,
        "grade_a_min": 75,
        "grade_b_min": 60,
        "grade_c_min": 50,
        "grade_d_min": 45,
        "grade_e_min": 40,
        **(selected_report_config or {}),
    }
    assessment_columns = (
        selected_assessments
        if selected_assessments is not None
        else [
            {"name": "CA1", "max_score": 20},
            {"name": "CA2", "max_score": 20},
            {"name": "CA3", "max_score": 20},
            {"name": "EXAM", "max_score": 40},
        ]
    )
    report_fields = {
        "subject_average": True,
        "first_term": True,
        "second_term": True,
        "cumulative": True,
        "grade": True,
        "position": True,
        "remark": True,
        **(selected_report_fields or {}),
    }
    if not assessment_columns:
        raise ValueError("Configure at least one active scored column.")
    normalized_assessments = []
    for column in assessment_columns:
        name = str(column["name"]).strip()
        maximum = float(column["max_score"])
        if not name or not math.isfinite(maximum) or maximum <= 0:
            raise ValueError("Every active scored column needs a name and a positive maximum mark.")
        normalized_assessments.append({"name": name, "max_score": maximum})
    if len({column["name"].casefold() for column in normalized_assessments}) != len(normalized_assessments):
        raise ValueError("Active scored column names must be unique.")
    if abs(sum(column["max_score"] for column in normalized_assessments) - 100) > 0.000001:
        raise ValueError("Active scored column maximums must total 100.")
    assessment_columns = normalized_assessments
    score_data = score_data or {}
    wb = Workbook()
    wb.remove(wb.active)
    sheet_names = {}

    term_details = (("1ST_TERM", "First", 1, False), ("2ND_TERM", "Second", 2, True), ("3RD_TERM", "Third", 3, True))
    for student in students_data:
        base = student["Name"].upper().replace(" ", "_")
        for suffix, term_name, term_number, show_previous in term_details:
            sheet_name = safe_sheet_name(base, suffix)
            ws = wb.create_sheet(sheet_name)
            sheet_names[(student["Admission No"], term_number)] = sheet_name
            create_term_sheet(ws, student, term_name, term_number, show_prev=show_previous)
            column_by_key = {
                key: index for index, (key, _) in enumerate(report_columns(term_number), 1)
            }
            for subject_index, subject in enumerate(subjects):
                result = score_data.get(
                    (student["Admission No"], subject, term_number), {}
                )
                score_row = 9 + subject_index
                for assessment in assessment_columns:
                    column = column_by_key[("assessment", assessment["name"])]
                    ws.cell(score_row, column).value = result.get(
                        assessment["name"], 0
                    )

    for term_number in (1, 2, 3):
        column_by_key = {
            key: index for index, (key, _) in enumerate(report_columns(term_number), 1)
        }
        position_column = column_by_key.get("position")
        if position_column is None:
            continue
        total_letter = get_column_letter(column_by_key["total"])
        for subject_index, subject in enumerate(subjects):
            score_row = 9 + subject_index
            for student in students_data:
                ws = wb[sheet_names[(student["Admission No"], term_number)]]
                position_terms = []
                for other_student in students_data:
                    other_sheet = sheet_names[
                        (other_student["Admission No"], term_number)
                    ].replace("'", "''")
                    position_terms.append(
                        f'COUNTIF(\'{other_sheet}\'!{total_letter}{score_row},'
                        f'">"&{total_letter}{score_row})'
                    )
                ws.cell(score_row, position_column).value = (
                    "=1+" + "+".join(position_terms)
                )

    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    if output_path is None:
        session_years = class_data["Session"].split("/")
        session_folder = f"{session_years[0]}-{session_years[1][-2:]}"
        output_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "final_3term_results",
            session_folder,
        )
        os.makedirs(output_folder, exist_ok=True)
        section = class_data.get("Section", "General")
        class_label = class_data["Class"]
        if section not in ("", "General"):
            class_label = f"{class_label}_{section}"
        filename = f"{class_label}_COMPLETE_3-TERM_RESULTS_{class_data['Session'].replace('/', '_')}.xlsx"
        output_path = os.path.join(output_folder, filename)
    else:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    wb.save(output_path)
    return output_path


if __name__ == "__main__":
    path = generate_grade_workbook(students_data, class_data, subjects)
    print("SUCCESS! 3-Term Report Card Generated")
    print(f"File: {path}")
    print(f"Students: {len(students_data)} x 3 sheets = {len(students_data)*3} total sheets")
    print("1st Term -> Only current term")
    print("2nd Term -> Current + 1st Term")
    print("3rd Term -> All 3 terms + Cumulative")
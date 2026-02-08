import csv
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def read_data(filename):
    data = []
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Marks"] = int(row["Marks"])
            data.append(row)
    return data

def analyze_data(data):
    total_students = len(data)
    marks = [student["Marks"] for student in data]

    average_marks = sum(marks) / total_students
    highest_marks = max(marks)
    lowest_marks = min(marks)

    return {
        "total_students": total_students,
        "average_marks": round(average_marks, 2),
        "highest_marks": highest_marks,
        "lowest_marks": lowest_marks
    }

def generate_pdf(data, analysis):
    pdf = canvas.Canvas("generated_report.pdf", pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 50, "Automated Student Performance Report")

    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(width - 50, height - 80, f"Generated on: {datetime.now().strftime('%d-%m-%Y')}")

    # Summary Section
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 120, "Summary")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, height - 150, f"Total Students: {analysis['total_students']}")
    pdf.drawString(70, height - 170, f"Average Marks: {analysis['average_marks']}")
    pdf.drawString(70, height - 190, f"Highest Marks: {analysis['highest_marks']}")
    pdf.drawString(70, height - 210, f"Lowest Marks: {analysis['lowest_marks']}")

    # Table Header
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 250, "Student Name")
    pdf.drawString(220, height - 250, "Department")
    pdf.drawString(380, height - 250, "Marks")

    y = height - 270
    pdf.setFont("Helvetica", 11)

    # Table Data
    for student in data:
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 50

        pdf.drawString(50, y, student["StudentName"])
        pdf.drawString(220, y, student["Department"])
        pdf.drawString(380, y, str(student["Marks"]))
        y -= 18

    pdf.save()

def main():
    data = read_data("data.csv")
    analysis = analyze_data(data)
    generate_pdf(data, analysis)
    print("PDF report generated successfully!")


if __name__ == "__main__":
    main()

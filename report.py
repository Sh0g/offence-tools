from fpdf import FPDF


def make_report (titlename, input, output, filename, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 14)
    pdf.cell(200, 10, titlename, ln=1, align="C")
    pdf.cell(100, 10, txt="You've been entered:", ln=1)
    pdf.cell(100, 10, txt=input, ln=1)
    pdf.ln(10)
    pdf.cell(100, 10, txt="Your result is:", ln=1)
    for line in output:
        pdf.multi_cell(0, 10, txt=line, align="L")
    pdf.cell(200, 10, txt=date, ln=1)
    pdf.output(filename, 'F')
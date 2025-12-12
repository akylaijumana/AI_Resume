"""
PDF Export Functionality
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class PDFExporter:
    """Takes care of exporting resumes to PDF format"""

    @staticmethod
    def export(resume_text, file_path):
        """
        Export the resume to a PDF file

        resume_text: the formatted text to put in PDF
        file_path: where to save the PDF
        """
        # set up the PDF document with margins
        pdf_doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        content_elements = []
        style_sheet = getSampleStyleSheet()

        # add a custom body style for better text formatting
        custom_body = ParagraphStyle(
            name='CustomBody',
            parent=style_sheet['BodyText'],
            fontSize=10,
            leading=14
        )
        style_sheet.add(custom_body)

        # split resume into lines and format each one
        lines = resume_text.split('\n')
        for line in lines:
            line_stripped = line.strip()
            if line_stripped:
                # headings are usually all caps or short
                line_len = len(line_stripped)
                is_upper = line_stripped.isupper()

                if is_upper or line_len < 40:
                    para = Paragraph(line_stripped, style_sheet['Heading2'])
                else:
                    para = Paragraph(line_stripped, style_sheet['CustomBody'])

                content_elements.append(para)
                content_elements.append(Spacer(1, 0.1*inch))

        # build the final PDF
        pdf_doc.build(content_elements)


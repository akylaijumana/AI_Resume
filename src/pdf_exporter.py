"""
PDF Export Functionality
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class PDFExporter:
    """Handles PDF generation from resume text"""

    @staticmethod
    def export(resume_text, file_path):
        """
        Export resume to PDF

        Args:
            resume_text: Formatted resume text
            file_path: Output PDF file path

        Raises:
            Exception: If PDF generation fails
        """
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        elements = []
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            leading=14
        ))

        paragraphs = resume_text.split('\n')
        for para in paragraphs:
            if para.strip():
                if para.isupper() or len(para) < 40:
                    p = Paragraph(para, styles['Heading2'])
                else:
                    p = Paragraph(para, styles['CustomBody'])
                elements.append(p)
                elements.append(Spacer(1, 0.1*inch))

        doc.build(elements)


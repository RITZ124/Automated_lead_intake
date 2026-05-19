import os
import re
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

from reportlab.lib import colors

def extract_scores(ai_report):

    scores = {

        "AI Readiness": "N/A",

        "Automation Potential": "N/A",

        "Digital Presence": "N/A",

        "Marketing Maturity": "N/A"

    }

    patterns = {

        "AI Readiness":
        r"AI Readiness Score:\s*(\d+/10)",

        "Automation Potential":
        r"Automation Potential Score:\s*(\d+/10)",

        "Digital Presence":
        r"Digital Presence Score:\s*(\d+/10)",

        "Marketing Maturity":
        r"Marketing Maturity Score:\s*(\d+/10)"

    }

    for key, pattern in patterns.items():

        match = re.search(
            pattern,
            ai_report
        )

        if match:

            scores[key] = match.group(1)

    return scores
def clean_ai_text(text):

    # REMOVE MARKDOWN **
    text = text.replace("**", "")

    return text


def generate_pdf_report(lead, ai_report):

    os.makedirs(
        "generated_reports",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"{lead.company}_{timestamp}.pdf"
    )

    filename = filename.replace(" ", "_")

    pdf_path = os.path.join(
        "generated_reports",
        filename
    )

    doc = SimpleDocTemplate(

        pdf_path,

        pagesize=letter,

        rightMargin=40,
        leftMargin=40,

        topMargin=40,
        bottomMargin=30

    )

    styles = getSampleStyleSheet()

    elements = []

    # TITLE
    title = Paragraph(

        """
        <font size=24 color='#007bff'>
        <b>AI Business Audit Report</b>
        </font>
        """,

        styles["Title"]

    )

    elements.append(title)

    elements.append(Spacer(1, 25))

    # COMPANY INFO
    company_data = [

        ["Company", lead.company],

        ["Website", lead.website],

        ["Contact", lead.email],

        ["Generated For", lead.name],

        ["Status", lead.status]

    ]

    table = Table(

        company_data,

        colWidths=[150, 320]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#007bff")),

            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

            ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ("FONTSIZE", (0, 0), (-1, -1), 11),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10)

        ])

    )

    elements.append(table)

    elements.append(Spacer(1, 30))

    # SECTION HEADER
    heading = Paragraph(

        """
        <font size=18 color='#222222'>
        <b>Personalized AI Audit</b>
        </font>
        """,

        styles["Heading1"]

    )

    elements.append(heading)

    elements.append(Spacer(1, 20))
    # EXTRACT SCORES
    scores = extract_scores(ai_report)

    # SCORE TITLE
    score_heading = Paragraph(

        """
        <font size=18 color='#222222'>
        <b>AI Business Intelligence Scores</b>
        </font>
        """,

        styles["Heading1"]

    )

    elements.append(score_heading)

    elements.append(Spacer(1, 15))

    # SCORE TABLE
    score_data = [

        ["Category", "Score"],

        ["AI Readiness",
        scores["AI Readiness"]],

        ["Automation Potential",
        scores["Automation Potential"]],

        ["Digital Presence",
        scores["Digital Presence"]],

        ["Marketing Maturity",
        scores["Marketing Maturity"]]

    ]

    score_table = Table(

        score_data,

        colWidths=[250, 120]

    )

    score_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0),
            colors.HexColor("#111827")),

            ("TEXTCOLOR", (0, 0), (-1, 0),
            colors.white),

            ("BACKGROUND", (0, 1), (-1, -1),
            colors.HexColor("#f3f4f6")),

            ("GRID", (0, 0), (-1, -1),
            1, colors.grey),

            ("FONTNAME", (0, 0), (-1, -1),
            "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, -1),
            10),

            ("FONTSIZE", (0, 0), (-1, -1),
            11)

        ])

    )

    elements.append(score_table)

    elements.append(Spacer(1, 30))
    # CLEAN AI REPORT
    ai_report = clean_ai_text(ai_report)

    # SPLIT SECTIONS
    sections = ai_report.split("\n")

    filtered_sections = []

    for line in sections:

        # REMOVE DUPLICATE SCORE LINES
        if (
            "AI Readiness Score:" in line
            or
            "Automation Potential Score:" in line
            or
            "Digital Presence Score:" in line
            or
            "Marketing Maturity Score:" in line
        ):

            continue

        filtered_sections.append(line)

    sections = filtered_sections

    for line in sections:

        line = line.strip()

        if not line:

            continue

        # HEADINGS
        if (
            re.match(r"^\d+\.", line)
            and len(line) < 80
        ):

            paragraph = Paragraph(

                f"""
                <font size=15 color='#007bff'>
                <b>{line}</b>
                </font>
                """,

                styles["Heading2"]

            )

            elements.append(paragraph)

            elements.append(Spacer(1, 12))

        # BULLET POINTS
        elif (
            line.startswith("-")
            or line.startswith("*")
        ):

            bullet = Paragraph(

                f"""
                <font size=11>
                • {line[1:].strip()}
                </font>
                """,

                styles["BodyText"]

            )

            elements.append(bullet)

            elements.append(Spacer(1, 8))

        # NORMAL TEXT
        else:

            paragraph = Paragraph(

                f"""
                <font size=11>
                {line}
                </font>
                """,

                styles["BodyText"]

            )

            elements.append(paragraph)

            elements.append(Spacer(1, 10))

    elements.append(Spacer(1, 25))

    # FOOTER
    footer = Paragraph(

        """
        <font size=9 color='grey'>
        Generated automatically by Automated Lead Intake System
        </font>
        """,

        styles["Italic"]

    )

    elements.append(footer)

    doc.build(elements)

    return pdf_path
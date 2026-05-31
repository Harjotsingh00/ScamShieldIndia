from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def create_report(
    filename,
    score,
    level,
    analysis
):
    """
    Generate PDF report
    """

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "ScamShield India Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Risk Score: {score}/100",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Level: {level}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            analysis,
            styles["BodyText"]
        )
    )

    doc.build(content)
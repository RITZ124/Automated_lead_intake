from datetime import datetime

from app.extensions import db


class Lead(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), nullable=False)

    company = db.Column(db.String(150), nullable=False)

    website = db.Column(db.String(200), nullable=False)

    message = db.Column(db.Text)

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    # ENRICHMENT
    company_title = db.Column(db.Text)

    meta_description = db.Column(db.Text)

    website_content = db.Column(db.Text)

    # AI REPORT
    ai_audit_report = db.Column(db.Text)

    # PDF
    pdf_report_path = db.Column(db.Text)

    # EMAIL STATUS
    email_sent = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):

        return f"<Lead {self.company}>"
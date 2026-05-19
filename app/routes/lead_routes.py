from flask import Blueprint, render_template, request, flash, redirect
import os
from app.utils.validators import (
    validate_email,
    validate_website,
    validate_required_fields
)

from app.models.lead import Lead

from app.extensions import db

from app.services.enrichment_service import enrich_company_data

from app.services.ai_service import generate_company_audit

from app.services.pdf_service import generate_pdf_report

from app.services.email_service import send_report_email

from app.services.sheets_service import log_lead_to_sheets

from app.services.drive_service import upload_pdf_to_drive

lead_bp = Blueprint("lead", __name__)


@lead_bp.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        lead_data = {

            "name": request.form.get("name"),

            "email": request.form.get("email"),

            "company": request.form.get("company"),

            "website": request.form.get("website"),

            "message": request.form.get("message")

        }

        # REQUIRED FIELDS
        missing_fields = validate_required_fields(
            lead_data
        )

        if missing_fields:

            flash(
                f"Missing fields: {', '.join(missing_fields)}",
                "danger"
            )

            return redirect("/")

        # EMAIL VALIDATION
        if not validate_email(lead_data["email"]):

            flash(
                "Invalid email address",
                "danger"
            )

            return redirect("/")

        # WEBSITE VALIDATION
        if not validate_website(lead_data["website"]):

            flash(
                "Invalid website URL",
                "danger"
            )

            return redirect("/")

        # WEBSITE ENRICHMENT
        enrichment_data = enrich_company_data(
            lead_data["website"]
        )

        # AI REPORT
        ai_report = generate_company_audit(
            enrichment_data
        )

        # TEMP OBJECT
        temp_lead = Lead(

            name=lead_data["name"],

            email=lead_data["email"],

            company=lead_data["company"],

            website=lead_data["website"],

            status="PDF Generated"

        )

        # GENERATE PDF
        pdf_path = generate_pdf_report(

            temp_lead,

            ai_report

        )

        # SEND EMAIL
        email_status = send_report_email(

            recipient_email=lead_data["email"],

            recipient_name=lead_data["name"],

            company_name=lead_data["company"],

            pdf_path=pdf_path

        )

        print("\n===== EMAIL STATUS =====")

        print(email_status)

        # GOOGLE SHEETS LOGGING
        sheet_status = log_lead_to_sheets({

            "name": lead_data["name"],

            "email": lead_data["email"],

            "company": lead_data["company"],

            "website": lead_data["website"],

            "status": "Completed"

        })

        print("\n===== SHEETS STATUS =====")

        print(sheet_status)

        # GOOGLE DRIVE PDF UPLOAD
        drive_status = upload_pdf_to_drive(
            pdf_path
        )

        print("\n===== DRIVE STATUS =====")

        print(drive_status)

        # SAVE TO DATABASE
        new_lead = Lead(

            name=lead_data["name"],

            email=lead_data["email"],

            company=lead_data["company"],

            website=lead_data["website"],

            message=lead_data["message"],

            company_title=enrichment_data.get(
                "title"
            ),

            meta_description=enrichment_data.get(
                "meta_description"
            ),

            website_content=enrichment_data.get(
                "website_text"
            ),

            ai_audit_report=ai_report,

            pdf_report_path=pdf_path,

            email_sent=email_status,

            status="Completed"

        )

        db.session.add(new_lead)

        db.session.commit()

        flash(

            "Lead processed, PDF generated, and email sent!",

            "success"

        )

        return redirect("/")

    return render_template("index.html")
@lead_bp.route("/admin")
def admin_dashboard():

    leads = Lead.query.order_by(
        Lead.created_at.desc()
    ).all()

    total_leads = Lead.query.count()

    emails_sent = Lead.query.filter_by(
        email_sent=True
    ).count()

    reports_generated = Lead.query.filter(
        Lead.pdf_report_path.isnot(None)
    ).count()

    completed_leads = Lead.query.filter_by(
        status="Completed"
    ).count()

    return render_template(

        "admin.html",

        leads=leads,

        total_leads=total_leads,

        emails_sent=emails_sent,

        reports_generated=reports_generated,

        completed_leads=completed_leads,

        os=os

    )
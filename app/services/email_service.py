import os

import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_report_email(

    recipient_email,

    recipient_name,

    company_name,

    pdf_path

):

    try:

        sender_email = os.getenv(
            "EMAIL_ADDRESS"
        )

        app_password = os.getenv(
            "EMAIL_APP_PASSWORD"
        )

        # EMAIL MESSAGE
        msg = EmailMessage()

        msg["Subject"] = (
            f"Your AI Business Audit Report - "
            f"{company_name}"
        )

        msg["From"] = sender_email

        msg["To"] = recipient_email

        # EMAIL BODY
        msg.set_content(f"""

Hello {recipient_name},

Thank you for submitting your company details.

We analyzed your business and generated a personalized AI-powered audit report.

Please find the attached PDF report.

Regards,
Automated Lead Intake System

""")

        # ATTACH PDF
        with open(pdf_path, "rb") as file:

            file_data = file.read()

            file_name = os.path.basename(
                pdf_path
            )

        msg.add_attachment(

            file_data,

            maintype="application",

            subtype="pdf",

            filename=file_name

        )

        # SMTP SERVER
        with smtplib.SMTP_SSL(

            "smtp.gmail.com",

            465

        ) as smtp:

            smtp.login(

                sender_email,

                app_password

            )

            smtp.send_message(msg)

        print("\n===== EMAIL SENT =====")

        return True

    except Exception as e:

        print("\n===== EMAIL ERROR =====")

        print(str(e))

        return False
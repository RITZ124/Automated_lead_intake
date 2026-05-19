import os

import resend

from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv(
    "RESEND_API_KEY"
)


def send_report_email(

    recipient_email,

    recipient_name,

    company_name,

    pdf_path

):

    try:

        params = {

            "from": "onboarding@resend.dev",

            "to": [recipient_email],

            "subject": f"AI Audit Report for {company_name}",

            "html": f"""

            <h2>Hello {recipient_name},</h2>

            <p>

            Your AI-powered business audit
            report has been generated successfully.

            </p>

            <p>

            Please find your personalized
            PDF audit report attached.

            </p>

            <br>

            <p>

            — Automated Lead Intake System

            </p>

            """,

            "attachments": [

                {

                    "filename":
                    os.path.basename(pdf_path),

                    "content":
                    open(pdf_path, "rb").read()

                }

            ]

        }

        resend.Emails.send(params)

        print("\n===== EMAIL SENT =====")

        return True

    except Exception as e:

        print("\n===== EMAIL ERROR =====")

        print(str(e))

        return False
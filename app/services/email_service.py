import os
import resend
import base64

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

        with open(
            pdf_path,
            "rb"
        ) as f:

            pdf_content = (
                base64.b64encode(
                    f.read()
                )
                .decode("utf-8")
            )

        resend.Emails.send({

            "from":
            "onboarding@resend.dev",

            "to":
            [recipient_email],

            "subject":
            f"AI Audit Report — {company_name}",

            "html":
            f"""
            <h2>Hello {recipient_name}</h2>

            <p>
            Your AI audit report is attached.
            </p>
            """,

            "attachments": [

                {

                    "filename":
                    os.path.basename(
                        pdf_path
                    ),

                    "content":
                    pdf_content

                }

            ]

        })

        print(
            "\n===== EMAIL SENT ====="
        )

        return True

    except Exception as e:

        print(
            "\n===== EMAIL ERROR ====="
        )

        print(e)

        return False

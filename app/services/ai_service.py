import os

from groq import Groq

from dotenv import load_dotenv

load_dotenv()

client = Groq(

    api_key=os.getenv("GROQ_API_KEY")

)


def generate_company_audit(company_data):

    prompt = f"""

You are an expert AI business consultant.

Analyze the following company data and generate
a highly personalized business audit report.

COMPANY TITLE:
{company_data.get("title")}

META DESCRIPTION:
{company_data.get("meta_description")}

WEBSITE CONTENT:
{company_data.get("website_text")}

Generate:

1. AI Readiness Score (out of 10)

2. Automation Potential Score (out of 10)

3. Digital Presence Score (out of 10)

4. Marketing Maturity Score (out of 10)

5. Executive Summary

6. What the company likely does

7. Business strengths

8. Potential weaknesses

9. AI automation opportunities

10. Marketing improvement suggestions

11. Lead generation suggestions

12. Personalized growth recommendations

IMPORTANT:

Return scores EXACTLY in this format:

AI Readiness Score: X/10
Automation Potential Score: X/10
Digital Presence Score: X/10
Marketing Maturity Score: X/10

Keep the report professional,
highly personalized,
and consulting-style.

"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.7,

            max_tokens=2000

        )

        audit_report = (
            response.choices[0]
            .message.content
        )

        return audit_report

    except Exception as e:

        return f"AI Generation Error: {str(e)}"
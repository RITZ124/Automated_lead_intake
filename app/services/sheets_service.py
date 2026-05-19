import gspread

from google.oauth2.service_account import Credentials

from datetime import datetime


SCOPES = [

    "https://www.googleapis.com/auth/spreadsheets",

    "https://www.googleapis.com/auth/drive"

]

SERVICE_ACCOUNT_FILE = (
    "credentials/google_credentials.json"
)


def log_lead_to_sheets(lead_data):

    try:

        credentials = Credentials.from_service_account_file(

            SERVICE_ACCOUNT_FILE,

            scopes=SCOPES

        )

        client = gspread.authorize(
            credentials
        )

        # OPEN SHEET
        sheet = client.open(
            "Automated Lead Tracker"
        ).sheet1

        # ADD ROW
        sheet.append_row([

            lead_data["name"],

            lead_data["email"],

            lead_data["company"],

            lead_data["website"],

            lead_data["status"],

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        ])

        print("\n===== SHEET UPDATED =====")

        return True

    except Exception as e:

        print("\n===== SHEETS ERROR =====")

        print(str(e))

        return False

import os

from google.oauth2.service_account import Credentials

from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload



SCOPES = [

    "https://www.googleapis.com/auth/drive"

]



def upload_pdf_to_drive(

    pdf_path

):

    try:

        creds = Credentials.from_service_account_file(

            "credentials/google_credentials.json",

            scopes=SCOPES

        )

        service = build(

            "drive",

            "v3",

            credentials=creds

        )

        folder_id = os.getenv(

            "GOOGLE_DRIVE_FOLDER_ID"

        )

        metadata = {

            "name":

            os.path.basename(

                pdf_path

            ),

            "parents":

            [folder_id]

        }

        media = MediaFileUpload(

            pdf_path,

            mimetype="application/pdf"

        )

        uploaded = service.files().create(

            body=metadata,

            media_body=media,

            fields="id"

        ).execute()

        print(

            "\n===== DRIVE UPLOADED ====="

        )

        print(

            uploaded["id"]

        )

        return True

    except Exception as e:

        print(

            "\n===== DRIVE ERROR ====="

        )

        print(e)

        return False

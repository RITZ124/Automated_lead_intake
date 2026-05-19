import os

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from google.auth.transport.requests import Request

from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload

import pickle

from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


def authenticate_drive():

    creds = None

    # TOKEN FILE
    if os.path.exists("token.pickle"):

        with open("token.pickle", "rb") as token:

            creds = pickle.load(token)

    # LOGIN FLOW
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(

                "credentials/oauth_credentials.json",

                SCOPES

            )

            creds = flow.run_local_server(
                port=0
            )

        # SAVE TOKEN
        with open("token.pickle", "wb") as token:

            pickle.dump(creds, token)

    return creds


def upload_pdf_to_drive(pdf_path):

    try:

        creds = authenticate_drive()

        service = build(
            "drive",
            "v3",
            credentials=creds
        )

        folder_id = os.getenv(
            "GOOGLE_DRIVE_FOLDER_ID"
        )

        file_metadata = {

            "name": os.path.basename(
                pdf_path
            ),

            "parents": [folder_id]

        }

        media = MediaFileUpload(

            pdf_path,

            mimetype="application/pdf"

        )

        uploaded_file = service.files().create(

            body=file_metadata,

            media_body=media,

            fields="id"

        ).execute()

        print("\n===== PDF UPLOADED =====")

        print(uploaded_file.get("id"))

        return True

    except Exception as e:

        print("\n===== DRIVE ERROR =====")

        print(str(e))

        return False
from flask import Flask, send_from_directory

from app.extensions import db
from app.routes.lead_routes import lead_bp

import os
import json


# REBUILD GOOGLE CREDENTIAL FILE
google_creds = os.getenv(
    "GOOGLE_CREDENTIALS_JSON"
)

if google_creds:

    os.makedirs(
        "credentials",
        exist_ok=True
    )

    with open(
        "credentials/google_credentials.json",
        "w"
    ) as f:

        f.write(
            google_creds
        )


app = Flask(

    __name__,

    template_folder="app/templates",

    static_folder="app/static"

)

app.secret_key = "supersecretkey"


# DATABASE CONFIG
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///database.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


# INITIALIZE DATABASE
db.init_app(app)


# REGISTER ROUTES
app.register_blueprint(
    lead_bp
)


# CREATE DATABASE
with app.app_context():

    db.create_all()


# PDF DOWNLOAD
@app.route(
    "/generated_reports/<path:filename>"
)
def download_report(

    filename

):

    return send_from_directory(

        "generated_reports",

        filename,

        as_attachment=False

    )


if __name__ == "__main__":

    app.run(
        debug=True
    )

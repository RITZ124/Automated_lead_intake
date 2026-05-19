import re
from urllib.parse import urlparse


def validate_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email)


def validate_website(url):

    parsed = urlparse(url)

    return all([parsed.scheme, parsed.netloc])


def validate_required_fields(data):

    required_fields = [
        "name",
        "email",
        "company",
        "website"
    ]

    missing_fields = []

    for field in required_fields:

        if not data.get(field):
            missing_fields.append(field)

    return missing_fields
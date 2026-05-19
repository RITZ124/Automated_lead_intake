import requests
import re

from bs4 import BeautifulSoup


def clean_text(text):

    # REMOVE EXTRA WHITESPACES
    text = re.sub(r"\s+", " ", text)

    # REMOVE WEIRD CHARACTERS
    text = re.sub(r"[^a-zA-Z0-9.,!?@()\-:;/ ]", "", text)

    return text.strip()


def enrich_company_data(url):

    try:

        headers = {

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )

        }

        response = requests.get(

            url,

            headers=headers,

            timeout=10

        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # REMOVE SCRIPTS & STYLES
        for tag in soup(["script", "style", "noscript"]):

            tag.decompose()

        # TITLE
        title = (
            soup.title.string.strip()
            if soup.title
            else "No title found"
        )

        # META DESCRIPTION
        meta_description = ""

        meta_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_tag:

            meta_description = meta_tag.get(
                "content",
                ""
            )

        else:

            meta_description = "No description found"

        # EXTRACT TEXT
        paragraphs = soup.find_all(["p", "h1", "h2", "h3"])

        content_list = []

        for para in paragraphs:

            text = para.get_text(strip=True)

            text = clean_text(text)

            # REMOVE VERY SHORT TEXT
            if len(text) > 40:

                # REMOVE DUPLICATES
                if text not in content_list:

                    content_list.append(text)

        website_text = " ".join(content_list)

        # LIMIT SIZE
        website_text = website_text[:5000]

        enriched_data = {

            "title": clean_text(title),

            "meta_description": clean_text(
                meta_description
            ),

            "website_text": website_text

        }

        return enriched_data

    except Exception as e:

        return {

            "error": str(e)

        }
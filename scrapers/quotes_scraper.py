import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from utils.http_client import create_session, get_page


logger = logging.getLogger(__name__)


class QuotesScraper:

    BASE_URL = "https://quotes.toscrape.com/"

    def __init__(self):
        self.session = create_session()

    def scrape(self):
        records = []
        current_url = self.BASE_URL
        page_number = 1

        while current_url:

            logger.info(
                "Scraping Quotes page %s: %s",
                page_number,
                current_url
            )

            try:
                response = get_page(
                    self.session,
                    current_url
                )

            except Exception as error:
                logger.error(
                    "Failed to scrape Quotes page %s: %s",
                    current_url,
                    error
                )
                break

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            quotes = soup.select("div.quote")

            logger.info(
                "Found %s quotes on page %s",
                len(quotes),
                page_number
            )

            for quote in quotes:

                try:
                    # -----------------------------
                    # Extract quote elements
                    # -----------------------------
                    text_element = quote.select_one(
                        "span.text"
                    )

                    author_element = quote.select_one(
                        "small.author"
                    )

                    tag_elements = quote.select(
                        "a.tag"
                    )

                    # -----------------------------
                    # Extract quote text
                    # -----------------------------
                    text = (
                        text_element.get_text(strip=True)
                        if text_element
                        else None
                    )

                    # -----------------------------
                    # Extract author
                    # -----------------------------
                    author = (
                        author_element.get_text(strip=True)
                        if author_element
                        else None
                    )

                    # -----------------------------
                    # Extract tags
                    # -----------------------------
                    tags = [
                        tag.get_text(strip=True)
                        for tag in tag_elements
                    ]

                    # -----------------------------
                    # Create standardized record
                    # -----------------------------
                    record = {
                        "source": "Quotes to Scrape",
                        "source_url": current_url,
                        "quote": text,
                        "author": author,
                        "tags": tags
                    }

                    records.append(record)

                except Exception as error:
                    logger.exception(
                        "Failed to parse a quote: %s",
                        error
                    )

            # -----------------------------
            # Find next page
            # -----------------------------
            next_link = soup.select_one(
                "li.next > a"
            )

            if next_link and next_link.get("href"):

                current_url = urljoin(
                    current_url,
                    next_link["href"]
                )

                page_number += 1

            else:
                current_url = None

        logger.info(
            "Quotes scraping completed. Total records: %s",
            len(records)
        )

        return records
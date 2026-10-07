import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from utils.http_client import create_session, get_page


logger = logging.getLogger(__name__)


class BooksScraper:

    BASE_URL = "https://books.toscrape.com/"

    def __init__(self):
        self.session = create_session()

    def scrape(self):
        records = []
        current_url = self.BASE_URL
        page_number = 1

        while current_url:

            logger.info(
                "Scraping Books page %s: %s",
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
                    "Failed to scrape Books page %s: %s",
                    current_url,
                    error
                )
                break

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            books = soup.select("article.product_pod")

            logger.info(
                "Found %s books on page %s",
                len(books),
                page_number
            )

            for book in books:

                try:
                    # -----------------------------
                    # Extract book elements
                    # -----------------------------
                    title_element = book.select_one("h3 a")

                    price_element = book.select_one(
                        "p.price_color"
                    )

                    availability_element = book.select_one(
                        "p.instock.availability"
                    )

                    rating_element = book.select_one(
                        "p.star-rating"
                    )

                    # -----------------------------
                    # Extract title
                    # -----------------------------
                    title = (
                        title_element.get("title")
                        if title_element
                        else None
                    )

                    # -----------------------------
                    # Extract price
                    # -----------------------------
                    price = (
                        price_element.get_text(strip=True)
                        if price_element
                        else None
                    )

                    # -----------------------------
                    # Extract availability
                    # -----------------------------
                    availability = (
                        availability_element.get_text(
                            " ",
                            strip=True
                        )
                        if availability_element
                        else None
                    )

                    # -----------------------------
                    # Extract rating
                    # -----------------------------
                    rating = (
                        rating_element.get("class")
                        if rating_element
                        else None
                    )

                    # -----------------------------
                    # Build original product URL
                    # -----------------------------
                    product_url = (
                        urljoin(
                            current_url,
                            title_element.get("href")
                        )
                        if title_element
                        else None
                    )

                    # -----------------------------
                    # Create standardized record
                    # -----------------------------
                    record = {
                        "source": "Books to Scrape",
                        "source_url": product_url,
                        "title": title,
                        "price": price,
                        "availability": availability,
                        "rating": rating
                    }

                    records.append(record)

                except Exception as error:
                    logger.exception(
                        "Failed to parse a book: %s",
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
            "Books scraping completed. Total records: %s",
            len(records)
        )

        return records
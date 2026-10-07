import math
from urllib.parse import urlparse


VALID_SOURCES = {"Books to Scrape", "Quotes to Scrape"}


def validate_record(rec):
    problems = []

    if not isinstance(rec, dict):
        return ["invalid_record"]

    source = str(rec.get("source") or "").strip()
    if source not in VALID_SOURCES:
        problems.append("unknown_source")

    name_or_title = rec.get("name_or_title")
    if name_or_title is None or (isinstance(name_or_title, str) and not name_or_title.strip()) or not name_or_title:
        problems.append("missing_name")

    url = str(rec.get("source_url") or "").strip()
    parsed = urlparse(url)

    if not url or parsed.scheme not in ("http", "https") or not parsed.netloc:
        problems.append("invalid_url")

    price = rec.get("price")
    if price is not None:
        is_valid_number = isinstance(price, (int, float)) and not isinstance(price, bool) and math.isfinite(price)
        if not is_valid_number or price < 0:
            problems.append("invalid_price")

    rating = rec.get("rating")
    if rating is not None:
        is_valid_rating = isinstance(rating, (int, float)) and not isinstance(rating, bool) and math.isfinite(rating)
        if not is_valid_rating or rating not in (1, 2, 3, 4, 5):
            problems.append("invalid_rating")

    return problems
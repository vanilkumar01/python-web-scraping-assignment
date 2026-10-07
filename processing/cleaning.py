def clean_text(value):
    """Remove extra spaces from text."""
    if value is None:
        return None

    value = str(value).strip()

    return value if value else None


def clean_price(value):
    """Convert price like £51.77 into 51.77."""
    if value is None:
        return None

    try:
        value = str(value).replace("£", "").replace("Â", "").strip()
        return float(value)
    except (ValueError, AttributeError):
        return None


def clean_rating(value):
    """Convert rating words into numbers."""

    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    if not value:
        return None

    if isinstance(value, list):
        rating_word = value[-1]
    else:
        rating_word = str(value).strip()

    return ratings.get(rating_word)


def clean_url(value):
    """Keep only HTTP/HTTPS URLs."""

    if not value:
        return None

    value = str(value).strip()

    if value.startswith("http://") or value.startswith("https://"):
        return value

    return None
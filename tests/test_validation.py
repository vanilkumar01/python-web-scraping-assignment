from processing.validation import validate_record


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Example Book",
        "price": 25.50,
        "rating": 4
    }

    assert validate_record(record) == []


def test_unknown_source():
    record = {
        "source": "Unknown Website",
        "source_url": "https://example.com/",
        "name_or_title": "Example Book",
        "price": 25.50,
        "rating": 4
    }

    assert "unknown_source" in validate_record(record)


def test_missing_name():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": None,
        "price": 25.50,
        "rating": 4
    }

    assert "missing_name" in validate_record(record)


def test_invalid_url():
    record = {
        "source": "Books to Scrape",
        "source_url": "not-a-url",
        "name_or_title": "Example Book",
        "price": 25.50,
        "rating": 4
    }

    assert "invalid_url" in validate_record(record)


def test_invalid_price():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Example Book",
        "price": -10,
        "rating": 4
    }

    assert "invalid_price" in validate_record(record)


def test_invalid_rating():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Example Book",
        "price": 25.50,
        "rating": 6
    }

    assert "invalid_rating" in validate_record(record)
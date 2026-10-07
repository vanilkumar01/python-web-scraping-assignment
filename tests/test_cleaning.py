from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_url
)


def test_clean_text():
    assert clean_text("  Book Title  ") == "Book Title"
    assert clean_text("") is None
    assert clean_text(None) is None


def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price(" £20.50 ") == 20.50
    assert clean_price("invalid") is None
    assert clean_price(None) is None


def test_clean_rating():
    assert clean_rating("One") == 1
    assert clean_rating("Three") == 3
    assert clean_rating("Five") == 5
    assert clean_rating(["star-rating", "Four"]) == 4
    assert clean_rating("Invalid") is None


def test_clean_url():
    assert clean_url(" https://example.com ") == "https://example.com"
    assert clean_url("http://example.com") == "http://example.com"
    assert clean_url("example.com") is None
    assert clean_url("invalid") is None
    assert clean_url(None) is None
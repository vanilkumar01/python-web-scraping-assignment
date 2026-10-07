import pandas as pd

from processing.consolidation import consolidate_data


def test_consolidation_standardizes_columns():
    data = pd.DataFrame([
        {
            "Title": "Book A",
            "Price": "£10.99",
            "Author": "Author A",
            "Source": "books"
        }
    ])

    result = consolidate_data(data)

    expected_columns = [
        "title",
        "price",
        "availability",
        "rating",
        "description",
        "author",
        "tags",
        "source"
    ]

    assert list(result.columns) == expected_columns
    assert result.iloc[0]["title"] == "Book A"
    assert result.iloc[0]["source"] == "books"


def test_consolidation_adds_missing_columns():
    data = pd.DataFrame([
        {
            "title": "Book A",
            "source": "books"
        }
    ])

    result = consolidate_data(data)

    assert "price" in result.columns
    assert "author" in result.columns
    assert "tags" in result.columns
    assert len(result) == 1
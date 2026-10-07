def normalize(value):
    """Make text consistent for comparison."""
    if value is None:
        return ""

    return " ".join(str(value).lower().split())


def find_duplicates(records):
    """
    Find duplicate records using source, title and author.
    """

    seen = set()
    unique_records = []
    duplicate_records = []

    for record in records:
        source = normalize(record.get("source"))
        title = normalize(record.get("name_or_title"))
        author = normalize(record.get("author"))

        key = (source, title, author)

        if key in seen:
            duplicate_records.append(record)
        else:
            seen.add(key)
            unique_records.append(record)

    return unique_records, duplicate_records
import hashlib, re

def make_fingerprint(rec):
    if rec["source"] == "Books to Scrape":
        key = f'{rec["source"]} {rec["name_or_title"]}'
    else:                                           # quotes
        key = f'{rec["source"]} {rec["author"]} {rec["name_or_title"][:50]}'
    key = re.sub(r"[^\w\s]", "", key.lower())      # lowercase, drop punctuation
    key = " ".join(key.split())                     # collapse spaces
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def find_duplicates(records):
    seen, unique, dupes = set(), [], []
    for rec in records:
        fp = make_fingerprint(rec)
        (dupes if fp in seen else unique).append(rec)
        seen.add(fp)
    return unique, dupes


def test_duplicates_ignore_case_and_spaces():
    base = {"source": "Books to Scrape", "author": None}
    records = [
        {**base, "name_or_title": "Example Book Title"},
        {**base, "name_or_title": "  Example Book Title "},
        {**base, "name_or_title": "EXAMPLE BOOK TITLE"},
    ]
    unique, dupes = find_duplicates(records)
    assert len(unique) == 1 and len(dupes) == 2
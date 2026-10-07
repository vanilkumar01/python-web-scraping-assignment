import pandas as pd


def consolidate_data(df):
    """
    Create one standardized dataset from all validated records.
    """

    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    standard_columns = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "availability"
    ]

    # Add missing columns
    for column in standard_columns:
        if column not in df.columns:
            df[column] = None

    # Keep consistent column order
    df = df[standard_columns]

    # Normalize missing source
    df["source"] = df["source"].fillna("unknown")

    # Reset index
    df = df.reset_index(drop=True)

    return df
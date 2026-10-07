import json
import logging
import os
import time

import pandas as pd

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_url
)

from processing.validation import validate_record
from processing.deduplication import find_duplicates
from processing.consolidation import consolidate_data


# ============================================================
# DIRECTORIES
# ============================================================

OUTPUT_DIR = "output"
LOG_DIR = "logs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# STANDARDIZE RECORD
# ============================================================

def standardize_record(record):
    """
    Convert records from different scrapers
    into a common structure.
    """

    name_or_title = (
        record.get("name_or_title")
        or record.get("title")
        or record.get("quote")
    )

    return {
        "source": record.get("source"),
        "source_url": (
            record.get("source_url")
            or record.get("url")
        ),
        "name_or_title": name_or_title,
        "category": record.get("category"),
        "price": record.get("price"),
        "rating": record.get("rating"),
        "author": record.get("author"),
        "tags": record.get("tags"),
        "description": record.get("description"),
        "availability": record.get("availability"),
        "scraped_at": record.get("scraped_at")
    }


# ============================================================
# CLEAN RECORD
# ============================================================

def clean_record(record):
    """
    Clean and normalize one record.
    """

    cleaned = record.copy()

    cleaned["source"] = clean_text(
        cleaned.get("source")
    )

    cleaned["source_url"] = clean_url(
        cleaned.get("source_url")
    )

    cleaned["name_or_title"] = clean_text(
        cleaned.get("name_or_title")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category")
    )

    cleaned["price"] = clean_price(
        cleaned.get("price")
    )

    cleaned["rating"] = clean_rating(
        cleaned.get("rating")
    )

    cleaned["author"] = clean_text(
        cleaned.get("author")
    )

    cleaned["description"] = clean_text(
        cleaned.get("description")
    )

    cleaned["availability"] = clean_text(
        cleaned.get("availability")
    )

    return cleaned


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    start_time = time.time()

    logger.info("=" * 70)
    logger.info("STARTING WEB SCRAPING DATA PIPELINE")
    logger.info("=" * 70)

    # --------------------------------------------------------
    # 1. SCRAPING
    # --------------------------------------------------------

    print("\n[1/6] SCRAPING")

    logger.info("Starting Books scraping")

    books_scraper = BooksScraper()
    books = books_scraper.scrape()

    logger.info(
        "Books scraping completed. Records: %s",
        len(books)
    )

    logger.info("Starting Quotes scraping")

    quotes_scraper = QuotesScraper()
    quotes = quotes_scraper.scrape()

    logger.info(
        "Quotes scraping completed. Records: %s",
        len(quotes)
    )

    all_records = books + quotes

    books_count = len(books)
    quotes_count = len(quotes)
    total_collected = len(all_records)

    print(f"Books scraped  : {books_count}")
    print(f"Quotes scraped : {quotes_count}")
    print(f"Total collected: {total_collected}")

    logger.info(
        "Total records collected: %s",
        total_collected
    )

    # --------------------------------------------------------
    # 2. CLEANING
    # --------------------------------------------------------

    print("\n[2/6] CLEANING")

    logger.info("Starting data cleaning")

    standardized_records = [
        standardize_record(record)
        for record in all_records
    ]

    cleaned_records = [
        clean_record(record)
        for record in standardized_records
    ]

    records_after_cleaning = len(cleaned_records)

    print(
        f"Records after cleaning: "
        f"{records_after_cleaning}"
    )

    logger.info(
        "Cleaning completed. Records: %s",
        records_after_cleaning
    )

    # --------------------------------------------------------
    # 3. VALIDATION
    # --------------------------------------------------------

    print("\n[3/6] VALIDATION")

    logger.info("Starting validation")

    valid_records = []
    rejected_records = []

    validation_errors = {}

    for record in cleaned_records:

        problems = validate_record(record)

        if problems:

            rejected_records.append({
                "record": record,
                "problems": problems
            })

            for problem in problems:
                validation_errors[problem] = (
                    validation_errors.get(problem, 0) + 1
                )

        else:
            valid_records.append(record)

    records_rejected = len(rejected_records)

    print(
        f"Valid records    : {len(valid_records)}"
    )

    print(
        f"Rejected records : {records_rejected}"
    )

    logger.info(
        "Validation completed. Valid: %s, Rejected: %s",
        len(valid_records),
        records_rejected
    )

    if validation_errors:
        logger.warning(
            "Validation errors: %s",
            validation_errors
        )

    # --------------------------------------------------------
    # STOP IF NO VALID RECORDS
    # --------------------------------------------------------

    if not valid_records:

        logger.error(
            "No valid records remain after validation"
        )

        raise RuntimeError(
            "No valid records remain after processing."
        )

    # --------------------------------------------------------
    # 4. DEDUPLICATION
    # --------------------------------------------------------

    print("\n[4/6] DEDUPLICATION")

    logger.info("Starting duplicate detection")

    unique_records, duplicate_records = find_duplicates(
        valid_records
    )

    duplicate_count = len(duplicate_records)

    print(
        "Records before deduplication : "
        f"{len(valid_records)}"
    )

    print(
        "Duplicate records detected   : "
        f"{duplicate_count}"
    )

    print(
        "Unique records remaining     : "
        f"{len(unique_records)}"
    )

    logger.info(
        "Deduplication completed. Duplicates: %s",
        duplicate_count
    )

    # --------------------------------------------------------
    # 5. CONSOLIDATION
    # --------------------------------------------------------

    print("\n[5/6] CONSOLIDATION")

    logger.info("Starting data consolidation")

    final_df = pd.DataFrame(unique_records)

    final_df = consolidate_data(final_df)

    if final_df.empty:

        logger.error(
            "Final dataset is empty after consolidation"
        )

        raise RuntimeError(
            "Final dataset is empty after consolidation."
        )

    final_record_count = len(final_df)
    final_column_count = len(final_df.columns)

    print(
        f"Final records : {final_record_count}"
    )

    print(
        f"Final columns : {final_column_count}"
    )

    logger.info(
        "Consolidation completed. "
        "Records: %s, Columns: %s",
        final_record_count,
        final_column_count
    )

    # --------------------------------------------------------
    # 6. EXPORT
    # --------------------------------------------------------

    print("\n[6/6] EXPORT")

    logger.info("Starting export")

    csv_path = os.path.join(
        OUTPUT_DIR,
        "final_dataset.csv"
    )

    final_df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info(
        "CSV exported successfully: %s",
        csv_path
    )

    # --------------------------------------------------------
    # SUMMARY REPORT
    # --------------------------------------------------------

    execution_time = round(
        time.time() - start_time,
        2
    )

    summary = {
        "books_records_collected": books_count,
        "quotes_records_collected": quotes_count,
        "total_records_collected": total_collected,
        "records_after_cleaning": records_after_cleaning,
        "records_rejected": records_rejected,
        "validation_errors": validation_errors,
        "duplicate_records_detected": duplicate_count,
        "final_record_count": final_record_count,
        "final_column_count": final_column_count,
        "execution_time_seconds": execution_time
    }

    json_path = os.path.join(
        OUTPUT_DIR,
        "summary_report.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False
        )

    logger.info(
        "Summary report exported successfully: %s",
        json_path
    )

    # --------------------------------------------------------
    # VERIFY OUTPUT
    # --------------------------------------------------------

    if os.path.exists(csv_path):

        exported_df = pd.read_csv(
            csv_path
        )

        logger.info(
            "CSV verification successful. "
            "Rows: %s, Columns: %s",
            len(exported_df),
            len(exported_df.columns)
        )

    else:

        logger.error(
            "CSV verification failed"
        )

    # --------------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(
        f"Final records       : {final_record_count}"
    )

    print(
        f"Final columns       : {final_column_count}"
    )

    print(
        f"Duplicates removed  : {duplicate_count}"
    )

    print(
        f"Execution time      : {execution_time} seconds"
    )

    print(
        f"\nCSV saved to        : {csv_path}"
    )

    print(
        f"Summary saved to    : {json_path}"
    )

    print(
        f"Log saved to        : "
        f"{os.path.join(LOG_DIR, 'scraper.log')}"
    )

    logger.info("=" * 70)
    logger.info(
        "PIPELINE COMPLETED SUCCESSFULLY"
    )
    logger.info(
        "Final records: %s",
        final_record_count
    )
    logger.info(
        "Execution time: %s seconds",
        execution_time
    )
    logger.info("=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        main()

    except Exception as error:

        logger.exception(
            "Pipeline failed: %s",
            error
        )

        print(
            f"\nERROR: {error}"
        )

        raise
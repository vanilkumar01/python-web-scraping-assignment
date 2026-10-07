# Web Scraping & Data Processing Pipeline

## 1. Project Overview

This project implements a modular Python web scraping and
data-processing pipeline using two public practice websites:

-   **Books to Scrape**
-   **Quotes to Scrape**

The pipeline collects data from both sources, cleans and standardizes
the records, validates data quality, detects duplicates, consolidates
the records into a common schema, and exports the final dataset and
processing metrics.

### End-to-End Workflow

``` text
Books to Scrape ─────┐
                     ├──> Scraping
Quotes to Scrape ────┘
                          ↓
                    Cleaning
                          ↓
                    Validation
                     ↙        ↘
                 Valid       Rejected
                    ↓
               Deduplication
                    ↓
               Consolidation
                    ↓
                  Export
             ↙              ↘
 final_dataset.csv    summary_report.json
```

------------------------------------------------------------------------

## 2. Project Objectives

The main objectives are:

1.  Scrape multiple pages from both websites.
2.  Handle pagination.
3.  Keep source-specific scraping logic separate.
4.  Capture the source and original source URL.
5.  Clean and standardize scraped data.
6.  Validate required fields and data types.
7.  Detect and remove duplicate records.
8.  Consolidate records into one common schema.
9.  Handle errors and maintain execution logs.
10. Export a final CSV dataset.
11. Generate a JSON summary report.
12. Maintain a test suite for core processing logic.

------------------------------------------------------------------------

## 3. Technologies Used

  Technology               Purpose
  ------------------------ --------------------------------
  Python                   Main programming language
  Requests / HTTP client   HTTP requests
  BeautifulSoup            HTML parsing and extraction
  Pandas                   Data processing and CSV export
  JSON                     Summary report generation
  Logging                  Execution and error logging
  Pytest                   Automated testing

------------------------------------------------------------------------

## 4. Project Structure

``` text
project/
│
├── scrapers/
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── cleaning.py
│   ├── validation.py
│   ├── deduplication.py
│   └── consolidation.py
│
├── utils/
│   └── http_client.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   ├── test_deduplication.py
│   └── test_consolidation.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

------------------------------------------------------------------------

# 5. Module-by-Module Explanation

## 5.1 `scrapers/books_scraper.py`

### Responsibility

Scrapes book records from Books to Scrape.

### Main operations

-   Creates an HTTP session.
-   Requests the website pages.
-   Parses HTML using BeautifulSoup.
-   Finds book cards using:

``` python
article.product_pod
```

-   Extracts:
    -   title
    -   price
    -   availability
    -   rating
    -   product URL
    -   source

### Pagination

The scraper checks for the Next button:

``` python
li.next > a
```

If the link exists, `urljoin()` creates the next absolute URL and the
scraper continues.

The scraper stops when there is no Next link.

### Output

Each book is returned as a dictionary containing source metadata and
scraped fields.

------------------------------------------------------------------------

## 5.2 `scrapers/quotes_scraper.py`

### Responsibility

Scrapes quote records from Quotes to Scrape.

### Main operations

-   Creates an HTTP session.
-   Requests each page.
-   Parses HTML with BeautifulSoup.
-   Finds quote blocks using:

``` python
div.quote
```

-   Extracts:
    -   quote text
    -   author
    -   tags
    -   source URL
    -   source

### Pagination

The scraper follows the website's Next link until there are no more
pages.

------------------------------------------------------------------------

# 6. Cleaning and Standardization

## `processing/cleaning.py`

The cleaning stage converts raw scraped values into consistent values.

### Text cleaning

Removes leading/trailing whitespace and treats empty values as missing.

Example:

``` text
"   Hello World   "
        ↓
"Hello World"
```

### Price cleaning

Converts a price string into a numeric value.

Example:

``` text
£51.77
   ↓
51.77
```

### Rating cleaning

Books to Scrape represents ratings as words/classes. The cleaning logic
standardizes them to numbers.

Example:

``` text
Three
  ↓
3
```

### URL cleaning

Only HTTP/HTTPS URLs are retained.

------------------------------------------------------------------------

# 7. Validation

## `processing/validation.py`

Validation checks whether a cleaned record satisfies the project's
data-quality rules.

### Validation checks

-   Recognized source.
-   Required name/title or quote exists.
-   Source URL is a valid-looking HTTP/HTTPS URL.
-   Price is numeric and non-negative when present.
-   Rating is within the range 1--5 when present.

### Validation result

Valid records continue through the pipeline.

Invalid records are rejected and their validation reasons are tracked in
the summary report.

### Example

``` text
Invalid rating
      ↓
invalid_rating
      ↓
record rejected
```

An empty validation error object:

``` json
"validation_errors": {}
```

means no records failed validation.

------------------------------------------------------------------------

# 8. Deduplication

## `processing/deduplication.py`

The deduplication stage removes duplicate records before final
consolidation.

### Normalization

Values are normalized by:

-   converting text to lowercase
-   removing extra whitespace

For example:

``` text
"  Hello World  "
        ↓
"hello world"
```

### Duplicate key

The current strategy uses a combination of:

``` text
source + name_or_title + author
```

This allows the pipeline to identify records that are equivalent despite
case or whitespace differences.

### Output

The function separates records into:

``` text
unique_records
duplicate_records
```

Only unique records continue to the final dataset.

------------------------------------------------------------------------

# 9. Consolidation

## `processing/consolidation.py`

The two websites provide different fields. Consolidation maps them into
a common standardized dataset.

### Final schema

The final dataset contains 10 standard columns:

``` text
source
source_url
name_or_title
category
price
rating
author
tags
description
availability
```

This allows data from both sources to exist in one consistent dataset.

------------------------------------------------------------------------

# 10. Main Pipeline

## `main.py`

`main.py` acts as the pipeline orchestrator.

The execution order is:

``` text
1. Scraping
      ↓
2. Cleaning
      ↓
3. Validation
      ↓
4. Deduplication
      ↓
5. Consolidation
      ↓
6. Export
```

It also:

-   records execution time
-   logs important events
-   creates output directories
-   generates the final CSV
-   generates the summary JSON
-   verifies the exported CSV
-   reports processing metrics

------------------------------------------------------------------------

# 11. Error Handling and Logging

The project uses Python's `logging` module.

Logs are written to:

``` text
logs/scraper.log
```

### Logged events include

-   scraping start
-   page being scraped
-   records found on a page
-   scraping completion
-   parsing errors
-   HTTP/request failures
-   cleaning completion
-   validation results
-   duplicate count
-   consolidation results
-   export completion
-   pipeline failures

Example:

``` text
2026-10-07 06:10:21 - INFO - Starting Books scraping
2026-10-07 06:10:22 - INFO - Found 20 books on page 1
2026-10-07 06:10:35 - INFO - Books scraping completed. Records: 1000
```

Errors are logged without silently hiding failures.

------------------------------------------------------------------------

# 12. Output Files

## `output/final_dataset.csv`

This is the final consolidated dataset after:

``` text
Cleaning
→ Validation
→ Deduplication
→ Consolidation
```

## `output/summary_report.json`

Contains processing metrics such as:

``` json
{
    "books_records_collected": 1000,
    "quotes_records_collected": 100,
    "total_records_collected": 1100,
    "records_after_cleaning": 1100,
    "records_rejected": 0,
    "validation_errors": {},
    "duplicate_records_detected": 1,
    "final_record_count": 1099,
    "final_column_count": 10,
    "execution_time_seconds": 24.51
}
```

### Interpretation of the current run

``` text
Books collected       : 1000
Quotes collected      : 100
Total collected       : 1100
After cleaning        : 1100
Rejected              : 0
Duplicates detected   : 1
Final records         : 1099
Final columns         : 10
Execution time        : 24.51 seconds
```

The final count is:

``` text
1100 - 1 duplicate = 1099
```

------------------------------------------------------------------------

# 13. Testing

The project includes tests for core processing components.

Run all tests with:

``` bash
pytest -v
```

The tests cover areas such as:

-   text cleaning
-   price cleaning
-   rating cleaning
-   URL cleaning
-   valid records
-   invalid sources
-   missing required names
-   invalid URLs
-   invalid prices
-   invalid ratings
-   duplicate detection
-   consolidation and standard columns

Example output:

``` text
tests/test_cleaning.py
tests/test_validation.py
tests/test_deduplication.py
tests/test_consolidation.py

PASSED
```

------------------------------------------------------------------------

# 14. Installation

Clone or copy the project and install the dependencies:

``` bash
pip install -r requirements.txt
```

If a virtual environment is used:

``` bash
python -m venv venv
```

Windows:

``` bash
venv\Scripts\activate
```

Then:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 15. Running the Project

Run the complete pipeline with:

``` bash
python main.py
```

The console shows the six stages:

``` text
[1/6] SCRAPING
[2/6] CLEANING
[3/6] VALIDATION
[4/6] DEDUPLICATION
[5/6] CONSOLIDATION
[6/6] EXPORT
```

After successful execution, check:

``` text
output/final_dataset.csv
output/summary_report.json
logs/scraper.log
```

------------------------------------------------------------------------

# 16. Interview Explanation

## 30-Second Explanation

> I developed a modular Python web-scraping and data-processing pipeline
> using Books to Scrape and Quotes to Scrape. I created separate scraper
> classes because each source has a different HTML structure. The
> scraped data is cleaned and standardized, then validated for required
> fields, URLs, prices, ratings, and source values. I use normalized
> composite keys for duplicate detection and then consolidate both
> sources into a common 10-column schema. Finally, I export the final
> dataset as CSV and generate a JSON summary report with processing
> metrics and execution time.

## 60-Second Explanation

> The pipeline starts by scraping multiple pages from two websites using
> separate scraper modules. Each scraper captures source metadata and
> the original source URL and handles pagination. The records are then
> passed through a cleaning layer that normalizes text, prices, ratings,
> and URLs. The validation layer checks source, required fields, URLs,
> prices, and ratings. Valid records are passed to deduplication, where
> normalized source, title or quote, and author values are used to
> detect duplicates. The remaining records are consolidated into a
> common 10-column schema and exported to CSV. A JSON summary report
> records counts, rejected records, validation errors, duplicates, final
> records, columns, and execution time. Logging provides traceability
> for scraping and processing errors.

------------------------------------------------------------------------

# 17. Key Interview Questions

### Why separate the scrapers?

Because the websites have different HTML structures and fields. Separate
classes keep source-specific logic isolated and maintainable.

### Why BeautifulSoup?

It provides a simple way to parse HTML and extract elements using CSS
selectors.

### How is pagination handled?

The scraper finds the Next link, resolves its URL using `urljoin()`, and
continues until the Next link is absent.

### Why clean the data?

Raw web data may contain whitespace, formatted prices, rating words,
missing values, and inconsistent URLs. Cleaning makes it suitable for
validation and analysis.

### How is validation performed?

The pipeline checks the source, required name/title or quote, URL
format, price, and rating range.

### How does deduplication work?

Relevant values are normalized and combined into a composite key. If the
key has already been seen, the record is classified as a duplicate.

### Why consolidate the records?

The two sources have different structures. A common schema makes the
final dataset consistent and easier to process.

### Why is `validation_errors` empty?

Because all 1,100 records passed validation.

### Why are there 1,099 final records?

There were 1,100 valid records and one duplicate was removed.

### Why use logging?

Logging provides traceability for page-level activity, parsing errors,
request failures, and pipeline stages without relying only on console
output.

------------------------------------------------------------------------

# 18. Design Decisions

### Modular architecture

Scraping, cleaning, validation, deduplication, and consolidation are
separated into different modules.

### Single responsibility

Each module focuses on one major responsibility.

### Reusable HTTP session

A shared session is created for each scraper to handle requests
consistently.

### Defensive error handling

Exceptions are logged so individual scraping failures can be diagnosed.

### Data quality before export

Records are cleaned, validated, deduplicated, and consolidated before
being written to the final dataset.

------------------------------------------------------------------------

# 19. Limitations and Possible Improvements

Potential future improvements include:

-   retry failed requests with exponential backoff
-   configurable request timeout and retry count
-   command-line arguments for output paths
-   more detailed data-quality metrics
-   configurable deduplication strategies
-   additional scraper unit tests
-   automated CI test execution
-   structured logging
-   configurable user-agent and rate limiting

These are future improvements rather than requirements for the current
implementation.

------------------------------------------------------------------------

# 20. Final Deliverables

The completed project should contain:

``` text
README.md
AI_USAGE.md
requirements.txt
main.py

scrapers/
processing/
utils/
tests/

output/
    final_dataset.csv
    summary_report.json

logs/
    scraper.log
```

------------------------------------------------------------------------

# 21. Quick Demo Checklist

Before submitting, verify:

``` text
[ ] python main.py runs successfully
[ ] Books scraper collects records
[ ] Quotes scraper collects records
[ ] Pagination works
[ ] source is present
[ ] source_url is present
[ ] Cleaning works
[ ] Validation works
[ ] Invalid records can be rejected
[ ] Deduplication works
[ ] Consolidation produces 10 columns
[ ] final_dataset.csv exists
[ ] summary_report.json exists
[ ] scraper.log exists
[ ] pytest -v passes
[ ] AI_USAGE.md is included
[ ] README.md explains the project
```

------------------------------------------------------------------------

# 22. Final Pipeline Summary

``` text
             WEB SOURCES
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
 Books to Scrape      Quotes to Scrape
        │                   │
        └─────────┬─────────┘
                  ↓
              SCRAPING
                  ↓
              CLEANING
                  ↓
             VALIDATION
                  ↓
          DUPLICATE DETECTION
                  ↓
            CONSOLIDATION
                  ↓
             FINAL DATASET
             /            \
            ↓              ↓
     final_dataset.csv   summary_report.json
                  +
             scraper.log
```



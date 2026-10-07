
# AI Usage & Development Disclosure

## 1. Purpose

AI assistance was used extensively during the development of this project.

AI was used for both **code generation and development assistance** across multiple parts of the assignment. The generated code was reviewed, integrated, executed, debugged, tested, and adapted to the actual requirements.

This document provides a transparent record of how AI contributed to the project and how the final implementation was verified.

---

# 2. AI Usage Summary

AI was used for:

- Understanding and breaking down the assignment requirements
- Planning the project architecture
- Generating initial and revised code
- Explaining Python and web-scraping concepts
- Designing scraper logic
- Designing cleaning functions
- Designing validation rules
- Designing duplicate detection
- Designing consolidation logic
- Adding logging and error handling
- Suggesting automated test cases
- Debugging implementation errors
- Improving README and project documentation

AI assistance was used across several project files, including:

```text
main.py

scrapers/
    books_scraper.py
    quotes_scraper.py

processing/
    cleaning.py
    validation.py
    deduplication.py
    consolidation.py

utils/
    http_client.py

tests/
    test_cleaning.py
    test_validation.py
    test_deduplication.py
    test_consolidation.py

README.md
AI_USAGE.md
```

The exact amount of AI-generated code may vary by file because the implementation was iteratively generated, reviewed, modified, and tested.

---

# 3. Important Disclosure

AI did generate code that was used in the project.

The development process was not:

```text
AI generates code → submit without checking
```

Instead, the process was:

```text
Assignment requirements
        ↓
AI-assisted design/code generation
        ↓
Review generated code
        ↓
Integrate into project
        ↓
Run the application
        ↓
Inspect actual results
        ↓
Identify errors/issues
        ↓
Modify and debug
        ↓
Run tests
        ↓
Verify final outputs
        ↓
Document the implementation
```

The final responsibility for understanding, integrating, testing, and verifying the implementation remained with the developer.

---

# 4. Step-by-Step AI-Assisted Development

## Step 1 — Understanding Requirements

AI was used to break the assignment into individual implementation requirements.

The main pipeline was identified as:

```text
Website A + Website B
        ↓
Scraping
        ↓
Cleaning
        ↓
Validation
        ↓
Deduplication
        ↓
Consolidation
        ↓
Final Dataset
```

This helped translate the assignment description into separate development tasks.

---

# 5. Step 2 — Project Structure

AI was used to suggest a modular structure.

The final structure was organized around responsibilities:

```text
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

### Reason for this structure

The project uses separate responsibilities instead of placing the entire pipeline in one file.

| File/Module | Responsibility |
|---|---|
| `books_scraper.py` | Books-specific scraping |
| `quotes_scraper.py` | Quotes-specific scraping |
| `cleaning.py` | Cleaning and normalization |
| `validation.py` | Data-quality validation |
| `deduplication.py` | Duplicate detection |
| `consolidation.py` | Common dataset schema |
| `http_client.py` | HTTP/session handling |
| `main.py` | Pipeline orchestration |
| `tests/` | Automated testing |

---

# 6. Step 3 — Books Scraper

## File

```text
scrapers/books_scraper.py
```

AI assisted with generating and explaining the initial scraper implementation.

The implementation extracts:

```text
title
price
availability
rating
source
source_url
```

The scraper uses BeautifulSoup to parse the HTML.

The book cards are located using:

```python
article.product_pod
```

Pagination is handled using the website's Next link:

```python
li.next > a
```

`urljoin()` is used to convert relative links into absolute URLs.

### Source metadata

The scraper includes:

```python
"source": "Books to Scrape"
```

and:

```python
"source_url": product_url
```

This is required for downstream validation and traceability.

---

# 7. Step 4 — Quotes Scraper

## File

```text
scrapers/quotes_scraper.py
```

AI assisted with generating and explaining the quote scraping implementation.

The scraper extracts:

```text
quote
author
tags
source
source_url
```

Quote blocks are identified using:

```python
div.quote
```

Quote text:

```python
span.text
```

Author:

```python
small.author
```

Tags:

```python
a.tag
```

Pagination is handled using the Next link.

The source metadata is:

```python
"source": "Quotes to Scrape"
```

---

# 8. Step 5 — Cleaning

## File

```text
processing/cleaning.py
```

AI assisted with creating reusable cleaning functions.

### `clean_text()`

Removes unnecessary whitespace.

Example:

```text
"   Hello World   "
        ↓
"Hello World"
```

### `clean_price()`

Converts formatted prices into numeric values.

Example:

```text
£51.77
   ↓
51.77
```

### `clean_rating()`

Converts rating words into numeric values.

Example:

```text
Three
  ↓
3
```

### `clean_url()`

Accepts HTTP/HTTPS URLs and rejects values that are not valid-looking web URLs.

---

# 9. Step 6 — Standardization

AI assisted with designing a common record structure so that both websites could pass through the same processing pipeline.

For example:

```text
Books:
title
```

and:

```text
Quotes:
quote
```

are mapped to:

```text
name_or_title
```

The standardized record contains fields such as:

```text
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

This allows records from different sources to be processed consistently.

---

# 10. Step 7 — Validation

## File

```text
processing/validation.py
```

AI assisted with implementing the validation rules required by the assignment.

The validation checks:

### Source

The source must be recognized:

```text
Books to Scrape
Quotes to Scrape
```

### Name/title

A usable `name_or_title` value must exist.

### URL

The source URL must:

- exist
- use HTTP or HTTPS
- contain a valid network location

### Price

When present, the price must:

- be numeric
- be finite
- not be negative

### Rating

When present, the rating must be one of:

```text
1, 2, 3, 4, 5
```

---

# 11. Step 8 — Real Debugging Example

An important validation problem occurred during development.

Initial execution produced:

```text
Valid records    : 0
Rejected records : 1100
```

The validation rejection reason was:

```text
unknown_source: 1100
```

Inspection of a rejected record showed:

```text
source: None
```

### Root cause

The scraper records did not contain the required `source` field.

### Fix

The source metadata was added to both scrapers:

```python
"source": "Books to Scrape"
```

and:

```python
"source": "Quotes to Scrape"
```

### Result after debugging

```text
Valid records    : 1100
Rejected records : 0
```

This demonstrates that the generated implementation was actually executed and debugged using real pipeline results.

---

# 12. Step 9 — Deduplication

## File

```text
processing/deduplication.py
```

AI assisted with designing a normalization-based duplicate detection strategy.

Text is normalized by:

```text
lowercase
+
remove extra whitespace
```

Example:

```text
"  Hello World  "
        ↓
"hello world"
```

A composite key is created from:

```text
source
name_or_title
author
```

If the same normalized key has already been seen, the record is classified as a duplicate.

### Actual result

```text
Records before deduplication : 1100
Duplicate records detected   : 1
Unique records remaining     : 1099
```

---

# 13. Step 10 — Consolidation

## File

```text
processing/consolidation.py
```

AI assisted with implementing the common final schema.

The final dataset contains 10 columns:

```text
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

The purpose is to make records from both websites consistent in one final dataset.

---

# 14. Step 11 — Error Handling

AI assisted with adding defensive exception handling.

The scrapers use:

```python
try:
    ...
except Exception as error:
    ...
```

This allows the project to:

- record request failures
- record parsing failures
- continue where appropriate
- provide debugging information

Errors are logged rather than silently ignored.

---

# 15. Step 12 — Logging

## File

```text
logs/scraper.log
```

AI assisted with setting up Python logging and identifying important events to record.

The log contains events such as:

```text
Scraping start
Page being scraped
Number of records found
Scraping completion
Parsing errors
Request failures
Validation results
Deduplication results
Consolidation results
Export results
Pipeline failures
```

Example:

```text
INFO - Starting Books scraping
INFO - Found 20 books on page 1
INFO - Books scraping completed. Records: 1000
```

---

# 16. Step 13 — Pipeline Orchestration

## File

```text
main.py
```

AI assisted with structuring the complete pipeline.

The final execution order is:

```text
[1/6] SCRAPING
        ↓
[2/6] CLEANING
        ↓
[3/6] VALIDATION
        ↓
[4/6] DEDUPLICATION
        ↓
[5/6] CONSOLIDATION
        ↓
[6/6] EXPORT
```

`main.py` coordinates all processing modules and creates the final outputs.

---

# 17. Step 14 — Output Generation

The project generates:

```text
output/final_dataset.csv
```

and:

```text
output/summary_report.json
```

The summary report contains:

```json
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

---

# 18. Step 15 — Testing

AI was used to help create and organize test cases.

Tests were created for:

```text
Cleaning
Validation
Deduplication
Consolidation
```

Examples include:

```text
test_clean_text
test_clean_price
test_clean_rating
test_clean_url
test_valid_record
test_unknown_source
test_missing_name
test_invalid_url
test_invalid_price
test_invalid_rating
test_duplicates_ignore_case_and_spaces
```

Tests can be executed with:

```bash
pytest -v
```

The test cases were reviewed against the actual implementation rather than being accepted without verification.

---

# 19. Step 16 — Documentation

AI assisted with structuring:

```text
README.md
AI_USAGE.md
```

The README documents the project architecture, workflow, setup, execution, outputs, testing, and interview explanation.

This document provides the AI usage disclosure.

---

# 20. Assignment Requirement Mapping

| Requirement | Implementation | AI Assistance |
|---|---|---|
| Multiple website sources | Two separate scraper classes | Yes |
| Pagination | Next-link processing | Yes |
| Separate source scrapers | `books_scraper.py`, `quotes_scraper.py` | Yes |
| Source metadata | `source` field | Yes |
| Original source URL | `source_url` field | Yes |
| Common schema | `consolidation.py` | Yes |
| Text cleaning | `clean_text()` | Yes |
| Numeric price | `clean_price()` | Yes |
| Standardized rating | `clean_rating()` | Yes |
| URL handling | `clean_url()` + validation | Yes |
| Missing values | Cleaning/standardization | Yes |
| Validation | `validation.py` | Yes |
| Duplicate detection | `deduplication.py` | Yes |
| Normalized comparison | lowercase + whitespace normalization | Yes |
| Error handling | `try/except` | Yes |
| Logging | Python logging | Yes |
| Final CSV | `final_dataset.csv` | Yes |
| Summary report | `summary_report.json` | Yes |
| Automated tests | `tests/` | Yes |
| Documentation | `README.md`, `AI_USAGE.md` | Yes |

---

# 21. What Was Personally Verified

Even though AI generated code used in multiple files, the implementation was verified by actually running the project.

Verification included:

1. Running the Books scraper.
2. Running the Quotes scraper.
3. Confirming pagination worked.
4. Confirming 1,000 book records were collected.
5. Confirming 100 quote records were collected.
6. Inspecting raw records.
7. Running the cleaning stage.
8. Running validation.
9. Investigating the `unknown_source` failure.
10. Fixing missing source metadata.
11. Re-running validation.
12. Running duplicate detection.
13. Confirming one duplicate was detected.
14. Confirming 1,099 unique records remained.
15. Confirming the final dataset contains 10 columns.
16. Verifying the CSV output.
17. Verifying the JSON summary report.
18. Verifying the execution log.
19. Running the automated tests.
20. Reviewing the project documentation.

---

# 22. What I Learned From the AI-Assisted Development

The project was also used as a learning process.

Key concepts understood include:

- Python classes
- HTTP requests
- sessions
- HTML parsing
- CSS selectors
- pagination
- URL handling
- data cleaning
- validation
- normalization
- duplicate detection
- Pandas DataFrames
- CSV/JSON output
- exception handling
- Python logging
- automated testing
- modular project architecture

The most important learning was understanding the complete data flow:

```text
HTML
 ↓
Raw Records
 ↓
Standardized Records
 ↓
Cleaned Records
 ↓
Validated Records
 ↓
Unique Records
 ↓
Consolidated Dataset
 ↓
CSV + JSON + Logs
```

---

# 23. How I Would Explain AI Usage in an Interview

If asked:

### "Did you use AI to write the code?"

A transparent answer is:

> "Yes. I used AI extensively during development, including generating code for several project files. I did not treat the generated code as automatically correct. I integrated it into the project, ran it against the target websites, inspected the output, debugged errors, modified the implementation where necessary, and verified the final dataset and tests."

### "Which parts did AI help with?"

> "AI assisted with the scrapers, cleaning functions, validation, deduplication, consolidation, logging, pipeline orchestration, test cases, and documentation."

### "Can you explain the code?"

> "Yes. I understand the role of each module and the data flow through scraping, cleaning, validation, deduplication, consolidation, and export. I also debugged an actual validation issue where all records were initially rejected because the source metadata was missing."

### "Did you verify the AI-generated code?"

> "Yes. I ran the complete pipeline, checked the record counts, investigated validation failures, verified the final CSV and JSON outputs, checked logs, and ran the automated tests."

---

# 24. AI Usage Principles

The development process followed:

```text
AI-generated suggestion/code
            ↓
Understand
            ↓
Review
            ↓
Integrate
            ↓
Execute
            ↓
Debug
            ↓
Test
            ↓
Verify
```

AI-generated code was not assumed to be correct simply because it was generated by AI.

The implementation was checked against the assignment requirements and actual execution results.

---

# 25. Final Verified Result

The current successful execution produced:

```text
Books records collected : 1000
Quotes records collected: 100
Total records collected : 1100

Records after cleaning  : 1100
Records rejected        : 0
Validation errors       : {}

Duplicates detected     : 1
Final records           : 1099
Final columns           : 10

Execution time          : 24.51 seconds
```

The final pipeline successfully produces:

```text
output/final_dataset.csv
output/summary_report.json
logs/scraper.log
```

---

# 26. Final Disclosure

AI was a significant part of the development process and was used to generate code as well as provide explanations, debugging assistance, testing suggestions, and documentation support.

The final project was executed, reviewed, debugged, tested, and verified against the assignment requirements.

The developer is responsible for understanding and explaining the submitted implementation.

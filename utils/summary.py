import json
from pathlib import Path

def write_summary(stats: dict, path: Path):
    path.parent.mkdir(exist_ok=True)               # create output/ if missing
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)

stats = {
    "collected_per_source": {"Books to Scrape": 1000, "Quotes to Scrape": 100},
    "rejected_by_reason": {"invalid_url": 0, "missing_name": 0},
    "duplicates_detected": 0,
    "final_record_count": 1100,
    "duration_seconds": 612.4,
}
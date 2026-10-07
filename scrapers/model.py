from dataclasses import dataclass
from typing import Optional


@dataclass
class ScrapedRecord:
    source: str
    source_url: str
    name_or_title: str
    category: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[int] = None
    author: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    scraped_at: Optional[str] = None
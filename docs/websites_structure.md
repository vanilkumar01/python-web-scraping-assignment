# Website Structure Analysis

## 1. Books to Scrape

Base URL:
https://books.toscrape.com/

| Field | HTML Element / Selector |
|---|---|
| Book container | `article.product_pod` |
| Title | `h3 a` |
| Price | `p.price_color` |
| Availability | `p.instock.availability` |
| Rating | `p.star-rating` |
| Product URL | `h3 a[href]` |
| Next page | `li.next a` |

### Pagination
The scraper finds the `Next` link and follows it until no Next link exists.

---

## 2. Quotes to Scrape

Base URL:
https://quotes.toscrape.com/

| Field | HTML Element / Selector |
|---|---|
| Quote container | `div.quote` |
| Quote text | `span.text` |
| Author | `small.author` |
| Tags | `a.tag` |
| Next page | `li.next a` |

### Pagination
The scraper finds the `Next` link and follows it until no Next link exists.
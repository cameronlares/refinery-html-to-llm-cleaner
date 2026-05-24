#!/usr/bin/env python3
"""Generate README.md with CDN-hosted store images for Apify Store."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "store"
README = ROOT / "README.md"
MAX_README_BYTES = 250_000
CDN_BASE = "https://cdn.jsdelivr.net/gh/LareLabs/refinery-html-to-llm-cleaner@main/assets/store"


def image_markdown(filename: str, alt: str) -> str:
    return f"![{alt}]({CDN_BASE}/{filename})"


def main() -> int:
    images = {
        "flow": ("flow-pipeline.webp", "Refinery pipeline: raw HTML to clean JSON for RAG"),
        "before_after": (
            "before-after-tokens.webp",
            "Token reduction: bloated HTML vs clean text after Refinery",
        ),
        "social": (
            "social-feed-html.webp",
            "Social and feed HTML: mentions and hashtags preserved as clean text",
        ),
        "console": (
            "console-output-demo.webp",
            "Apify dataset output: clean text, word count, and timing",
        ),
        "bulk": (
            "bulk-urls-mode.webp",
            "Bulk URL mode: many pages in, dataset rows out",
        ),
        "stack": (
            "stack-integrations.webp",
            "Refinery in your stack: crawler, clean, vector DB, LLM",
        ),
    }

    embedded = {}
    for key, (filename, alt) in images.items():
        p = ASSETS / filename
        if not p.is_file():
            print(f"Missing {p}", file=sys.stderr)
            return 1
        embedded[key] = image_markdown(filename, alt)
        print(f"  {filename}: {p.stat().st_size:,} bytes")

    body = f"""# Refinery — Clean HTML for RAG & LLM pipelines

**Strip scripts, nav, and layout junk from HTML before you chunk and embed.**  
Pay **$0.002/page** · **~2–8ms** clean step (after your crawler fetches the page).

[![Price](https://img.shields.io/badge/price-%240.002%2Fpage-blue)](https://apify.com/larelabs/refinery-html-to-llm-cleaner/pricing)
[![Speed](https://img.shields.io/badge/speed-2--8ms%2Fpage-brightgreen)]()

{embedded["flow"]}

---

## Before vs after (why RAG teams use this)

{embedded["before_after"]}

Same page class as a news homepage — **up to ~97% fewer estimated tokens** on heavy DOM (your mileage varies).

---

## Social posts & feed HTML

Scraped timelines and comment threads ship **messy DOM** — scripts, sidebars, and nested widgets. Refinery keeps **post body text** and normalizes **@mentions** / **#topics** for chunking without paying for chrome.

{embedded["social"]}

Paste `raw_payload` from your scraper, or pass URLs if you already fetch HTML elsewhere.

---

## What you see in Apify Console

Run **Try actor** with the prefilled `example.com` URL — output lands in the dataset like this:

{embedded["console"]}

---

## Bulk URL mode

Send **many URLs in one run** — each row in the dataset gets `text`, `word_count`, and timing. Ideal after a crawl batch or sitemap pass.

{embedded["bulk"]}

```json
{{
  "urls": [
    "https://example.com",
    "https://www.bbc.com/news",
    "https://httpbin.org/html"
  ],
  "removeScripts": true,
  "removeStyles": true,
  "includeMetadata": true
}}
```

---

## Who this is for

- **RAG / agent builders** paying per token on bloated page HTML  
- **Scrape pipelines** that already fetch HTML (Firecrawl, Crawl4AI, Playwright, Apify crawlers)  
- **Teams** who want deterministic text + `word_count` without BeautifulSoup on every worker  

**Refinery is not a crawler.** It cleans HTML you already have.

```
Your crawler → raw HTML → Refinery → clean text → chunk → embed → LLM
```

---

## Try it now (3 demos)

**Demo 1** is prefilled in Console. Paste **Demo 2** or **Demo 3** to see different modes.

### Demo 1 — Quick URL

```json
{{
  "urls": ["https://example.com"],
  "removeScripts": true,
  "removeStyles": true,
  "includeMetadata": true
}}
```

### Demo 2 — Bloated news homepage

```json
{{
  "urls": ["https://www.bbc.com/news"],
  "removeScripts": true,
  "removeStyles": true,
  "includeMetadata": true
}}
```

### Demo 3 — Paste HTML (middleware)

```json
{{
  "raw_payload": "<html><head><script>gtag('event')</script></head><body><nav>Home · Pricing</nav><article><h1>Update</h1><p>Clean before embedding.</p></article></body></html>",
  "removeScripts": true,
  "removeStyles": true,
  "includeMetadata": true
}}
```

---

## What you get back

```json
{{
  "text": "Example Product Page\\nEnterprise AI Infrastructure...",
  "language": "en",
  "word_count": 12,
  "content_type": "web",
  "processing_time_ms": 19.29,
  "success": true
}}
```

| Field | Use it for |
|-------|------------|
| `text` | Chunking, embeddings, LLM context |
| `word_count` | Cost estimates |
| `processing_time_ms` | Latency monitoring |

---

## Where Refinery fits

{embedded["stack"]}

| You already use… | Refinery's job |
|------------------|----------------|
| Firecrawl, Crawl4AI | Clean their HTML output |
| Apify Web Scraper | Clean `html` field |
| Self-hosted BeautifulSoup | Faster hot path (~281× in our benchmarks) |

---

## Pricing

| Event | Cost |
|-------|------|
| HTML extraction | **$0.002** / page |
| ~1,000 pages | **~$2.05** |

---

## Integrate

### JavaScript

```javascript
import {{ ApifyClient }} from 'apify-client';
const client = new ApifyClient({{ token: process.env.APIFY_TOKEN }});
const run = await client.actor('larelabs/refinery-html-to-llm-cleaner').call({{
  urls: ['https://example.com'],
}});
const {{ items }} = await client.dataset(run.defaultDatasetId).listItems();
console.log(items[0].text, items[0].word_count);
```

### Python

```python
from apify_client import ApifyClient
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("larelabs/refinery-html-to-llm-cleaner").call(
    run_input={{"urls": ["https://example.com"]}}
)
print(next(client.dataset(run["defaultDatasetId"]).iterate_items()))
```

---

## FAQ

**Replacement for Firecrawl?** No — fetch with Firecrawl, **clean with Refinery**.

**SPAs?** Use a browser crawler first; Refinery cleans the HTML you pass in.

**Social / X HTML?** Pass saved page HTML via `raw_payload` — Refinery does not log in or scrape feeds for you.

---

## Support

**LareLabs** · [Store listing](https://apify.com/larelabs/refinery-html-to-llm-cleaner) · [Console](https://console.apify.com/organization/vTZ0XDFG4cZCNAdQl/actors/jOcx8jK2FdhZhoKrE)

---

*Rust core · Apify Actor · Update `assets/store/*.webp`, push to GitHub, then run `python scripts/embed_store_readme.py` and `python scripts/sync_store_readme.py`.*
"""

    README.write_text(body, encoding="utf-8")
    size = README.stat().st_size
    print(f"\nWrote {README} ({size:,} bytes)")
    if size > MAX_README_BYTES:
        print(f"WARNING: README exceeds {MAX_README_BYTES:,} bytes — compress WebP assets.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Refinery — Clean HTML for RAG & LLM pipelines

**Strip scripts, nav, and layout junk from HTML before you chunk and embed.**  
Pay **$0.002/page** · **~2–8ms** clean step (after your crawler fetches the page).

[![Price](https://img.shields.io/badge/price-%240.002%2Fpage-blue)](https://apify.com/larelabs/refinery-html-to-llm-cleaner/pricing)
[![Speed](https://img.shields.io/badge/speed-2--8ms%2Fpage-brightgreen)]()

---

## Who this is for

- **RAG / agent builders** paying per token on bloated page HTML  
- **Scrape pipelines** that already fetch HTML (Firecrawl, Crawl4AI, Playwright, Apify crawlers) and need a **cheap clean step**  
- **Teams** who want deterministic text + `word_count` without running BeautifulSoup on every worker  

**Refinery is not a crawler.** It does not discover URLs or render SPAs. It **cleans HTML you already have**.

```
Your crawler → raw HTML → Refinery → clean text → chunk → embed → LLM
```

---

## Try it now (3 demos)

In Apify Console, open **Try actor** — **Demo 1** is prefilled. Or paste **Demo 2** / **Demo 3** below.

### Demo 1 — Quick URL (fastest)

Good first run: small page, proves fetch + clean works.

```json
{
  "urls": ["https://example.com"],
  "removeScripts": true,
  "removeStyles": true,
  "includeMetadata": true
}
```

**You should see:** `success: true`, short `text`, `word_count`, `processing_time_ms` (~20ms including fetch).

---

### Demo 2 — Bloated news homepage (token savings)

Shows why RAG teams care — huge DOM → small text.

```json
{
  "urls": ["https://www.bbc.com/news"],
  "removeScripts": true,
  "removeStyles": true,
  "includeMetadata": true
}
```

**Typical result (varies by page):**

| | Raw HTML | After Refinery |
|--|----------|----------------|
| Payload | ~330 KB | ~10 KB text |
| Est. tokens (chars ÷ 4) | ~82,000 | ~2,500 |
| Words returned | — | ~1,600 |

---

### Demo 3 — Paste HTML (middleware mode)

Use when your pipeline already has HTML strings (no fetch).

```json
{
  "raw_payload": "<html><head><script>gtag('event','page_view')</script><style>.nav,.footer,.promo{display:block}</style></head><body><nav>Home · Pricing · Docs · Login</nav><article><h1>Quarterly update</h1><p>We reduced embedding cost by cleaning HTML before chunking.</p></article><footer>© 2026 · 40 footer links · consent banner</footer><script>window.__NEXT_DATA__={}</script></body></html>",
  "removeScripts": true,
  "removeStyles": true,
  "includeMetadata": true
}
```

**You should see:** only the article heading + paragraph — no nav, scripts, or footer noise.

---

## What you get back

Each run writes **one dataset item** per page:

```json
{
  "text": "Quarterly update\nWe reduced embedding cost by cleaning HTML before chunking.",
  "language": "en",
  "word_count": 12,
  "content_type": "web",
  "processing_time_ms": 4.2,
  "success": true
}
```

| Field | Use it for |
|-------|------------|
| `text` | Chunking, embeddings, LLM context |
| `word_count` | Cost estimates, quotas |
| `processing_time_ms` | Latency monitoring |
| `language` | Routing / locale |

Optional: `extractMentions` / `extractHashtags` for social HTML.

---

## Where Refinery fits

| You already use… | Refinery's job |
|------------------|----------------|
| Firecrawl, Crawl4AI, custom fetch | Clean their HTML output |
| Apify Web Scraper / Playwright | Second step on `html` field |
| `httpx` / `requests` + save HTML | Batch `urls` or paste `raw_payload` |
| Self-hosted BeautifulSoup | Replace hot path; **~281× faster** on extraction in our benchmarks |

---

## Pricing

| Event | Cost |
|-------|------|
| Actor start | $0.00005 |
| HTML extraction | **$0.002** |
| Result write | $0.00001 |

**~$2.05 per 1,000 pages** — often cheaper than sending full DOM text to GPT-4 class models.

---

## Integrate

### JavaScript

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('larelabs/refinery-html-to-llm-cleaner').call({
  urls: ['https://example.com'],
  removeScripts: true,
  removeStyles: true,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items[0].text, items[0].word_count);
```

### Python

```python
from apify_client import ApifyClient
import os

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("larelabs/refinery-html-to-llm-cleaner").call(
    run_input={
        "urls": ["https://example.com"],
        "removeScripts": True,
        "removeStyles": True,
    }
)
item = next(client.dataset(run["defaultDatasetId"]).iterate_items())
print(item["text"], item["word_count"])
```

### cURL

```bash
curl -X POST "https://api.apify.com/v2/acts/larelabs~refinery-html-to-llm-cleaner/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://example.com"],"removeScripts":true,"removeStyles":true}'
```

---

## Input options

| Field | Description |
|-------|-------------|
| `urls` | Fetch + clean (one or many URLs) |
| `raw_payload` | Clean HTML you already fetched |
| `removeScripts` | Default `true` — strips JS, trackers |
| `removeStyles` | Default `true` — strips CSS |
| `includeMetadata` | Default `true` — word count, language, timing |
| `extractMentions` / `extractHashtags` | Optional, for social HTML |

**Limit:** 10 MB HTML per request.

---

## FAQ

**Is this a replacement for Firecrawl?**  
No. Firecrawl fetches; Refinery **cleans**. Use both.

**Why Apify instead of BeautifulSoup on my server?**  
No parser ops to maintain, scales on Apify, predictable **$0.002/page**, Rust core for speed.

**Will it work on every site?**  
Heavy SPAs may need a browser crawler first; Refinery cleans the HTML you give it. Marketing pages and articles see the biggest token wins.

**How do I bulk process?**  
Pass multiple URLs in `urls` or call the Actor in parallel from your pipeline.

---

## Support

**LareLabs** · [Apify Store listing](https://apify.com/larelabs/refinery-html-to-llm-cleaner) · Actor ID `jOcx8jK2FdhZhoKrE`

Issues via [Apify Console](https://console.apify.com/organization/vTZ0XDFG4cZCNAdQl/actors/jOcx8jK2FdhZhoKrE).

---

*Rust extraction core · Python Apify Actor · Production on Apify.*

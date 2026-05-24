# Apify deploy — Lare Labs org only

**Do not deploy to Cameron's personal Apify account.** Wrong account = duplicate actors, failed builds, hours of debugging.

## Verify before every `apify push`

```bash
apify info
```

| Must see | Must NOT see |
|----------|----------------|
| `larelabs` | `cameronlares` |
| `vTZ0XDFG4cZCNAdQl` | `v83urlldkZpIfuYFp` |

- **Lare Labs org:** `larelabs` / `vTZ0XDFG4cZCNAdQl`
- **Personal (wrong):** `cameronlares` / `v83urlldkZpIfuYFp`

If wrong:

```bash
apify logout
apify login --token "$APIFY_LARELABS_TOKEN"   # org token from secure store, not personal
apify info   # confirm again
```

## Canonical actor (only one)

| Field | Value |
|-------|--------|
| Store URL | https://apify.com/larelabs/refinery-html-to-llm-cleaner |
| Actor ID | `jOcx8jK2FdhZhoKrE` |
| Console | https://console.apify.com/organization/vTZ0XDFG4cZCNAdQl/actors/jOcx8jK2FdhZhoKrE |
| Namespace | `larelabs/` (not `cameronlares/`) |

## Deploy from this directory only

```bash
cd /root/ACTIVE_PROJECTS/refinery/refinery-rust
apify actors push --force
```

Source of truth: this repo path. Not `ARCHIVE/`, not personal Apify, not a second actor name.

## Version tags (avoid “three latest” in Console)

In `.actor/actor.json` keep **one** line only:

```json
"version": "1.1",
"buildTag": "latest"
```

Do **not** create `1.2` unless you mean to. After a mistaken `1.2` push, clear its tag in Console or API:

- `1.1` → `buildTag: latest` (and point global `latest` at the last green **1.1.x** build)
- `1.0` / `1.2` → `buildTag: null`

**Current (fixed):** global `latest` = build **1.1.39**; only version **1.1** shows `(latest)`.

## Store README images

- Apify **does not render** GitHub `raw.githubusercontent.com` image URLs in the Actor README.
- Use **embedded WebP** via small assets (`assets/store/*.webp`) — keep total README **under ~250KB** (never multi‑MB base64 like the old `3620cb7` commit).
- Prefer **Console output** screenshots over fake social posts for trust.
- To refresh images: compress to WebP (~20–80KB each), re-run embed script, rebuild.
- **Do not** use `*.md` in `.apifyignore` — it can exclude `README.md` and leave the Console stuck on an old Store README.

## GitHub

Apify builds from **CLI push** here unless you explicitly wire GitHub → Apify in the **Lare Labs** org console. Pushes to GitHub do not update the Store listing unless that integration is on the org actor.

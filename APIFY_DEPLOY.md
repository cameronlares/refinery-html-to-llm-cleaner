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

## GitHub

Apify builds from **CLI push** here unless you explicitly wire GitHub → Apify in the **Lare Labs** org console. Pushes to GitHub do not update the Store listing unless that integration is on the org actor.

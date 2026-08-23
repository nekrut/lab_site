# anLab — Nekrutenko Lab website

Single-page static site for the [Nekrutenko Lab](https://nekrut.github.io/lab_site/) at Penn State — the birthplace of [Galaxy](https://galaxyproject.org). Deployed via GitHub Pages from `master:/docs`, rebuilt automatically every month.

**Live site:** https://nekrut.github.io/lab_site/

## How it works

```
nekrut/CV (private)          NIH iCite API           KUI dashboard (Looker Studio)
  vitae.md                     citations               usegalaxy.* usage numbers
  people, grants, PMIDs           │                        │
        │                        │                        │  scripts/fetch_kui_stats.py
        └────────────┬───────────┘                        │  (playwright scrape)
                     ▼                                    ▼
            scripts/build_site.py  ◄──── scripts/data/{icite_cache,kui_stats}.json
                     │                    graph_data/ppl.json (github handles,
                     ▼                    affinity colors, countries)
        docs/index.html + 404.html + logos/ + flags/
                     │
                     ▼
              GitHub Pages (master:/docs)
```

The **CV is the curated source of truth**: team members and tenure come from the Research Personnel / Graduate / Undergraduate tables in `vitae.md`; publications come from its `PMID:` links (titles, journals, and citation counts are then pulled live from [NIH iCite](https://icite.od.nih.gov)); active grants are hand-mirrored from the CV into the template. `graph_data/ppl.json` supplements GitHub handles, biological⇄computational affinity colors, and countries.

## Monthly automation

`.github/workflows/update-site.yml` runs on the 1st of every month (and via *Run workflow*):

1. Checks out this repo + the private `nekrut/CV` repo
2. `fetch_kui_stats.py` — refreshes the four usegalaxy.\* stats (keeps old values if the scrape fails)
3. `build_site.py` — regenerates `docs/` with fresh iCite citations
4. `check_links.py` — verifies every external link on the built page
5. `discover_pubs.py` — searches PubMed for the PI's papers missing from the CV
6. Commits `docs/` + `scripts/data/` if anything changed; dead links / new-PMID candidates / scrape failures are filed into a `site-maintenance` issue

**Required secret:** `CV_REPO_TOKEN` — a fine-grained PAT with *Contents: Read* on `nekrut/CV` (repo → Settings → Secrets and variables → Actions).

## Making changes

| Change | Where |
|---|---|
| Team member joins/leaves, dates, roles | edit tables in `nekrut/CV` `vitae.md` (name cell may be a `[Name](github url)` link) |
| One-off people corrections | guarded patch block in `scripts/build_site.py` (search `corrections`) |
| New publication | add the PMID to `vitae.md`; citations fetch automatically |
| Grants | `GRANTS` array in `scripts/build_site.py` (mirror the CV) |
| Products / collaborators | `PRODUCTS` array / `collabs` list in `scripts/build_site.py` |
| Logos, flags | `assets/logos/`, `assets/flags/` (synced into `docs/` at build) |
| Design / layout / copy | the `E` template string in `scripts/build_site.py` |

Never edit `docs/index.html` directly — the monthly build overwrites it.

### Local build & preview

```bash
python3 scripts/build_site.py          # regenerates docs/ (uses ~/git/CV/vitae.md)
python3 -m http.server -d docs 8741    # http://localhost:8741
python3 scripts/check_links.py         # optional: link check
```

`CV_MD=/path/to/vitae.md` overrides the CV location; `PREVIEWS=1` also emits the design variants.

## Repository layout

```
docs/                     deployed site (generated — do not hand-edit)
scripts/build_site.py     generator: CV + iCite + KUI → docs/
scripts/fetch_kui_stats.py  Looker Studio scraper (playwright)
scripts/check_links.py    external link checker
scripts/discover_pubs.py  PubMed vs CV diff → issue candidates
scripts/data/             icite_cache.json, kui_stats.json
assets/                   logos + twemoji country flags (source of docs/ copies)
graph_data/ppl.json       legacy people metadata still merged at build
design_previews/          design exploration: variants A–E + generator
.github/workflows/        monthly update workflow
```

## Design notes

The deployed design ("E · Hybrid") combines a bold industrial layout with Inter Tight display type and Spline Sans Mono labels — paper background `#f4f2ed`, accent `#ff4d00` (text-safe `#d63a00`). Alternate explorations (terminal, industrial, quiet, Swiss) live in `design_previews/`.

The Orbit and Foundry logos in `assets/logos/` are lab-drawn proposals in the classic Galaxy logo style, PR'd upstream: [galaxyproject/loom#442](https://github.com/galaxyproject/loom/pull/442), [galaxyproject/foundry#471](https://github.com/galaxyproject/foundry/pull/471). Country flags are [Twemoji](https://github.com/jdecked/twemoji) (CC-BY 4.0).

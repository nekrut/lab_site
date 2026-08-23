#!/usr/bin/env python3
"""Scrape the four aggregate numbers from the usegalaxy KUI Looker Studio dashboard.

Renders the dashboard's "Aggregate data" page headlessly (Looker Studio is a JS
app; there is no data API for anonymous viewers) and extracts:
  Total registered users / Total jobs / Total datasets / Total workflows

On any failure the existing scripts/data/kui_stats.json is left untouched and
the script exits 0 with a warning, so a flaky scrape never breaks the build.
Exit code 2 signals "stats are stale" to the workflow (used for the issue report).
"""
import json, os, re, sys, datetime

DASH = ("https://lookerstudio.google.com/reporting/"
        "8cfee054-2ddd-4711-af5a-a7a8d62076bb/page/p_kmr3zbo6ad")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "kui_stats.json")
LABELS = {
    "Total registered users": "users",
    "Total jobs": "jobs",
    "Total datasets": "datasets",
    "Total workflows": "workflows",
}


def scrape():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        page.goto(DASH, wait_until="networkidle", timeout=120_000)
        page.wait_for_timeout(8_000)  # charts render after network idle
        text = page.inner_text("body")
        browser.close()
    # numbers follow their labels in the flattened text, e.g. "Total jobs\n208.9M"
    found = {}
    for label, key in LABELS.items():
        m = re.search(re.escape(label) + r"\s*\n\s*([\d.,]+[KMB]?)", text)
        if m:
            found[key] = m.group(1)
    return found


def main():
    try:
        found = scrape()
    except Exception as e:  # noqa: BLE001 - any scrape failure keeps old stats
        print(f"WARN: KUI scrape failed ({e}); keeping previous stats", file=sys.stderr)
        sys.exit(2)
    if set(found) != set(LABELS.values()):
        print(f"WARN: KUI scrape incomplete ({found}); keeping previous stats", file=sys.stderr)
        sys.exit(2)
    found["as_of"] = datetime.date.today().strftime("%Y-%m")
    with open(OUT + ".tmp", "w") as fh:
        json.dump(found, fh, indent=1)
    os.replace(OUT + ".tmp", OUT)
    print("KUI stats updated:", found)


if __name__ == "__main__":
    main()

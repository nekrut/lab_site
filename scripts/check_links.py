#!/usr/bin/env python3
"""Check every external link in the generated site; print failures.

Writes a markdown report to stdout; exits 1 if any link is dead so the
workflow can open/refresh a maintenance issue (build itself is unaffected).
"""
import re, sys, urllib.request, os

HTML = os.environ.get("SITE_HTML", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "index.html"))
UA = {"User-Agent": "Mozilla/5.0 (lab-site link check)"}
SKIP = ("fonts.googleapis.com", "fonts.gstatic.com", "google.com/maps",
        "pubmed.ncbi.nlm.nih.gov", "linkedin.com", "ncbi.nlm.nih.gov")


def main():
    html = open(HTML).read()
    urls = sorted({u.rstrip('"\\').rstrip('/') or u for u in re.findall(r'https?://[^"\'\s<>`]+', html)
                   if not any(sk in u for sk in SKIP)})
    dead = []
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=UA, method="GET")
            with urllib.request.urlopen(req, timeout=25) as r:
                if r.status >= 400:
                    dead.append((u, r.status))
        except Exception as e:  # noqa: BLE001
            dead.append((u, str(e)[:80]))
    print(f"Checked {len(urls)} external links.")
    if dead:
        print("\n### Dead links\n")
        for u, why in dead:
            print(f"- {u} — {why}")
        sys.exit(1)
    print("All links OK.")


if __name__ == "__main__":
    main()

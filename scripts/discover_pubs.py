#!/usr/bin/env python3
"""Find PubMed papers by the PI that are not yet in the CV.

The CV (vitae.md) is the curated source of truth for the site's publication
list; this script only *discovers* candidates so a human can vet them.
Prints a markdown list; exits 1 when there are new candidates so the workflow
can open/refresh an issue.
"""
import json, os, re, sys, urllib.request

CV_MD = os.environ.get("CV_MD", "/home/anton/git/CV/vitae.md")
ESEARCH = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
           "?db=pubmed&term=nekrutenko+a%5Bau%5D&retmax=300&retmode=json")
ESUMMARY = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            "?db=pubmed&retmode=json&id=")


def main():
    cv_pmids = set(re.findall(r"PMID: (\d+)", open(CV_MD).read()))
    with urllib.request.urlopen(ESEARCH, timeout=60) as r:
        pubmed = set(json.load(r)["esearchresult"]["idlist"])
    new = sorted(pubmed - cv_pmids, key=int, reverse=True)
    if not new:
        print("No new PubMed records; CV is up to date.")
        return
    with urllib.request.urlopen(ESUMMARY + ",".join(new[:50]), timeout=60) as r:
        docs = json.load(r)["result"]
    print(f"### {len(new)} PubMed record(s) not in the CV\n")
    print("Vet these and add the real ones to `vitae.md` in nekrut/CV "
          "(the site rebuilds from the CV):\n")
    for pmid in new[:50]:
        d = docs.get(pmid, {})
        print(f"- [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/) — "
              f"{d.get('title', '?')} *{d.get('source', '')}* {d.get('pubdate', '')}")
    sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json, csv, html

OUT = '/home/anton/git/lab_site/design_previews'

import re, urllib.request, os, unicodedata
CV = open('/home/anton/git/CV/vitae.md').read()
CUR_YEAR = 2026

# ---- publications: PMIDs from CV, metadata + citations live from NIH iCite ----
pmids = []
for m in re.finditer(r'PMID: (\d+)', CV):
    if m.group(1) not in pmids: pmids.append(m.group(1))
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icite_cache.json')
try:
    icite = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
except ValueError:
    icite = {}
missing = [p for p in pmids if p not in icite]
for i in range(0, len(missing), 100):
    url = 'https://icite.od.nih.gov/api/pubs?pmids=' + ','.join(missing[i:i+100])
    with urllib.request.urlopen(url, timeout=60) as r:
        for d in json.load(r).get('data', []):
            icite[str(d['pmid'])] = {'title': d.get('title'), 'journal': d.get('journal'),
                                     'year': d.get('year'), 'cites': d.get('citation_count') or 0}
    json.dump(icite, open(CACHE + '.tmp', 'w')); os.replace(CACHE + '.tmp', CACHE)
pubs = [{'pmid': p, 'url': f'https://pubmed.ncbi.nlm.nih.gov/{p}/', **icite[p]} for p in pmids if p in icite]
# doi-only entries in CV (no PMID yet)
pubs.append({'pmid': '', 'url': 'https://doi.org/10.64898/2026.01.29.702612',
             'title': 'BUSTED-PH: Isolating the genomic signatures of convergent phenotypes.',
             'journal': 'bioRxiv', 'year': 2026, 'cites': 0})
for p in pubs: p['Year'] = p['year']; p['cites'] = int(p['cites'])
pubs.sort(key=lambda p: (-p['year'], -p['cites']))

# ---- people: CV tables (authoritative for names/years/roles) merged with ppl.json (github/affinity/country) ----
ppl = json.load(open('/home/anton/git/lab_site/graph_data/ppl.json'))
old_people = list(ppl['datasets'].values())[0]
normcc = lambda c: {'UK': 'GB'}.get((c or '').strip()[:2].upper(), (c or '').strip()[:2].upper())
skey = lambda n: re.sub(r'[^a-z]', '', unicodedata.normalize('NFD', n.lower()))
oldmap = {}
for p in old_people:
    clean = re.sub(r'\s*\([^)]*\)\s*$', '', p['name'])
    oldmap[skey(clean.split()[-1])] = p

def cv_table(section, role_col=None, role_fmt=None):
    rows = []
    m = re.search(r'### ' + section + r'(.*?)(?=\n#|\Z)', CV, re.S)
    for line in m.group(1).strip().splitlines():
        if not line.startswith('|') or set(line.replace('|','').strip()) <= set('- '): continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if cells[0] in ('Name',) or not cells[0]: continue
        gh = ''
        lm = re.match(r'\[([^\]]+)\]\(([^)]+)\)', cells[0])
        if lm:
            cells[0] = lm.group(1)
            if 'github.com/' in lm.group(2): gh = '@' + lm.group(2).rstrip('/').split('/')[-1]
        ym = next((c for c in cells if re.match(r'^\d{4}[–-]', c)), None)
        if not ym: continue
        y = re.match(r'^(\d{4})[–-](\d{4})?', ym)
        role = cells[role_col] if role_col is not None and role_col < len(cells) else ''
        if role_fmt: role = role_fmt(cells)
        rows.append({'name': cells[0], 'start': int(y.group(1)),
                     'end': int(y.group(2)) if y.group(2) else None, 'role': role, 'gh': gh})
    return rows

cvp = (cv_table('Research Personnel', role_col=3)
     + cv_table('Graduate Students', role_fmt=lambda c: f"{c[1]} student, {c[2]}")
     + cv_table('Undergraduate Students', role_fmt=lambda c: f"Undergraduate, {c[1]}"))
merged = {}
for r in cvp:
    surname = r['name'].split()[-1]
    k = skey(surname)
    if k in merged:  # e.g. Blankenberg grad + postdoc -> merge span
        m0 = merged[k]
        m0['start'] = min(m0['start'], r['start'])
        m0['end'] = None if (m0['end'] is None or r['end'] is None) else max(m0['end'], r['end'])
        m0['role'] += ' · ' + r['role']
        continue
    old = oldmap.get(k) or next((v for kk, v in oldmap.items() if kk and (kk in k or k in kk)), None)
    merged[k] = {'name': r['name'], 'start': r['start'], 'end': r['end'], 'role': r['role'],
                 'github': (old or {}).get('github') or r.get('gh') or '',
                 'country': normcc((old or {}).get('country')) if old else '',
                 'aff': (old or {}).get('affinity') or 'C',
                 'pubmed': (old or {}).get('pubmed') or
                     f"https://www.ncbi.nlm.nih.gov/pubmed/?term=nekrutenko+AND+{surname.lower()}"}
# PI + anyone in ppl.json the CV tables omit
anton = oldmap.get('nekrutenko', {})
merged['nekrutenko'] = {'name': 'Anton Nekrutenko', 'start': 2003, 'end': None,
    'role': 'PI · Huck Chair in Genomics · Professor of Biochemistry and Molecular Biology',
    'github': anton.get('github') or '@nekrut', 'country': normcc(anton.get('country') or 'UA'),
    'aff': anton.get('affinity') or 'BC', 'pubmed': 'https://scholar.google.com/citations?user=wiBQ9IQAAAAJ&hl=en'}
for k, old in oldmap.items():
    if not any(k in mk or mk in k for mk in merged):
        merged[k] = {'name': re.sub(r'\s*\([^)]*\)\s*$', '', old['name']),
                     'start': int(old['yr'][:4]), 'end': int(old['now'][:4]), 'role': '',
                     'github': old.get('github') or '', 'country': normcc(old.get('country')),
                     'aff': old.get('affinity') or 'C', 'pubmed': old.get('pubmed') or ''}
if 'cain' in merged: merged['cain']['country'] = merged['cain']['country'] or 'US'
# corrections & additions beyond CV tables
if 'kamali' in merged: merged['kamali']['end'] = 2024
if 'cech' in merged: merged['cech']['end'] = 2025
sm = merged.setdefault('smeds', {'name': 'Patrik Smeds', 'start': 2023, 'end': 2025, 'role': 'Bioinformatician',
    'aff': 'C', 'github': '', 'country': '',
    'pubmed': 'https://www.ncbi.nlm.nih.gov/pubmed/?term=nekrutenko+AND+smeds'})
sm['country'] = sm['country'] or 'SE'
sm['github'] = sm['github'] or '@smeds'
sm['pubmed'] = sm['pubmed'].split(']')[0]
people = list(merged.values())
for p in people:
    p['now'] = p['end'] is None
    p['end'] = p['end'] or CUR_YEAR
people.sort(key=lambda p: (p['start'], p['end']))

KUI_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kui_stats.json')
KUI = json.load(open(KUI_FILE)) if os.path.exists(KUI_FILE) else \
    {'users': '731.7K', 'jobs': '208.9M', 'datasets': '386.3M', 'workflows': '971.5K', 'as_of': '2026-08'}
json.dump(KUI, open(KUI_FILE, 'w'))
import datetime
BUILD_DATE = datetime.date.today().isoformat()
total_cites = sum(p['cites'] for p in pubs)
yr_min = min(p['start'] for p in people)
yr_max = max(p['end'] for p in people)
pub_years = sorted({p['year'] for p in pubs})

collabs = [
    ("Daniel Blankenberg", "Cleveland Clinic", "Cleveland, OH, USA", "https://www.blankenberglab.org/", ""),
    ("Rayan Chikhi", "Institut Pasteur", "Paris, France", "https://rayan.chikhi.name", ""),
    ("Giulio Formenti", "The Rockefeller University", "New York, NY, USA", "https://www.vertebrategenomelab.org/", ""),
    ("Jeremy Goecks", "Moffitt Cancer Center", "Tampa, FL, USA", "https://www.goeckslab.org/", ""),
    ("Björn Grüning", "Albert-Ludwigs-Universität", "Freiburg, Germany", "https://galaxyproject.org/freiburg/", ""),
    ("Maximilian Haeussler", "UC Santa Cruz", "Santa Cruz, CA, USA", "https://ucscgenomics.soe.ucsc.edu/person/maximilian-haeussler/", ""),
    ("Sergei Kosakovsky Pond", "Temple University", "Philadelphia, PA, USA", "https://lab.hyphy.org", ""),
    ("Ross Lazarus", "galaxyproject.org", "Sydney, Australia", "https://github.com/fubar2", ""),
    ("Kateryna Makova", "Penn State", "State College, PA, USA", "https://www.bx.psu.edu/makova_lab/", ""),
    ("David Rogers", "Clever Canary", "Open genomics tools & resources", "https://www.clevercanary.com", ""),
    ("Mike Schatz", "Johns Hopkins", "Baltimore, MD, USA", "https://schatz-lab.org", ""),
    ("James Taylor", "JXTX Foundation", "Baltimore, MD, USA", "https://jxtxfoundation.org", "1979–2020 · in memoriam"),
]

DATA = json.dumps({
    'people': [{'name': p['name'], 'github': p['github'], 'pubmed': p['pubmed'], 'country': p['country'],
                'start': p['start'], 'end': p['end'], 'now': p['now'], 'aff': p['aff'], 'role': p['role']} for p in people],
    'pubs': [{'pmid': p['pmid'], 'url': p['url'], 'title': p['title'],
              'journal': p['journal'], 'year': p['year'], 'cites': p['cites']} for p in pubs],
    'collabs': [{'name': n, 'inst': i, 'loc': l, 'url': u, 'memo': m} for n, i, l, u, m in collabs],
    'stats': {'npubs': len(pubs), 'cites': total_cites, 'npeople': len(people),
              'yr_min': yr_min, 'yr_max': yr_max,
              'pub_yr_min': min(pub_years), 'pub_yr_max': max(pub_years),
              'kui': KUI, 'build_date': BUILD_DATE},
})

FOOT_NOTE = "Publication metadata & citations from NIH iCite · auto-updated monthly via GitHub Actions · last build __BUILD__"


def write(name, body):
    open(f'{OUT}/{name}', 'w').write(body.replace('__DATA__', DATA.replace('<', '\\u003c')))
    print('wrote', name)


# ============================================================ A: TERMINAL
A = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nekrutenko Lab — A · Terminal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
<style>
:root{--bg:#0c0e11;--panel:#12151a;--line:#232830;--fg:#c9d1d9;--dim:#6e7681;--acc:#ff6b4a;--b:#e4574f;--bc:#e8a33d;--cb:#7db2d8;--c:#4a8fd4;--green:#3fb950}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font:14px/1.6 "JetBrains Mono",ui-monospace,monospace;padding:0 0 80px}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:960px;margin:0 auto;padding:0 24px}
header{border-bottom:1px solid var(--line);padding:18px 0;position:sticky;top:0;background:rgba(12,14,17,.92);backdrop-filter:blur(6px);z-index:5}
header .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.logo b{color:#fff}.logo span{color:var(--dim)}
nav a{color:var(--dim);margin-left:18px;font-size:13px}nav a:hover{color:var(--acc);text-decoration:none}
.hero{padding:72px 0 48px}
.prompt{color:var(--green)}
h1{font-size:clamp(28px,5vw,44px);font-weight:700;color:#fff;line-height:1.15;margin:14px 0 18px}
h1 .acc{color:var(--acc)}
.sub{color:var(--dim);max-width:640px}
.stats{display:flex;gap:0;border:1px solid var(--line);border-radius:8px;overflow:hidden;margin:40px 0 0;flex-wrap:wrap}
.stat{flex:1 1 140px;padding:16px 20px;border-right:1px solid var(--line)}
.stat:last-child{border-right:0}
.stat b{display:block;font-size:24px;color:#fff}.stat span{color:var(--dim);font-size:12px}
section{padding:48px 0 8px}
h2{font-size:15px;font-weight:500;color:var(--dim);margin-bottom:24px}
h2 .prompt{margin-right:8px}h2 b{color:#fff;font-weight:700}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:20px}
.person{display:grid;grid-template-columns:230px 1fr 90px;gap:12px;align-items:center;padding:3px 0;font-size:12.5px}
.person .nm{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--fg)}
.person .nm a{color:inherit}
.track{position:relative;height:10px;background:#0a0c0f;border-radius:2px}
.bar{position:absolute;top:2px;bottom:2px;border-radius:2px;min-width:6px}
.person .yrs{color:var(--dim);text-align:right;font-size:11.5px}
.legend{display:flex;gap:18px;margin-top:16px;font-size:11.5px;color:var(--dim);flex-wrap:wrap}
.sw{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.yeargrp{margin-bottom:26px}
.yeargrp h3{color:var(--acc);font-size:13px;margin-bottom:8px}
.pub{display:flex;gap:14px;padding:7px 0;border-bottom:1px dashed var(--line);align-items:baseline}
.pub:last-child{border-bottom:0}
.cites{flex:0 0 64px;text-align:right;font-size:12px;color:var(--dim)}
.cites.hot{color:var(--acc);font-weight:700}
.pub .t{font-size:13px}.pub .t a{color:var(--fg)}.pub .t a:hover{color:var(--acc)}
.pub .j{color:var(--dim);font-size:12px;white-space:nowrap}
.grid3{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px 16px;font-size:13px}
.card b{color:#fff;display:block}.card span{color:var(--dim);font-size:12px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:700px){.two{grid-template-columns:1fr}.person{grid-template-columns:150px 1fr 80px}}
footer{margin-top:64px;border-top:1px solid var(--line);padding-top:20px;color:var(--dim);font-size:12px}
.cursor{display:inline-block;width:9px;height:18px;background:var(--acc);vertical-align:-3px;animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
kbd{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:1px 7px;font-size:12px;color:var(--green)}
</style></head><body>
<header><div class="wrap">
<div class="logo"><b>nekrutenko-lab</b><span> @ penn-state ~ galaxy</span></div>
<nav><a href="#people">people</a><a href="#pubs">pubs</a><a href="#collab">collab</a><a href="#contact">contact</a></nav>
</div></header>
<div class="wrap">
<div class="hero">
<div class="prompt">$ cat README.md</div>
<h1>The birthplace of <span class="acc">Galaxy</span><span class="cursor"></span></h1>
<p class="sub">We build <a href="https://galaxyproject.org">Galaxy</a> — an open, web-based platform for accessible, reproducible, and transparent computational research — together with our collaborators and the worldwide Galaxy community.</p>
<div class="stats" id="stats"></div>
</div>
<section id="people"><h2><span class="prompt">$</span> ./people --timeline <b># biological ⇄ computational</b></h2>
<div class="panel" id="ppl"></div></section>
<section id="pubs"><h2><span class="prompt">$</span> grep -c . publications.txt <b id="pubcount"></b></h2>
<div class="panel" id="publist"></div></section>
<section id="collab"><h2><span class="prompt">$</span> ls collaborators/</h2>
<div class="grid3" id="collabs"></div></section>
<section id="funding"><h2><span class="prompt">$</span> cat FUNDING</h2>
<div class="two">
<div class="card"><b>NIH · NSF</b><span>Primary funding from the National Institutes of Health and the National Science Foundation</span></div>
<div class="card"><b>Huck Institutes</b><span>Additional funds from the Huck Institutes of the Life Sciences at Penn State</span></div>
</div></section>
<section id="contact"><h2><span class="prompt">$</span> finger anton</h2>
<div class="card" style="max-width:420px"><b>Anton Nekrutenko</b>
<span>505 Wartik Lab · University Park, PA 16802 · USA<br>+1 814 845 4752 · <a href="mailto:anton@nekrut.org">anton@nekrut.org</a> · <a href="https://github.com/nekrut">@nekrut</a></span></div></section>
<footer>last build: <kbd>2026-08-01 04:00 UTC</kbd> · __FOOT__</footer>
</div>
<script>
const D=__DATA__;
const AC={B:'var(--b)',BC:'var(--bc)',CB:'var(--cb)',C:'var(--c)'};
const S=D.stats;
document.getElementById('stats').innerHTML=[
 [S.npubs,'publications'],[S.cites.toLocaleString(),'citations'],[S.npeople,'lab members'],
 [S.pub_yr_min+'–now','publishing'],].map(x=>`<div class="stat"><b>${x[0]}</b><span>${x[1]}</span></div>`).join('');
const y0=S.yr_min,y1=S.yr_max,span=y1-y0;
document.getElementById('ppl').innerHTML=D.people.map(p=>{
 const l=(p.start-y0)/span*100,w=Math.max((p.end-p.start)/span*100,1.5);
 return `<div class="person"><div class="nm"><a href="${p.pubmed}">${p.name}</a></div>
 <div class="track"><div class="bar" style="left:${l}%;width:${w}%;background:${AC[p.aff]}" title="${p.start}–${p.end}${p.github?" · "+p.github:""}"></div></div>
 <div class="yrs">${p.start}–${p.end>=2023?'now':p.end}</div></div>`;}).join('')+
 `<div class="legend"><span><i class="sw" style="background:var(--b)"></i>biological</span><span><i class="sw" style="background:var(--bc)"></i>bio→comp</span><span><i class="sw" style="background:var(--cb)"></i>comp→bio</span><span><i class="sw" style="background:var(--c)"></i>computational</span></div>`;
document.getElementById('pubcount').textContent='# '+S.npubs+' papers · '+S.cites.toLocaleString()+' citations';
const byYear={};D.pubs.forEach(p=>{(byYear[p.year]=byYear[p.year]||[]).push(p)});
document.getElementById('publist').innerHTML=Object.keys(byYear).sort((a,b)=>b-a).map(y=>
 `<div class="yeargrp"><h3>── ${y} ──</h3>`+byYear[y].map(p=>
 `<div class="pub"><div class="cites ${p.cites>500?'hot':''}">${p.cites.toLocaleString()}×</div>
 <div class="t"><a href="https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/">${p.title}</a></div>
 <div class="j">${p.journal}</div></div>`).join('')+'</div>').join('');
document.getElementById('collabs').innerHTML=D.collabs.map(c=>
 `<div class="card"><b>${c.name}</b><span>${c.inst} · ${c.loc}</span></div>`).join('');
</script></body></html>"""

# ============================================================ B: INDUSTRIAL BOLD (varda-like)
B = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nekrutenko Lab — B · Industrial</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500&family=Archivo+Expanded:wght@500;700&family=Space+Mono&display=swap" rel="stylesheet">
<style>
:root{--bg:#f4f2ed;--ink:#141412;--dim:#6f6c64;--line:#d8d4ca;--acc:#ff4d00;--card:#fbfaf7}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:15px/1.65 Archivo,system-ui,sans-serif}
a{color:inherit;text-decoration:none}
.mono{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim)}
.wrap{max-width:1200px;margin:0 auto;padding:0 32px}
header{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--ink);z-index:10}
header .wrap{display:flex;justify-content:space-between;align-items:center;height:60px}
.logo{font-family:"Archivo Expanded";font-weight:700;letter-spacing:-.01em}
.logo i{color:var(--acc);font-style:normal}
nav a{font-family:"Space Mono",monospace;font-size:11px;text-transform:uppercase;letter-spacing:.1em;margin-left:26px}
nav a:hover{color:var(--acc)}
.hero{padding:90px 0 60px;border-bottom:1px solid var(--ink)}
h1{font-family:"Archivo Expanded";font-size:clamp(40px,7.5vw,96px);font-weight:700;line-height:.98;letter-spacing:-.02em;text-transform:uppercase}
h1 span{color:var(--acc)}
.hero p{max-width:560px;margin-top:28px;font-size:17px;color:var(--dim)}
.statband{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--ink)}
.statband div{padding:26px 32px;border-right:1px solid var(--ink)}
.statband div:last-child{border-right:0}
.statband b{font-family:"Archivo Expanded";font-size:clamp(26px,3.4vw,44px);display:block;line-height:1}
.statband small{font-family:"Space Mono";font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--dim)}
section{padding:70px 0}
.shead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:36px;border-bottom:1px solid var(--ink);padding-bottom:12px}
h2{font-family:"Archivo Expanded";font-size:clamp(22px,3vw,34px);text-transform:uppercase;letter-spacing:-.01em}
.num{font-family:"Space Mono";color:var(--acc);font-size:13px}
.tl{border:1px solid var(--line);background:var(--card)}
.tlrow{display:grid;grid-template-columns:220px 1fr;border-bottom:1px solid var(--line);align-items:center}
.tlrow:last-child{border-bottom:0}
.flg{width:16px;height:16px;margin-right:8px;vertical-align:-2px}
.tlrow .nm{padding:7px 16px;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-right:1px solid var(--line)}
.tlrow .tr{position:relative;height:100%;min-height:30px}
.tlbar{position:absolute;top:9px;height:12px;min-width:8px}
.axis{display:grid;grid-template-columns:220px 1fr;font-family:"Space Mono";font-size:10px;color:var(--dim);margin-top:8px}
.axis .ticks{display:flex;justify-content:space-between;padding:0 4px}
.hm{overflow-x:auto;padding-bottom:6px}
.hmgrid{display:grid;grid-auto-flow:column;gap:6px}
.hmcol{display:flex;flex-direction:column-reverse;gap:6px}
.cell{width:30px;height:30px;background:#e6e2d8;position:relative;cursor:pointer;transition:transform .1s}
.cell:hover{transform:scale(1.18);z-index:3;outline:2px solid var(--ink)}
.hmyr{font-family:"Space Mono";font-size:9px;color:var(--dim);text-align:center;margin-top:6px;transform:rotate(-60deg);height:26px}
.toplist{margin-top:48px;display:grid;grid-template-columns:1fr 1fr;gap:0 48px}
.tp{display:flex;gap:18px;padding:14px 0;border-bottom:1px solid var(--line);align-items:baseline}
.tp b{font-family:"Archivo Expanded";font-size:20px;color:var(--acc);min-width:74px;text-align:right}
.tp .t{font-size:14px}.tp .t:hover{color:var(--acc)}
.tp small{display:block;color:var(--dim);font-family:"Space Mono";font-size:10px;text-transform:uppercase;margin-top:2px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));border-top:1px solid var(--ink);border-left:1px solid var(--ink)}
.cgrid a{padding:22px;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink);background:var(--card)}
.cgrid a:hover{background:var(--acc);color:#fff}
.cgrid b{display:block;font-family:"Archivo Expanded";font-size:15px}
.cgrid span{font-family:"Space Mono";font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--dim)}
.cgrid a:hover span{color:#ffd9c7}
.fund{display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px}
.fund div{border-top:3px solid var(--ink);padding-top:16px}
.fund b{font-family:"Archivo Expanded"}
footer{border-top:1px solid var(--ink);padding:28px 0 60px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
@media(max-width:820px){.statband{grid-template-columns:1fr 1fr}.statband div{border-bottom:1px solid var(--ink)}.toplist{grid-template-columns:1fr}.tlrow{grid-template-columns:130px 1fr}.axis{grid-template-columns:130px 1fr}.fund{grid-template-columns:1fr}}
.tip{position:fixed;pointer-events:none;background:var(--ink);color:#fff;padding:8px 12px;font-size:12px;max-width:320px;z-index:50;display:none}
.tip small{color:#b8b4aa;font-family:"Space Mono";font-size:10px}
</style></head><body>
<header><div class="wrap"><div class="logo">NEKRUTENKO<i>/</i>LAB</div>
<nav><a href="#team">Team</a><a href="#pubs">Publications</a><a href="#collab">Network</a><a href="#contact">Contact</a></nav></div></header>
<div class="hero"><div class="wrap">
<div class="mono">Penn State · Est. 2000 · galaxyproject.org</div>
<h1>Compute born,<br>biology <span>bound.</span></h1>
<p>The birthplace of <b>Galaxy</b> — the open platform for accessible, reproducible, transparent computational biomedical research, built with collaborators worldwide.</p>
</div></div>
<div class="statband wrap" id="stats" style="padding:0"></div>
<div class="wrap">
<section id="team"><div class="shead"><h2>The Team</h2><span class="num">01 / Biological ⇄ Computational</span></div>
<div class="tl" id="tl"></div><div class="axis"><span></span><div class="ticks" id="ticks"></div></div></section>
<section id="pubs"><div class="shead"><h2>Publications</h2><span class="num" id="pn">02</span></div>
<div class="mono" style="margin-bottom:14px">Every paper since __PY0__ · cell area = one paper · color = citations · click to open</div>
<div class="hm"><div class="hmgrid" id="hm"></div></div>
<div class="mono" style="margin:40px 0 0">Most cited</div>
<div class="toplist" id="top"></div></section>
<section id="collab"><div class="shead"><h2>The Network</h2><span class="num">03 / Key collaborators</span></div>
<div class="cgrid" id="cg"></div>
<div class="mono" style="margin:36px 0 10px">Public usegalaxy.* servers</div>
<div class="wmap"><img src="world.svg" alt="World map of public Galaxy servers">
<a class="srv" style="left:18.5%;top:42.6%" href="https://usegalaxy.org" target="_blank" rel="noopener"><i></i>usegalaxy.org</a>
<a class="srv" style="left:25.4%;top:35.0%" href="https://usegalaxy.ca" target="_blank" rel="noopener"><i></i>.ca</a>
<a class="srv srv-l" style="left:48.8%;top:32.8%" href="https://usegalaxy.fr" target="_blank" rel="noopener"><i></i>.fr</a>
<a class="srv" style="left:50.2%;top:33.4%" href="https://usegalaxy.eu" target="_blank" rel="noopener"><i></i>.eu</a>
<a class="srv srv-l" style="left:91.4%;top:94.6%" href="https://usegalaxy.org.au" target="_blank" rel="noopener"><i></i>.org.au</a>
</div></section>
<section id="funding"><div class="shead"><h2>Funding</h2><span class="num">04</span></div>
<div class="fund">
<div><b>NIH</b><p>National Institutes of Health — primary support.</p></div>
<div><b>NSF</b><p>National Science Foundation — primary support.</p></div>
<div><b>Huck Institutes</b><p>Of the Life Sciences at Penn State — additional funds.</p></div>
</div></section>
</div>
<footer><div class="wrap" style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:20px;width:100%" id="contact">
<div><div class="logo">NEKRUTENKO<i>/</i>LAB</div><div class="mono" style="margin-top:8px">505 Wartik Lab · University Park PA 16802<br>+1 814 845 4752 · anton@nekrut.org</div></div>
<div class="mono">__FOOT__</div>
</div></footer>
<div class="tip" id="tip"></div>
<script>
const D=__DATA__,S=D.stats;
const AC={B:'#d43d2a',BC:'#e09b2d',CB:'#5f8fb4',C:'#2a5fd4'};
document.getElementById('stats').innerHTML=[[S.npubs,'Publications'],[S.cites.toLocaleString(),'Citations'],[S.npeople,'Lab members over the years'],[(S.pub_yr_max-S.pub_yr_min)+' yrs','Publishing '+S.pub_yr_min+'–now']]
 .map(x=>`<div><b>${x[0]}</b><small>${x[1]}</small></div>`).join('');
const y0=S.yr_min,y1=S.yr_max,sp=y1-y0;
document.getElementById('tl').innerHTML=D.people.map(p=>{
 const l=(p.start-y0)/sp*100,w=Math.max((p.end-p.start)/sp*100,1);
 return `<div class="tlrow"><a class="nm" href="${p.pubmed}">${p.name}</a><div class="tr"><div class="tlbar" style="left:${l}%;width:${w}%;background:${AC[p.aff]}"></div></div></div>`}).join('');
document.getElementById('ticks').innerHTML=Array.from({length:Math.floor(sp/4)+1},(_,i)=>`<span>${y0+i*4}</span>`).join('');
const byY={};D.pubs.forEach(p=>{(byY[p.year]=byY[p.year]||[]).push(p)});
const mx=Math.max(...D.pubs.map(p=>p.cites));
const heat=c=>{const t=Math.log(c+1)/Math.log(mx+1);
 return `hsl(${18-t*6} ${55+t*45}% ${88-t*55}%)`}
const tip=document.getElementById('tip');
document.getElementById('hm').innerHTML=Object.keys(byY).sort().map(y=>
 `<div><div class="hmcol">`+byY[y].map(p=>
 `<a class="cell" href="https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/" style="background:${heat(p.cites)}" data-t="${p.title.replace(/"/g,'&quot;')}" data-j="${p.journal} · ${y} · ${p.cites.toLocaleString()} citations"></a>`).join('')+
 `</div><div class="hmyr">'${String(y).slice(2)}</div></div>`).join('');
document.addEventListener('mousemove',e=>{const c=e.target.closest('.cell');
 if(c){tip.style.display='block';tip.innerHTML=c.dataset.t+'<br><small>'+c.dataset.j+'</small>';
 tip.style.left=Math.min(e.clientX+14,innerWidth-340)+'px';tip.style.top=e.clientY+16+'px';}
 else tip.style.display='none';});
document.getElementById('pn').textContent='02 / '+S.npubs+' papers · '+S.cites.toLocaleString()+' citations';
document.getElementById('top').innerHTML=[...D.pubs].sort((a,b)=>b.cites-a.cites).slice(0,10).map(p=>
 `<div class="tp"><b>${p.cites.toLocaleString()}</b><div><a class="t" href="https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/">${p.title}</a><small>${p.journal} · ${p.year}</small></div></div>`).join('');
document.getElementById('cg').innerHTML=D.collabs.map(c=>
 `<a><b>${c.name}</b><span>${c.inst} — ${c.loc}</span></a>`).join('');
</script></body></html>"""

# ============================================================ C: MINIMAL ADAPTIVE (pi.dev-like)
C = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nekrutenko Lab — C · Quiet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#fdfdfc;--fg:#1a1a18;--dim:#75756e;--line:#e8e8e3;--soft:#f4f4f0;--acc:#0d7a5f;--b:#c2543f;--bc:#d99a3d;--cb:#6d9cbf;--c:#3d6bc2}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#131312;--fg:#e6e6e1;--dim:#8f8f88;--line:#282824;--soft:#1c1c1a;--acc:#3fbf9a}}
:root[data-theme=dark]{--bg:#131312;--fg:#e6e6e1;--dim:#8f8f88;--line:#282824;--soft:#1c1c1a;--acc:#3fbf9a}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font:15px/1.7 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.mono{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--dim)}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:720px;margin:0 auto;padding:0 24px}
header{padding:22px 0;border-bottom:1px solid var(--line)}
header .wrap{display:flex;justify-content:space-between;align-items:center;max-width:720px}
.logo{font-weight:600;font-size:15px;color:var(--fg)}
nav{display:flex;gap:18px;align-items:center}
nav a{color:var(--dim);font-size:13.5px}nav a:hover{color:var(--fg);text-decoration:none}
#mode{cursor:pointer;border:1px solid var(--line);background:var(--soft);color:var(--dim);border-radius:99px;padding:3px 12px;font:12px "IBM Plex Mono",monospace}
.hero{padding:72px 0 40px}
h1{font-size:clamp(30px,4.6vw,42px);font-weight:600;letter-spacing:-.025em;line-height:1.15}
.hero p{margin-top:18px;color:var(--dim);font-size:16.5px;max-width:600px}
.hero .mono{margin-bottom:14px;color:var(--acc)}
.chips{display:flex;gap:10px;margin-top:26px;flex-wrap:wrap}
.chip{border:1px solid var(--line);background:var(--soft);border-radius:99px;padding:5px 14px;font:12.5px "IBM Plex Mono",monospace;color:var(--dim)}
.chip b{color:var(--fg);font-weight:500}
section{padding:52px 0 6px}
h2{font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.09em;color:var(--dim);margin-bottom:22px;display:flex;align-items:baseline;gap:10px}
h2:after{content:"";flex:1;border-top:1px solid var(--line)}
.prow{display:grid;grid-template-columns:1fr 200px;gap:14px;padding:6.5px 0;border-bottom:1px solid var(--line);align-items:center;font-size:13.5px}
.prow:last-of-type{border-bottom:0}
.prow .nm a{color:var(--fg)}.prow .nm a:hover{color:var(--acc)}
.spark{position:relative;height:8px;background:var(--soft);border-radius:99px}
.spark i{position:absolute;top:0;bottom:0;border-radius:99px;min-width:5px}
.lg{display:flex;gap:16px;margin-top:14px;font:11.5px "IBM Plex Mono",monospace;color:var(--dim);flex-wrap:wrap}
.dot{display:inline-block;width:8px;height:8px;border-radius:99px;margin-right:5px}
details{border-bottom:1px solid var(--line)}
summary{cursor:pointer;padding:12px 0;display:flex;justify-content:space-between;align-items:baseline;gap:14px;list-style:none;font-weight:500;font-size:14.5px}
summary::-webkit-details-marker{display:none}
summary:hover{color:var(--acc)}
summary .mono{white-space:nowrap}
.pubs-inner{padding:2px 0 16px}
.pb{display:grid;grid-template-columns:56px 1fr;gap:12px;padding:6px 0;font-size:13.5px;align-items:baseline}
.pb .c{font:12px "IBM Plex Mono",monospace;color:var(--dim);text-align:right}
.pb .c.hot{color:var(--acc);font-weight:500}
.pb a{color:var(--fg)}.pb a:hover{color:var(--acc)}
.pb small{color:var(--dim);font-size:12px}
.clist{display:grid;grid-template-columns:1fr 1fr;gap:2px 32px}
.cl{padding:9px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.cl b{font-weight:500}.cl div{color:var(--dim);font-size:12.5px}
.note{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:16px 20px;font-size:13.5px;color:var(--dim)}
footer{margin:70px 0 60px;padding-top:20px;border-top:1px solid var(--line);color:var(--dim);font-size:12.5px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media(max-width:640px){.prow{grid-template-columns:1fr 110px}.clist{grid-template-columns:1fr}}
</style></head><body>
<header><div class="wrap">
<div class="logo">Nekrutenko Lab</div>
<nav><a href="#people">People</a><a href="#pubs">Papers</a><a href="#collab">Collaborators</a><button id="mode">auto</button></nav>
</div></header>
<main class="wrap">
<div class="hero">
<div class="mono">~ the birthplace of galaxy</div>
<h1>Accessible, reproducible, transparent computational research.</h1>
<p>Our lab created <a href="https://galaxyproject.org">Galaxy</a>. We develop and maintain it with collaborators and the worldwide Galaxy community, at Penn State.</p>
<div class="chips" id="chips"></div>
</div>
<section id="people"><h2>People</h2>
<div id="ppl"></div>
<div class="lg"><span><i class="dot" style="background:var(--b)"></i>biological</span><span><i class="dot" style="background:var(--bc)"></i>bio→comp</span><span><i class="dot" style="background:var(--cb)"></i>comp→bio</span><span><i class="dot" style="background:var(--c)"></i>computational</span></div>
</section>
<section id="pubs"><h2>Publications</h2><div id="publist"></div></section>
<section id="collab"><h2>Collaborators</h2><div class="clist" id="cl"></div></section>
<section id="funding"><h2>Funding</h2>
<p class="note">Primarily funded by the <b>National Institutes of Health</b> and the <b>National Science Foundation</b>, with additional support from the <b>Huck Institutes of the Life Sciences</b> at Penn State.</p></section>
<section id="contact"><h2>Contact</h2>
<p style="font-size:14px">Anton Nekrutenko · 505 Wartik Lab, University Park, PA 16802, USA<br>
<span class="mono">+1 814 845 4752 · <a href="mailto:anton@nekrut.org">anton@nekrut.org</a> · <a href="https://github.com/nekrut">github.com/nekrut</a></span></p></section>
<footer><span>© Nekrutenko Lab, Penn State</span><span>__FOOT__</span></footer>
</main>
<script>
const D=__DATA__,S=D.stats;
const AC={B:'var(--b)',BC:'var(--bc)',CB:'var(--cb)',C:'var(--c)'};
document.getElementById('chips').innerHTML=[
 ['<b>'+S.npubs+'</b> papers'],['<b>'+S.cites.toLocaleString()+'</b> citations'],
 ['<b>'+S.npeople+'</b> members'],['<b>'+S.pub_yr_min+'–now</b>']].map(x=>`<span class="chip">${x}</span>`).join('');
const y0=S.yr_min,sp=S.yr_max-y0;
document.getElementById('ppl').innerHTML=D.people.map(p=>{
 const l=(p.start-y0)/sp*100,w=Math.max((p.end-p.start)/sp*100,2);
 return `<div class="prow"><span class="nm"><a href="${p.pubmed}">${p.name}</a>${p.github?` <span class="mono">${p.github}</span>`:''}</span>
 <span class="spark" title="${p.start}–${p.end}"><i style="left:${l}%;width:${w}%;background:${AC[p.aff]}"></i></span></div>`}).join('');
const byY={};D.pubs.forEach(p=>{(byY[p.year]=byY[p.year]||[]).push(p)});
const yrs=Object.keys(byY).sort((a,b)=>b-a);
document.getElementById('publist').innerHTML=yrs.map((y,i)=>{
 const ps=byY[y],c=ps.reduce((a,p)=>a+p.cites,0);
 return `<details ${i<2?'open':''}><summary><span>${y}</span><span class="mono">${ps.length} paper${ps.length>1?'s':''} · ${c.toLocaleString()} citations</span></summary>
 <div class="pubs-inner">`+ps.map(p=>
 `<div class="pb"><span class="c ${p.cites>500?'hot':''}">${p.cites.toLocaleString()}</span>
 <span><a href="https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/">${p.title}</a> <small>— ${p.journal}</small></span></div>`).join('')+`</div></details>`}).join('');
document.getElementById('cl').innerHTML=D.collabs.map(c=>
 `<div class="cl"><b>${c.name}</b><div>${c.inst} · ${c.loc}</div></div>`).join('');
const btn=document.getElementById('mode'),modes=['auto','light','dark'];let mi=0;
btn.onclick=()=>{mi=(mi+1)%3;const m=modes[mi];btn.textContent=m;
 if(m==='auto')document.documentElement.removeAttribute('data-theme');
 else document.documentElement.setAttribute('data-theme',m);};
</script></body></html>"""

# ============================================================ D: SWISS DATA
D_ = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nekrutenko Lab — D · Swiss</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;600;800&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#fff;--ink:#0a0a0a;--dim:#8a8a8a;--line:#e2e2e2;--red:#e30613;--b:#e30613;--bc:#f28c28;--cb:#5b9bd5;--c:#1436c9}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:15px/1.6 "Inter Tight",system-ui,sans-serif}
a{color:inherit;text-decoration:none}
.mono{font-family:"Spline Sans Mono",monospace;font-size:11px;letter-spacing:.04em;color:var(--dim)}
.wrap{max-width:1140px;margin:0 auto;padding:0 28px}
header{border-bottom:3px solid var(--ink)}
header .wrap{display:flex;justify-content:space-between;align-items:flex-end;padding:20px 28px 14px}
.logo{font-weight:800;font-size:20px;letter-spacing:-.03em}
.logo em{font-style:normal;color:var(--red)}
nav a{font-size:13px;font-weight:600;margin-left:22px}nav a:hover{color:var(--red)}
.hero{display:grid;grid-template-columns:2fr 1fr;border-bottom:1px solid var(--ink)}
.hero>div{padding:64px 28px}
.hero .left{border-right:1px solid var(--ink)}
h1{font-size:clamp(38px,5.5vw,72px);font-weight:800;letter-spacing:-.04em;line-height:1.0}
h1 em{font-style:normal;color:var(--red)}
.hero p{margin-top:24px;max-width:520px;color:#444}
.bignum{display:flex;flex-direction:column;gap:24px;justify-content:center}
.bignum b{font-size:clamp(34px,4vw,52px);font-weight:800;letter-spacing:-.03em;line-height:1;display:block}
.bignum b i{font-style:normal;color:var(--red)}
section{border-bottom:1px solid var(--ink);padding:56px 0}
.shead{display:grid;grid-template-columns:60px 1fr auto;gap:20px;align-items:baseline;margin-bottom:36px}
.shead .n{font-family:"Spline Sans Mono";font-size:13px;color:var(--red)}
h2{font-size:clamp(24px,3vw,36px);font-weight:800;letter-spacing:-.03em}
svg text{font-family:"Spline Sans Mono",monospace}
.chartbox{overflow-x:auto}
.pubtable{width:100%;border-collapse:collapse;font-size:13.5px}
.pubtable th{font-family:"Spline Sans Mono";font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--dim);text-align:left;padding:8px 12px 8px 0;border-bottom:2px solid var(--ink)}
.pubtable td{padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:baseline}
.pubtable tr:hover td{background:#fafafa}
.pubtable .yr,.pubtable .ct{font-family:"Spline Sans Mono";font-size:12px;white-space:nowrap}
.pubtable .ct{text-align:right}.hot{color:var(--red);font-weight:600}
.pubtable a:hover{color:var(--red)}
.jr{color:var(--dim);font-size:12.5px;white-space:nowrap}
.showmore{margin-top:18px;font-family:"Spline Sans Mono";font-size:12px;border:1px solid var(--ink);background:none;padding:9px 22px;cursor:pointer}
.showmore:hover{background:var(--ink);color:#fff}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.cgrid div{background:var(--bg);padding:18px 20px}
.cgrid b{font-weight:600;font-size:14px}
.cgrid span{display:block;color:var(--dim);font-size:12.5px}
.frow{display:flex;gap:60px;flex-wrap:wrap}
.frow b{font-size:22px;font-weight:800;letter-spacing:-.02em}
.frow span{display:block;color:var(--dim);font-size:13px;max-width:220px}
footer{padding:32px 0 70px;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
@media(max-width:800px){.hero{grid-template-columns:1fr}.hero .left{border-right:0;border-bottom:1px solid var(--ink)}.bignum{flex-direction:row;flex-wrap:wrap}}
.tip2{position:fixed;pointer-events:none;background:var(--ink);color:#fff;padding:8px 12px;font-size:12px;max-width:330px;display:none;z-index:40}
</style></head><body>
<header><div class="wrap"><div class="logo">Nekrutenko Lab<em>.</em></div>
<nav><a href="#p">People</a><a href="#pub">Publications</a><a href="#c">Collaborators</a><a href="#f">Funding</a></nav></div></header>
<div class="hero wrap" style="padding:0">
<div class="left"><div class="mono" style="margin-bottom:16px">PENN STATE · GALAXYPROJECT.ORG</div>
<h1>The birthplace of <em>Galaxy</em>.</h1>
<p>An open, web-based platform enabling accessible, reproducible, and transparent computational research — developed here and maintained with our collaborators and the worldwide Galaxy community.</p></div>
<div class="bignum" id="bn"></div>
</div>
<div class="wrap">
<section id="p"><div class="shead"><span class="n">01</span><h2>Two and a half decades of people</h2><span class="mono">COLOR = BIOLOGICAL ⇄ COMPUTATIONAL AFFINITY</span></div>
<div class="chartbox"><svg id="tlsvg" width="1080"></svg></div></section>
<section id="pub"><div class="shead"><span class="n">02</span><h2>Publications</h2><span class="mono" id="pmeta"></span></div>
<div class="chartbox"><svg id="barsvg" width="1080" height="150"></svg></div>
<table class="pubtable"><thead><tr><th style="width:52px">Year</th><th>Title</th><th>Journal</th><th style="text-align:right">Cited</th></tr></thead><tbody id="ptb"></tbody></table>
<button class="showmore" id="more">SHOW ALL __N__ PAPERS ↓</button></section>
<section id="c"><div class="shead"><span class="n">03</span><h2>Collaborators</h2></div>
<div class="cgrid" id="cg"></div>
<div class="mono" style="margin:36px 0 10px">Public usegalaxy.* servers</div>
<div class="wmap"><img src="world.svg" alt="World map of public Galaxy servers">
<a class="srv" style="left:18.5%;top:42.6%" href="https://usegalaxy.org" target="_blank" rel="noopener"><i></i>usegalaxy.org</a>
<a class="srv" style="left:25.4%;top:35.0%" href="https://usegalaxy.ca" target="_blank" rel="noopener"><i></i>.ca</a>
<a class="srv srv-l" style="left:48.8%;top:32.8%" href="https://usegalaxy.fr" target="_blank" rel="noopener"><i></i>.fr</a>
<a class="srv" style="left:50.2%;top:33.4%" href="https://usegalaxy.eu" target="_blank" rel="noopener"><i></i>.eu</a>
<a class="srv srv-l" style="left:91.4%;top:94.6%" href="https://usegalaxy.org.au" target="_blank" rel="noopener"><i></i>.org.au</a>
</div></section>
<section id="f"><div class="shead"><span class="n">04</span><h2>Funding</h2></div>
<div class="frow">
<div><b>NIH</b><span>National Institutes of Health — primary funding</span></div>
<div><b>NSF</b><span>National Science Foundation — primary funding</span></div>
<div><b>Huck</b><span>Huck Institutes of the Life Sciences, Penn State — additional funds</span></div>
</div></section>
<footer><div><b>Anton Nekrutenko</b><br><span class="mono">505 WARTIK LAB · UNIVERSITY PARK PA 16802 · +1 814 845 4752 · ANTON@NEKRUT.ORG</span></div>
<span class="mono">__FOOT__</span></footer>
</div>
<div class="tip2" id="tip"></div>
<script>
const D=__DATA__,S=D.stats;
const AC={B:'var(--b)',BC:'var(--bc)',CB:'var(--cb)',C:'var(--c)'};
document.getElementById('bn').innerHTML=[[S.npubs,'publications'],[S.cites.toLocaleString(),'citations'],[S.npeople,'members '+S.yr_min+'–now']]
 .map(x=>`<div><b><i>${x[0]}</i></b><span class="mono">${String(x[1]).toUpperCase()}</span></div>`).join('');
// people timeline SVG
const svg=document.getElementById('tlsvg'),W=1080,RH=24,ML=210,MT=26;
const y0=S.yr_min,y1=S.yr_max,sp=y1-y0,cw=W-ML-20;
svg.setAttribute('height',MT+D.people.length*RH+10);
let g='';
for(let y=y0;y<=y1;y+=2){const x=ML+(y-y0)/sp*cw;
 g+=`<line x1="${x}" y1="${MT-8}" x2="${x}" y2="${MT+D.people.length*RH}" stroke="var(--line)"/>
 <text x="${x}" y="${MT-12}" font-size="10" fill="var(--dim)" text-anchor="middle">${y}</text>`;}
D.people.forEach((p,i)=>{const y=MT+i*RH;
 const x=ML+(p.start-y0)/sp*cw, w=Math.max((p.end-p.start)/sp*cw,6);
 g+=`<a href="${p.pubmed}"><text x="${ML-10}" y="${y+13}" font-size="11" fill="var(--ink)" text-anchor="end">${p.name}</text>
 <rect x="${x}" y="${y+4}" width="${w}" height="11" fill="${AC[p.aff]}" rx="1"><title>${p.name} · ${p.start}–${p.end}${p.github?" · "+p.github:""}</title></rect></a>`;});
svg.innerHTML=g;
// pubs/year bar chart
const byY={};D.pubs.forEach(p=>{(byY[p.year]=byY[p.year]||[]).push(p)});
const yrs=Object.keys(byY).sort();
const bs=document.getElementById('barsvg'),bw=Math.min(34,(1040)/yrs.length-6);
const mxn=Math.max(...yrs.map(y=>byY[y].length));
bs.innerHTML=yrs.map((y,i)=>{const h=byY[y].length/mxn*95,x=20+i*((1040)/yrs.length);
 return `<rect x="${x}" y="${110-h}" width="${bw}" height="${h}" fill="var(--ink)"><title>${y}: ${byY[y].length} papers</title></rect>
 <text x="${x+bw/2}" y="${104-h}" font-size="9.5" fill="var(--dim)" text-anchor="middle">${byY[y].length}</text>
 <text x="${x+bw/2}" y="${126}" font-size="9" fill="var(--dim)" text-anchor="middle" transform="rotate(-50 ${x+bw/2} 126)">${y}</text>`}).join('');
document.getElementById('pmeta').textContent=S.npubs+' PAPERS · '+S.cites.toLocaleString()+' CITATIONS · SOURCE: PUBMED + ICITE';
// table
const rows=D.pubs.map(p=>`<tr><td class="yr">${p.year}</td>
 <td><a href="https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/">${p.title}</a></td>
 <td class="jr">${p.journal}</td><td class="ct ${p.cites>500?'hot':''}">${p.cites.toLocaleString()}</td></tr>`);
const tb=document.getElementById('ptb'),btn=document.getElementById('more');
tb.innerHTML=rows.slice(0,15).join('');
btn.onclick=()=>{tb.innerHTML=rows.join('');btn.remove();};
document.getElementById('cg').innerHTML=D.collabs.map(c=>
 `<div><b>${c.name}</b><span>${c.inst} · ${c.loc}</span></div>`).join('');
</script></body></html>"""

A = A.replace('__FOOT__', FOOT_NOTE.replace('__BUILD__', BUILD_DATE))
B = B.replace('__FOOT__', FOOT_NOTE.replace('__BUILD__', BUILD_DATE)).replace('__PY0__', str(min(pub_years)))
C = C.replace('__FOOT__', FOOT_NOTE.replace('__BUILD__', BUILD_DATE))
D_ = D_.replace('__FOOT__', FOOT_NOTE.replace('__BUILD__', BUILD_DATE)).replace('__N__', str(len(pubs)))

write('a-terminal.html', A)
write('b-industrial.html', B)
# ============================================================ E: standalone (B structure + D fonts + products/flags/kui-stats/collab-links)
E = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nekrutenko Lab (anLab) — Galaxy · Penn State</title>
<meta name="description" content="anLab — the Anton Nekrutenko lab at Penn State, birthplace of Galaxy: the open platform for accessible, reproducible computational biomedical research.">
<link rel="canonical" href="https://nekrut.org/">
<meta property="og:title" content="Nekrutenko Lab — birthplace of Galaxy">
<meta property="og:description" content="Open, reproducible computational biomedical research at Penn State. 100+ papers, 20,000+ citations, Galaxy and its ecosystem.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://nekrut.org/">
<meta property="og:image" content="https://nekrut.org/logos/galaxy.png">
<meta name="twitter:card" content="summary">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23141412'/><text x='28' y='82' font-size='90' font-family='monospace' fill='%23ff4d00'>/</text></svg>">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"ResearchOrganization","name":"Nekrutenko Lab (anLab)","url":"https://nekrut.org/","parentOrganization":{"@type":"CollegeOrUniversity","name":"The Pennsylvania State University"},"address":{"@type":"PostalAddress","streetAddress":"505 Wartik Lab","addressLocality":"University Park","addressRegion":"PA","postalCode":"16802","addressCountry":"US"},"email":"aun1@psu.edu","telephone":"+1-814-826-9628","founder":{"@type":"Person","name":"Anton Nekrutenko","jobTitle":"Dorothy Foehr Huck and J. Lloyd Huck Chair in Genomics; Professor of Biochemistry and Molecular Biology","sameAs":["https://github.com/nekrut"]}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;800&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#f4f2ed;--ink:#141412;--dim:#6f6c64;--line:#d8d4ca;--acc:#ff4d00;--acc-text:#d63a00;--card:#fbfaf7}
html{scroll-behavior:smooth}
section[id],#contact{scroll-margin-top:76px}
.skip{position:absolute;left:-999px;top:0;background:var(--ink);color:#fff;padding:8px 16px;z-index:99}
.skip:focus{left:0}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:15px/1.65 "Inter Tight",system-ui,sans-serif}
a{color:inherit;text-decoration:none}
.mono{font-family:"Spline Sans Mono",monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim)}
.wrap{max-width:1200px;margin:0 auto;padding:0 32px}
header{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--ink);z-index:10}
header .wrap{display:flex;justify-content:space-between;align-items:center;height:60px}
.logo{font-family:"Inter Tight";font-weight:800;letter-spacing:-.01em}
.logo i{color:var(--acc);font-style:normal}
nav a{font-family:"Spline Sans Mono",monospace;font-size:11px;text-transform:uppercase;letter-spacing:.1em;margin-left:26px}
nav a:hover{color:var(--acc)}
.hero{padding:90px 0 60px;border-bottom:1px solid var(--ink)}
h1{font-family:"Inter Tight";font-weight:800;font-size:clamp(40px,7.5vw,96px);line-height:.98;letter-spacing:-.02em;text-transform:none}
h1 span{color:var(--acc)}
.hero p{max-width:560px;margin-top:28px;font-size:17px;color:var(--dim)}
.statband{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--ink)}
.statband div{padding:26px 32px;border-right:1px solid var(--ink)}
.statband div:last-child{border-right:0}
.statband b{font-family:"Inter Tight";font-weight:800;font-size:clamp(26px,3.4vw,44px);display:block;line-height:1}
.statband small{font-family:"Spline Sans Mono";font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--dim)}
.statnote{padding:10px 32px;border-bottom:1px solid var(--ink);font-family:"Spline Sans Mono";font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)}
section{padding:70px 0}
.shead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:36px;border-bottom:1px solid var(--ink);padding-bottom:12px}
h2{font-family:"Inter Tight";font-weight:800;font-size:clamp(22px,3vw,34px);text-transform:uppercase;letter-spacing:-.01em}
.num{font-family:"Spline Sans Mono";color:var(--acc-text);font-size:13px}
.tl{border:1px solid var(--line);background:var(--card)}
.tlrow{display:grid;grid-template-columns:230px 1fr;border-bottom:1px solid var(--line);align-items:center}
.tlrow:last-child{border-bottom:0}
.flg{width:14px;height:14px;margin-right:8px;vertical-align:-2px}
.tlrow .nm{padding:3px 16px;font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-right:1px solid var(--line)}
.tlrow .tr{position:relative;height:100%;min-height:22px}
.tlbar{position:absolute;top:6px;height:10px;min-width:8px}
.axis{display:grid;grid-template-columns:230px 1fr;font-family:"Spline Sans Mono";font-size:10px;color:var(--dim);margin-top:8px}
.axis .ticks{position:relative;height:14px;font-size:9px}
.axis .ticks span{position:absolute;transform:translateX(-50%)}
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--ink);border:1px solid var(--ink)}
.pcard{background:var(--card);padding:28px;display:flex;flex-direction:column;gap:14px}
.pcard:hover{background:#fff}

.plogo{height:58px;display:flex;align-items:center}
.plogo img{height:46px;width:auto;max-width:95%;object-fit:contain}
.pcard b{font-family:"Inter Tight";font-weight:800;font-size:17px;text-transform:uppercase;letter-spacing:.01em}
.pcard b em{font-style:normal;font-family:"Spline Sans Mono";font-weight:400;font-size:10px;color:var(--acc-text);letter-spacing:.1em;vertical-align:2px;margin-left:8px}
.pcard p{font-size:13.5px;color:var(--dim);flex:1}
.pcard .gh{font-family:"Spline Sans Mono";font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--acc-text)}
.hm{overflow-x:auto;padding-bottom:6px}
.hmgrid{display:grid;grid-auto-flow:column;gap:6px}
.hmcol{display:flex;flex-direction:column-reverse;gap:6px}
.cell{width:30px;height:30px;background:#e6e2d8;position:relative;cursor:pointer;transition:transform .1s}
.cell:hover{transform:scale(1.18);z-index:3;outline:2px solid var(--ink)}
.cell:focus-visible{outline:2px solid var(--acc-text);z-index:3}
.lg{display:flex;gap:18px;margin-top:12px;font-family:"Spline Sans Mono";font-size:10.5px;color:var(--dim);flex-wrap:wrap;text-transform:uppercase;letter-spacing:.06em}
.dot{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.hscale{display:flex;align-items:center;gap:10px;margin-top:14px;font-family:"Spline Sans Mono";font-size:10.5px;color:var(--dim)}
.hscale .ramp{height:10px;flex:0 0 160px;border:1px solid var(--line)}
.memo{display:block;font-family:"Spline Sans Mono";font-size:9.5px;color:var(--acc-text);letter-spacing:.06em;text-transform:uppercase;margin-top:4px}
.cgrid a:hover .memo{color:#ffd9c7}
.wmap{position:relative;border:1px solid var(--line);background:var(--card);margin-top:4px}
.wmap>img{display:block;width:100%;height:auto;opacity:.9}
.srv{position:absolute;display:flex;align-items:center;gap:6px;font-family:"Spline Sans Mono";font-size:11px;font-weight:500;color:var(--ink);white-space:nowrap;transform:translate(-8px,-8px)}
.srv i{position:relative;width:12px;height:12px;border-radius:99px;background:var(--acc);border:2px solid var(--card);outline:1px solid var(--ink);flex:0 0 12px}
.srv i::after{content:"";position:absolute;inset:-2px;border-radius:99px;border:2px solid var(--acc);animation:pulse 2.2s ease-out infinite}
.srv:nth-child(3) i::after{animation-delay:.4s}.srv:nth-child(4) i::after{animation-delay:.8s}.srv:nth-child(5) i::after{animation-delay:1.2s}.srv:nth-child(6) i::after{animation-delay:1.6s}
@keyframes pulse{0%{transform:scale(1);opacity:.9}70%{transform:scale(2.6);opacity:0}100%{transform:scale(2.6);opacity:0}}
@media(prefers-reduced-motion:reduce){.srv i::after{animation:none;display:none}}
.srv:hover{color:var(--acc-text)}
.srv-l{transform:translate(calc(-100% + 8px),-8px);flex-direction:row-reverse}
@media(max-width:600px){.srv{font-size:8.5px}.srv i{width:9px;height:9px;flex-basis:9px}}
#totop{position:fixed;right:22px;bottom:22px;background:var(--ink);color:#fff;font-family:"Spline Sans Mono";font-size:11px;padding:9px 13px;border:0;cursor:pointer;display:none;z-index:20}
#totop:hover{background:var(--acc-text)}
nav a.active{color:var(--acc-text)}
.hmyr{font-family:"Spline Sans Mono";font-size:9px;color:var(--dim);text-align:center;margin-top:8px;height:14px;white-space:nowrap}
.toplist{margin-top:48px;display:grid;grid-template-columns:1fr 1fr;gap:0 48px}
.tp{display:flex;gap:18px;padding:14px 0;border-bottom:1px solid var(--line);align-items:baseline}
.tp b{font-family:"Inter Tight";font-weight:800;font-size:20px;color:var(--acc);min-width:74px;text-align:right}
.tp .t{font-size:14px;text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:3px}.tp .t:hover{color:var(--acc-text);text-decoration-color:var(--acc-text)}
.tp small{display:block;color:var(--dim);font-family:"Spline Sans Mono";font-size:10px;text-transform:uppercase;margin-top:2px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));border-top:1px solid var(--ink);border-left:1px solid var(--ink)}
.cgrid a{padding:22px;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink);background:var(--card)}
.cgrid a:hover{background:var(--acc);color:#fff}
.cgrid b{display:block;font-family:"Inter Tight";font-weight:800;font-size:15px}
.cgrid span{font-family:"Spline Sans Mono";font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--dim)}
.cgrid a:hover span{color:#ffd9c7}
.ggrid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--ink);border:1px solid var(--ink)}
.gcard{background:var(--card);padding:20px;display:flex;flex-direction:column;gap:8px}
.gcard:hover{background:#fff}
.gtop{display:flex;justify-content:space-between;align-items:center;gap:8px}
.rolepill{font-family:"Spline Sans Mono";font-size:10.5px;letter-spacing:.08em;padding:2px 9px;border-radius:99px}
.rolepill.pd{background:var(--acc-text);color:#fff}
.rolepill.coi{border:1px solid var(--dim);color:var(--dim)}
.gcard b{font-family:"Inter Tight";font-weight:800;font-size:24px;line-height:1}
.gcard p{font-size:12.5px;color:var(--dim);flex:1}
@media(max-width:1000px){.ggrid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.ggrid{grid-template-columns:1fr}}
footer{border-top:1px solid var(--ink);padding:28px 0 60px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
@media(max-width:660px){header .wrap{height:auto;flex-wrap:wrap;padding:10px 16px;gap:6px}nav a{margin:0 14px 0 0;font-size:10px}}
@media print{header{position:static}nav,.tip,#totop{display:none}.hm{overflow:visible}.cell{print-color-adjust:exact;-webkit-print-color-adjust:exact}body{background:#fff}}
@media(max-width:820px){.statband{grid-template-columns:1fr 1fr}.statband div{border-bottom:1px solid var(--ink)}.toplist{grid-template-columns:1fr}.tlrow{grid-template-columns:150px 1fr}.axis{grid-template-columns:150px 1fr}.fund{grid-template-columns:1fr}.pgrid{grid-template-columns:1fr}}
.tip{position:fixed;pointer-events:none;background:var(--ink);color:#fff;padding:8px 12px;font-size:12px;max-width:320px;z-index:50;display:none}
.tip small{color:#b8b4aa;font-family:"Spline Sans Mono";font-size:10px}
</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="wrap"><div class="logo">NEKRUTENKO<i>/</i>LAB</div>
<nav><a href="#team">Team</a><a href="#products">Products</a><a href="#pubs">Publications</a><a href="#collab">Network</a><a href="#funding">Funding</a><a href="#contact">Contact</a></nav></div></header>
<div class="hero"><div class="wrap">
<div class="mono">Penn State · Est. 2003 · galaxyproject.org</div>
<h1>anLab<span>.</span></h1>
<p><b>anLab</b> — the <a href="https://scholar.google.com/citations?user=wiBQ9IQAAAAJ&hl=en" target="_blank" rel="noopener" style="color:var(--acc-text)">Anton Nekrutenko</a> lab at Penn State — is the birthplace of <b>Galaxy</b>: the open platform for accessible, reproducible, transparent computational biomedical research, built with collaborators worldwide. Current directions: pathogen &amp; host multiomics (BRC-Analytics), agentic AI for reproducible analysis, and large-genome assembly at scale.</p>
</div></div>
<div class="statband wrap" id="stats" style="padding:0"></div>
<div class="statnote wrap" id="statnote"></div>
<main class="wrap" id="main">
<section id="team"><div class="shead"><h2>The Team</h2><span class="num">01 / Biological ⇄ Computational</span></div>
<div class="tl" id="tl"></div><div class="axis"><span></span><div class="ticks" id="ticks"></div></div>
<div class="lg"><span><i class="dot" style="background:#d43d2a"></i>Biological</span><span><i class="dot" style="background:#e09b2d"></i>Bio→Comp</span><span><i class="dot" style="background:#5f8fb4"></i>Comp→Bio</span><span><i class="dot" style="background:#2a5fd4"></i>Computational</span></div></section>
<section id="products"><div class="shead"><h2>Products</h2><span class="num">02 / github.com/galaxyproject</span></div>
<div class="mono" style="margin-bottom:14px">A collaborative effort across the <a href="https://galaxyproject.org/usegalaxy/" target="_blank" rel="noopener" style="color:var(--acc-text)">usegalaxy.* consortium</a> and the <a href="https://github.com/orgs/galaxyproject/people" target="_blank" rel="noopener" style="color:var(--acc-text)">Galaxy community</a></div>
<div class="pgrid" id="pg"></div></section>
<section id="pubs"><div class="shead"><h2>Publications</h2><span class="num" id="pn">03</span></div>
<div class="mono" style="margin-bottom:14px">One cell = one paper · color = citations · click to open</div>
<div class="hm"><div class="hmgrid" id="hm"></div></div>
<div class="hscale"><span>0</span><div class="ramp" id="ramp"></div><span id="rampmax"></span><span>citations (log scale)</span></div>
<div class="mono" style="margin:40px 0 0">Most cited</div>
<div class="toplist" id="top"></div></section>
<section id="collab"><div class="shead"><h2>The Network</h2><span class="num">04 / Key collaborators</span></div>
<div class="cgrid" id="cg"></div>
<div class="mono" style="margin:36px 0 10px">Public usegalaxy.* servers</div>
<div class="wmap"><img src="world.svg" alt="World map of public Galaxy servers">
<a class="srv" style="left:18.5%;top:42.6%" href="https://usegalaxy.org" target="_blank" rel="noopener"><i></i>usegalaxy.org</a>
<a class="srv" style="left:25.4%;top:35.0%" href="https://usegalaxy.ca" target="_blank" rel="noopener"><i></i>.ca</a>
<a class="srv srv-l" style="left:48.8%;top:32.8%" href="https://usegalaxy.fr" target="_blank" rel="noopener"><i></i>.fr</a>
<a class="srv" style="left:50.2%;top:33.4%" href="https://usegalaxy.eu" target="_blank" rel="noopener"><i></i>.eu</a>
<a class="srv srv-l" style="left:91.4%;top:94.6%" href="https://usegalaxy.org.au" target="_blank" rel="noopener"><i></i>.org.au</a>
</div></section>
<section id="funding"><div class="shead"><h2>Funding</h2><span class="num" id="gn">05</span></div>
<div class="mono" style="margin-bottom:14px">Lab continuously funded since 2006 · active awards below (total project costs, PD/PI + Co-I) · <a href="https://reporter.nih.gov/search/koRNhs2Wy0akJuPp5EiYXA/projects" style="color:var(--acc-text)">NIH RePORTER ↗</a> · <a href="https://www.nsf.gov/awardsearch/simpleSearchResult?queryText=nekrutenko&ActiveAwards=true" style="color:var(--acc-text)">NSF Award Search ↗</a></div>
<div class="ggrid" id="gg"></div>
<div class="mono" style="margin-top:14px">Previously: 11 completed federal awards (2006–2025) + Beckman Young Investigator Award · additional support from the Huck Institutes of the Life Sciences</div></section>
</main>
<footer><div class="wrap" style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:20px;width:100%" id="contact">
<div><div class="logo">NEKRUTENKO<i>/</i>LAB</div><div class="mono" style="margin-top:8px"><a href="https://scholar.google.com/citations?user=wiBQ9IQAAAAJ&hl=en" target="_blank" rel="noopener" style="color:var(--acc-text)">Anton Nekrutenko</a> · Huck Chair in Genomics · Professor of Biochemistry &amp; Molecular Biology<br><a href="https://www.google.com/maps/search/?api=1&query=Wartik+Laboratory,+University+Park,+PA+16802" target="_blank" rel="noopener">505 Wartik Lab · University Park PA 16802</a> · <a href="tel:+18148269628">+1 814 826 9628</a> · <a href="mailto:aun1@psu.edu" style="color:var(--acc-text)">aun1@psu.edu</a><br>Interested in joining the lab? <a href="mailto:aun1@psu.edu?subject=Joining%20anLab" style="color:var(--acc-text)">Get in touch</a> · <a href="https://github.com/galaxyproject" style="color:var(--acc-text)">github.com/galaxyproject</a></div></div>
<div class="mono">__FOOT__</div>
</div></footer>
<div class="tip" id="tip" role="tooltip"></div>
<button id="totop" aria-label="Back to top">↑ TOP</button>
<script>
const D=__DATA__,S=D.stats;
const esc=x=>String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const AC={B:'#d43d2a',BC:'#e09b2d',CB:'#5f8fb4',C:'#2a5fd4'};
document.getElementById('stats').innerHTML=[
 [S.kui.users,'Registered users'],[S.kui.jobs,'Jobs run'],[S.kui.datasets,'Datasets created'],[S.kui.workflows,'Workflows built']]
 .map(x=>`<div><b>${x[0]}</b><small>${x[1]}</small></div>`).join('');
document.getElementById('statnote').textContent=`Impact across all public usegalaxy.* servers (as of ${S.kui.as_of}) · Galaxy used in 15,600+ papers from 9,300+ institutions in 163 countries`;
const flag=c=>c?`<img class="flg" src="flags/${c.toLowerCase()}.svg" alt="" aria-hidden="true">`:'';
const y0=S.yr_min,y1=S.yr_max,sp=Math.max(y1-y0,1);
document.getElementById('tl').innerHTML=D.people.map(p=>{
 const l=(p.start-y0)/sp*100,w=Math.max((p.end-p.start)/sp*100,1);
 const nm=p.name.replace(/\s*\([A-Z]{2}\)\s*$/,'');
 const yrs=`${p.start}–${p.now?'present':p.end}`;
 return `<div class="tlrow"><a class="nm" href="${p.pubmed}" title="${esc(p.role||nm)} · ${yrs}" aria-label="${esc(nm)}, ${esc(p.role||'lab member')}, ${yrs}">${flag(p.country)}${nm}</a><div class="tr"><div class="tlbar" style="left:${l}%;width:${w}%;background:${AC[p.aff]}"></div></div></div>`}).join('');
const tickYrs=[];for(let y=y0;y<=y1;y++)tickYrs.push(y);
document.getElementById('ticks').innerHTML=tickYrs.map(y=>`<span style="left:${(y-y0)/sp*100}%">${y}</span>`).join('');
const PRODUCTS=[
 {n:'Galaxy',img:'logos/galaxy.png',d:'The open, web-based platform for accessible, reproducible, and transparent computational research.',u:'https://galaxyproject.org'},
 {n:'Pulsar',img:'logos/pulsar.png',d:'Galaxy\u2019s distributed job execution engine — run jobs on remote compute, from clusters to clouds.',u:'https://github.com/galaxyproject/pulsar'},
 {n:'Planemo',img:'logos/planemo.png',d:'Command-line SDK for building, testing, and publishing Galaxy tools and workflows.',u:'https://github.com/galaxyproject/planemo'},
 {n:'IUC',img:'logos/iuc.svg',d:'The Intergalactic Utilities Commission — community-maintained, best-practice Galaxy tools.',u:'https://github.com/galaxyproject/tools-iuc'},
 {n:'IWC',img:'logos/iwc.png',d:'The Intergalactic Workflow Commission — curated, tested, versioned Galaxy workflows.',u:'https://iwc.galaxyproject.org/'},
 {n:'Orbit',img:'logos/orbit.svg',d:'Your AI co-scientist for Galaxy — chat, plan, run, and keep every step in a living notebook.',u:'https://galaxyproject.github.io/loom/'},
 {n:'BRC-Analytics',img:'logos/brc.svg',d:'Pathogen and host data analytics for the Bioinformatics Resource Centers — from raw reads to publication in a browser.',u:'https://brc-analytics.org'},
 {n:'GenomeArk2',img:'logos/genomeark2.svg',d:'Assembly and analysis of large eukaryotic genomes on public infrastructure, with the Vertebrate Genomes Project.',u:'https://genomeark2.org'},
 {n:'Foundry',img:'logos/foundry.svg',d:'The Galaxy Workflow Knowledge Base — casting community workflows into skills and actionable knowledge.',u:'https://galaxyproject.github.io/foundry/'},
];
document.getElementById('pg').innerHTML=PRODUCTS.map(p=>
 `<a class="pcard" href="${p.u}" target="_blank" rel="noopener"><span class="plogo"><img src="${p.img}" alt="${p.n} logo"></span>
 <b>${p.n}${p.badge?`<em>${p.badge}</em>`:''}</b><p>${p.d}</p><span class="gh">${p.u.replace('https://','')}</span></a>`).join('');
const byY={};D.pubs.forEach(p=>{(byY[p.year]=byY[p.year]||[]).push(p)});
const mx=Math.max(1,...D.pubs.map(p=>p.cites));
const heat=c=>{const t=Math.log(c+1)/Math.log(mx+1);
 return `hsl(${18-t*6} ${55+t*45}% ${88-t*55}%)`}
const tip=document.getElementById('tip');
const hmYears=[];for(let y=S.pub_yr_min;y<=S.pub_yr_max;y++)hmYears.push(y);
document.getElementById('hm').innerHTML=hmYears.map(y=>
 `<div><div class="hmcol">`+(byY[y]||[]).map(p=>
 `<a class="cell" href="${p.url}" target="_blank" rel="noopener" style="background:${heat(p.cites)}" aria-label="${esc(p.title)} — ${esc(p.journal)}, ${y}, ${p.cites.toLocaleString()} citations" data-t="${esc(p.title)}" data-j="${esc(p.journal)} · ${y} · ${p.cites.toLocaleString()} citations"></a>`).join('')+
 `</div><div class="hmyr">${y}</div></div>`).join('');
document.getElementById('ramp').style.background=`linear-gradient(90deg,${[0,.25,.5,.75,1].map(t=>heat(Math.round(Math.exp(t*Math.log(mx+1))-1))).join(',')})`;
document.getElementById('rampmax').textContent=mx.toLocaleString();
const showTip=(c,x,y)=>{tip.style.display='block';tip.innerHTML=esc(c.dataset.t)+'<br><small>'+esc(c.dataset.j)+'</small>';
 tip.style.left=Math.min(x,innerWidth-340)+'px';tip.style.top=y+'px';};
document.addEventListener('mousemove',e=>{const c=e.target.closest('.cell');
 if(c)showTip(c,e.clientX+14,e.clientY+16); else tip.style.display='none';});
document.addEventListener('focusin',e=>{const c=e.target.closest('.cell');
 if(c){const r=c.getBoundingClientRect();showTip(c,r.left,r.bottom+8);}});
document.addEventListener('focusout',()=>tip.style.display='none');
document.getElementById('pn').textContent='03 / '+S.npubs+' papers · '+S.cites.toLocaleString()+' citations';
document.getElementById('top').innerHTML=[...D.pubs].sort((a,b)=>b.cites-a.cites).slice(0,10).map(p=>
 `<div class="tp"><b>${p.cites.toLocaleString()}</b><div><a class="t" href="${p.url}" target="_blank" rel="noopener">${esc(p.title)}</a><small>${esc(p.journal)} · ${p.year}</small></div></div>`).join('');
const GRANTS=[
 {t:'An integrated platform for multiomic analyses of pathogen and host data using scalable public infrastructure (BRC-Analytics)',id:'U24AI183870',y:'2024–2029',amt:10216207,pd:1,ag:'NIH/NIAID'},
 {t:'Democratization of Data Analysis in Life Sciences Through Galaxy',id:'U24HG006620',y:'2012–2032',amt:30446748,pd:1,ag:'NIH/NHGRI'},
 {t:'Expanding the AnVIL (Analysis, Visualization, and Informatics Lab-space)',id:'U24HG010263',y:'2018–2028',amt:22712912,pd:0,ag:'NIH/NHGRI'},
 {t:'Developing a Cancer Galaxy Computational Workbench to Meet Emerging Cancer Data Analysis Needs',id:'U24CA284167',y:'2024–2029',amt:4200000,pd:0,ag:'NIH/NCI'},
 {t:'Hypothesis Testing using Phylogenies for the 21st century',id:'R01GM151683',y:'2024–2028',amt:1226505,pd:0,ag:'NIH/NIGMS'},
 {t:'The CFDE Cloud Workspace',id:'OT2OD037936',y:'2024–2029',amt:4852171,pd:0,ag:'NIH/OD'},
 {t:'Understanding biodiversity through a global platform for assembly and analysis of large genomes',id:'2419522',y:'2024–2028',amt:2963428,pd:1,ag:'NSF'},
 {t:'A k-mer-based search engine for sequencing databases',id:'2138585',y:'2022–2027',amt:800000,pd:0,ag:'NSF'},
];
const fmtM=a=>'$'+(a/1e6>=1?(a/1e6).toFixed(1)+'M':Math.round(a/1e3)+'K');
document.getElementById('gg').innerHTML=GRANTS.map(g=>
 `<div class="gcard"><div class="gtop"><span class="rolepill ${g.pd?'pd':'coi'}">${g.pd?'PD/PI':'Co-I'}</span><span class="mono" style="font-size:9.5px">${g.ag} · ${g.id}</span></div>
 <b>${fmtM(g.amt)}</b><p>${g.t}</p><span class="mono">${g.y}</span></div>`).join('');
document.getElementById('gn').textContent='05 / '+fmtM(GRANTS.reduce((a,g)=>a+g.amt,0))+' in active awards · funded since 2006';
document.getElementById('cg').innerHTML=D.collabs.map(c=>
 `<a href="${c.url}" target="_blank" rel="noopener"><b>${esc(c.name)}</b><span>${esc(c.inst)} — ${esc(c.loc)}</span>${c.memo?`<span class="memo">${esc(c.memo)}</span>`:''}</a>`).join('');
const toTop=document.getElementById('totop');
addEventListener('scroll',()=>{toTop.style.display=scrollY>600?'block':'none'},{passive:true});
toTop.onclick=()=>scrollTo({top:0,behavior:'smooth'});
const navLinks=[...document.querySelectorAll('nav a')];
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting)navLinks.forEach(a=>a.classList.toggle('active',a.hash==='#'+en.target.id))}),{rootMargin:'-30% 0px -60% 0px'});
document.querySelectorAll('section[id]').forEach(x=>io.observe(x));
</script></body></html>"""
E = E.replace('__FOOT__', FOOT_NOTE).replace('__BUILD__', BUILD_DATE).replace('__PY0__', str(min(pub_years)))
write('e-hybrid.html', E)

write('c-quiet.html', C)
write('d-swiss.html', D_)

INDEX = """<!doctype html><html><head><meta charset="utf-8"><title>Design previews</title>
<style>body{font:16px/1.6 system-ui;max-width:760px;margin:60px auto;padding:0 20px;background:#fafafa}
a.c{display:block;border:1px solid #ddd;border-radius:10px;padding:18px 22px;margin:14px 0;text-decoration:none;color:#111;background:#fff}
a.c:hover{border-color:#888}b{font-size:18px}p{margin:.3em 0 0;color:#666;font-size:14px}</style></head><body>
<h1>Nekrutenko Lab — design previews</h1>
<p style="color:#666">All four use the real lab data (27 people, 99 pubs + citations). Same content, four looks.</p>
<a class="c" href="e-hybrid.html" style="border-color:#ff4d00"><b>E · Hybrid (B+D) — current pick</b><p>B's structure (stat band, heatmap, network grid) with D's fonts: Inter Tight display + Spline Sans Mono labels.</p></a>
<a class="c" href="a-terminal.html"><b>A · Terminal</b><p>Dark, monospace, coral accent — herdr.dev-style dev aesthetic. Shell-prompt section headers, tenure bars, year-grouped pub list.</p></a>
<a class="c" href="b-industrial.html"><b>B · Industrial</b><p>varda.com energy: warm paper background, huge condensed uppercase display type, international-orange accent, stat band, citation heatmap grid.</p></a>
<a class="c" href="c-quiet.html"><b>C · Quiet</b><p>pi.dev-style minimal: narrow column, Inter + mono labels, auto light/dark with toggle, collapsible per-year publications.</p></a>
<a class="c" href="d-swiss.html"><b>D · Swiss</b><p>White, hard black rules, red accent, numbered sections. SVG people timeline + papers-per-year bars + sortable-feel table.</p></a>
</body></html>"""
open(f'{OUT}/index.html', 'w').write(INDEX)
open(f'{OUT}/404.html', 'w').write('''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Not found — Nekrutenko Lab</title>
<style>body{background:#f4f2ed;color:#141412;font:15px/1.65 "Inter Tight",system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0}
div{text-align:center}h1{font-weight:800;font-size:64px;letter-spacing:-.02em}h1 span{color:#ff4d00}
a{color:#d63a00;font-family:monospace;font-size:13px;text-transform:uppercase;letter-spacing:.1em;text-decoration:none}a:hover{text-decoration:underline}</style>
</head><body><div><h1>404<span>.</span></h1><p>This page drifted out of orbit.</p><a href="/">← back to the lab</a></div></body></html>''')
print('wrote index.html')

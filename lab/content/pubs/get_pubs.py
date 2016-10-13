#!/usr/bin/env python
# Based on https://gist.github.com/ehazlett/1104507
# A crude generator of a publication list in markdown

from Bio import Entrez
from Bio import Medline

MAX_COUNT = 100
TERM = 'Nekrutenko A'

Entrez.email = 'A.N.Other@example.com'
h = Entrez.esearch(db='pubmed', retmax=MAX_COUNT, term=TERM)
result = Entrez.read(h)
ids = result['IdList']
h = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text')

for record in Medline.parse(h):
	print "1. ",
	for au in record.get('AU'):
		print au,
	print "[%s](https://www.ncbi.nlm.nih.gov/pubmed/%s)" % (record.get('TI'),record.get('PMID')),
	print "*%s*" % record.get('TA'),
	print record.get('DP')[0:4],
	print "<div class='altmetric-embed' data-link-target='_blank' data-badge-type='donut' data-pmid='%s'></div>" % record.get('PMID')


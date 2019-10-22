---
title: "Effects of RT and PCR on mutation spectra"
date: 2019-10-10
author: Anton
tags: [PCR,RNA viruses,RT,mutation]
show_summary: false 
---

<div class="alert alert-warning" role="alert">
This is one of those "i-write-it-for-myself" notes about a paper that I really needed to understand
</div>

This is summary of [paper](http://dx.doi.org/10.1186/s12864-015-1456-x) by Orton et al. 2015 "Distinguishing low frequency mutations from RT-PCR and sequence errors in viral deep sequencing data"

In this manuscript the authors investigated the effects of various stages of sample preparation on the frequency of artifactual mutations. This is particularly interesting because it is based on re-sequencing on a single stranded RNA virus - a procedure that necessarily involves the Reverse Transcription (RT) step. It is therefore applicable to data generated for other (not necessarily single stranded RNA viruses such as HIV-1).

## Design

In this paper a cloned partial genome of the Foot and Mouth Disease Virus (FMDV) was sequenced using four strategies:

------

![](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs12864-015-1456-x/MediaObjects/12864_2015_1456_Fig2_HTML.gif)

<small><b>Fig. 2 |</b> Control sample processing and genome targets. (a) is a schematic of the four different control samples and the processing that each one has undergone. The numbers in brackets represent the number of PCR cycles used during PCR steps, the (2) label on reverse transcription denotes that there was a preceding transcription step. (b) is a schematic of the DNA plasmid used, the genomic regions each of the control samples covers, and the regions that are directly comparable between all controls and used for later analyses. From <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-015-1456-x">Orton et al. 2015</a></small>

------

These strategies were:

 1. <kbd>Seq</kbd> - sequencing linearized plasmid directly (immediately initiating library prep);
 2. <kbd>PCR-low</kbd> - amplifying linearized plasmid using two primer pairs in two 19-cycle PCR reactions and then initiating the library prep;
 3. <kbd>PCR-high</kbd> - diluting linearized plasmid and then amplifying it using two primer pairs in two 39-cycle PCR reactions and then initiating the library prep;
 4. <kbd>RT + PCR</kbd> - transcribing the linearized plasmid, reverse transcribing it and then amplifying it using two primer pairs in two 39-cycle PCR reactions and then initiating the library prep.

 The sequencing was done in Illumina GAIIx yielding 73 bp single-end reads (see [PRJEB8601](https://www.ncbi.nlm.nih.gov/bioproject/PRJEB860)).

## Results

### Mutation spectra

 The mutation spectra obtained from this experiment are show in Fig. 3 of the manuscript. One can see the increase in the number of processing steps shifts mutations towards higher frequency bins:

------

![](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs12864-015-1456-x/MediaObjects/12864_2015_1456_Fig3_HTML.gif)

<small><b>Fig. 3 |</b> Experimental data mutation spectra. The mutation spectrum of each of the experimental samples: Seq (blue), PCR-Low (red), PCR-High (green) and RT-PCR (purple) along with a real FMDV sample (black) from an infected cow (A5-7DPFC-PB in [18]). Each genome position considered is placed into a discrete bin based on its mismatch (to the reference) frequency. The x-axis represents the mismatch frequency of the bin whilst the y-axis represents the number of genome positions that are in that bin. Both axes are presented on a log10 scale. From <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-015-1456-x">Orton et al. 2015</a></small>

-------

### Variant frequency thresholds

This is where it gets interesting:


```
             25%     50%     75%     95%   100%
-------------------------------------------------
Seq.     0.0119% 0.0183% 0.0268% 0.0466% 0.276%
PCR-Low	 0.0261% 0.0371% 0.0518% 0.0793% 0.4074%
PCR-High 0.0323% 0.0457% 0.0623% 0.1004% 0.3755%
RT-PCR.  0.0368% 0.0526% 0.0793% 0.1403% 0.6571%
Real.    0.0309% 0.0510% 0.0916% 0.2113% 100
-------------------------------------------------
This table contains the 25th, median 50th, 75th, 95th and the maximum
100th percentiles of genome position mismatch frequencies in each of
the four samples.
```

The maximum observed mutation frequency for RT-PCR is 0.66% and according to Fig 3 (not Fig. 4 as stated in the text) the real genome starts to deviate from RT-PCR mutation frequency in 0.157-0.324 frequency bin. They further state:

>A total of 226 variants are observed above this threshold in the RT-PCR control sample, whilst 516 variants are observed in the real FMDV sample, 290 of which are therefore likely to be true. A threshold of 0.66% would correctly identify all the errors (100% specificity), but would only identify 32 of the 290 likely variants in the real FMDV sample as true. Lowering the threshold by half to 0.3% results in a doubling of the number of likely true variants identified to 75 at a relatively small cost with specificity only dropping to 99.86%. Whilst at a threshold of 0.15%, specificity drops to 96% with 226 errors falsely identified as true, but all 290 are the likely true variants also identified. It is important to note that a threshold will be dictated by the actual sample processing used and must also be taken in context. The fidelity of the enzymes used and the number of the PCR cycles will highly influence threshold setting, whilst the coverage of a genome position and the quality of it’s aligned reads will influence a threshold in a site specific manner.

and finally:

>From the data itself we identified a minimum frequency of ~0.5% above which one can be reasonably confident that an observed mutation is real. 
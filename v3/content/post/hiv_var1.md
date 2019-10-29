---
title: "Viral variation: a Galaxy tutorial"
date: 2019-10-29
author: Anton
tags: [Galaxy,RNA viruses,HIV]
show_summary: false 
---

<div class="alert alert-warning" role="alert">
This tutorials will be converted into an official Galaxy Training Material
</div>

## Objective

Learn to upload, process, and analyze complex multi-sample datasets. Such datasets are typical in today's biomedical research. Here we will analyze data from [Jair et al. 2019](https://doi.org/10.1371/journal.pone.0214820) manuscript. 

## The Galaxy instance

TFor this tutorial we will use a Galaxy instance specifically configured for running workshops (right click on the following link to open it in a new window or browser tab): https://workshop.usegalaxy.org

## The data

Jair et al. 2019](https://doi.org/10.1371/journal.pone.0214820) generated 68 datasets ([PRJNA517147](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA517147)). For the purposes of this tutorial we produced a downsampled version of these data available at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3519268.svg)](https://doi.org/10.5281/zenodo.3519268). 

Fr this tutorial we will use a subset consisting of these datasets:

```text
SRR8525909
SRR8525905
SRR8525896
SRR8525889
```

## Uploading the data

To upload the data we will use the [rule builder](https://galaxyproject.github.io/training-material/topics/galaxy-data-manipulation/tutorials/processing-many-samples-at-once/tutorial.html) functionality.

### Create manifest for upload

Locate and click the upload button in the upper left corner of the Galaxy interface

---------

![](/lab_site/images/var1_upload.png)
<small>Click upload button</small>

-----

Select **Rule-based** tab within the upload interface:

-----

![](/lab_site/images/var1_rb1.png)
<small>Click on the <b>Rule-based</b> tab</small>
![](/lab_site/images/var1_rb2.png)
<small>Select *Colections* in the **Upload data as:** dropdown:</small>

------
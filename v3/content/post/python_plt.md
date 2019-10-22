---
title: "Getting interested in Python"
date: 2019-10-09
author: Anton
tags: ["python", "plotting","TnSeq"]
show_summary: false 
---

by AN

----------

<div class="alert alert-warning" role="alert">
This lecture draws extensively from <a href="http://seaborn.pydata.org/tutorial.html">Seaborn tutorials</a>. The best way to run it, is to use <a href="https://colab.research.google.com/">Collaboratory</a> from Google.
</div>

{{< highlight bash >}}
# Colaboratory has an old version of seaborn, so let's upgrade 
!pip install seaborn --upgrade
{{< / highlight >}}

{{< highlight py3 >}}
import seaborn as sns
sns.set(style="ticks")
import pandas as pd
import matplotlib.pyplot as plt
{{< / highlight >}}


# Why plotting?
We will use [Ascombe's quartet](https://en.wikipedia.org/wiki/Anscombe%27s_quartet) build in into Seaborn to answer this questions


{{< highlight py3 >}}
# Load the example dataset for Anscombe's quartet
df = sns.load_dataset("anscombe")
df
{{< / highlight >}}

{{< highlight py3 >}}
   dataset     x      y
0        I  10.0   8.04
1        I   8.0   6.95
2        I  13.0   7.58
3        I   9.0   8.81
4        I  11.0   8.33
5        I  14.0   9.96
6        I   6.0   7.24
7        I   4.0   4.26
8        I  12.0  10.84
9        I   7.0   4.82
10       I   5.0   5.68
11      II  10.0   9.14
12      II   8.0   8.14
13      II  13.0   8.74
14      II   9.0   8.77
15      II  11.0   9.26
16      II  14.0   8.10
17      II   6.0   6.13
18      II   4.0   3.10
19      II  12.0   9.13
20      II   7.0   7.26
21      II   5.0   4.74
22     III  10.0   7.46
23     III   8.0   6.77
24     III  13.0  12.74
25     III   9.0   7.11
26     III  11.0   7.81
27     III  14.0   8.84
28     III   6.0   6.08
29     III   4.0   5.39
30     III  12.0   8.15
31     III   7.0   6.42
32     III   5.0   5.73
33      IV   8.0   6.58
34      IV   8.0   5.76
35      IV   8.0   7.71
36      IV   8.0   8.84
37      IV   8.0   8.47
38      IV   8.0   7.04
39      IV   8.0   5.25
40      IV  19.0  12.50
41      IV   8.0   5.56
42      IV   8.0   7.91
43      IV   8.0   6.89
{{< / highlight >}}

{{< highlight py3 >}}
df.groupby('dataset').describe()
{{< / highlight >}}


{{< highlight py3 >}}
            x                                               y                                                    
        count mean       std  min  25%  50%   75%   max count      mean       std   min    25%   50%   75%    max
dataset                                                                                                          
I        11.0  9.0  3.316625  4.0  6.5  9.0  11.5  14.0  11.0  7.500909  2.031568  4.26  6.315  7.58  8.57  10.84
II       11.0  9.0  3.316625  4.0  6.5  9.0  11.5  14.0  11.0  7.500909  2.031657  3.10  6.695  8.14  8.95   9.26
III      11.0  9.0  3.316625  4.0  6.5  9.0  11.5  14.0  11.0  7.500000  2.030424  5.39  6.250  7.11  7.98  12.74
IV       11.0  9.0  3.316625  8.0  8.0  8.0   8.0  19.0  11.0  7.500909  2.030579  5.25  6.170  7.04  8.19  12.50
{{< / highlight >}}


{{< highlight py3 >}}
# Show the results of a linear regression within each dataset
sns.lmplot(x="x", y="y", col="dataset", hue="dataset", data=df,
           col_wrap=2
           )
{{< / highlight >}}

![png](/images/output_7_1.png)


## Let's look at TnSeq data 

<div class="alert alert-warning" role="alert">
If you are not familiar with TnSeq data, begin by reading <a href="http://dx.doi.org/10.1186/s12864-015-1361-3">Santiago et al. 2015</a>.
</div>


{{< highlight bash >}}
%%bash
wget https://nekrut.github.io/BMMB554/tnseq_untreated.txt.gz
wget https://nekrut.github.io/BMMB554/ta_gc.txt
{{< / highlight >}}

{{< highlight py3 >}}
data_file = 'tnseq_untreated.txt.gz'
{{< / highlight >}}


{{< highlight py3 >}}
# Process tnseq_untreated.txt.gz to correctly parse gene names

import os
f = open('data.txt','w')

with os.popen('gunzip -c {}'.format(data_file)) as stream:
  for line in stream:
    if line.split( '\t' )[7].startswith( '.' ):
      f.write( '{}\t{}\n'.format( '\t'.join( line.split( '\t' )[:7] ) , 'intergenic'  ) )
    elif line.split( '\t' )[7].startswith( 'ID' ):
      f.write( '{}\t{}\n'.format( '\t'.join( line.split( '\t' )[:7] ) , line.split( '\t' )[7].split(';')[0][3:] ) )
f.close()
{{< / highlight >}}


{{< highlight py3 >}}
# Reading TnSeq data into a dataframe

tnseq = pd.read_table('data.txt', header=None, names=['pos','blunt','cap','dual','erm','pen','tuf','gene'])
{{< / highlight >}}

{{< highlight py3 >}}
# Reading GC content data

gc = pd.read_table('ta_gc.txt', header=None, names=['pos','gc'])
{{< / highlight >}}

{{< highlight py3 >}}
tnseq.head()
{{< / highlight >}}

{{< highlight py3 >}}
       pos  blunt  cap  dual  erm  pen  tuf        gene
0  2400002    0.0  0.0   1.0  0.0  0.0  1.0  intergenic
1  2400004    1.0  0.0   5.0  0.0  0.0  1.0  intergenic
2  2400006    1.0  0.0   5.0  1.0  0.0  1.0  intergenic
3  2400009    2.0  2.0   8.0  1.0  0.0  0.0  intergenic
4  2400029    6.0  1.0   0.0  1.0  0.0  1.0  intergenic
{{< / highlight >}}

{{< highlight py3 >}}
gc.head()
{{< / highlight >}}

{{< highlight py3 >}}
   pos        gc
0    4  0.339286
1   10  0.354839
2   16  0.367647
3   42  0.372340
4   79  0.303922
{{< / highlight >}}


{{< highlight py3 >}}
# Join tnseq and GC content data together

tn_gc = tnseq.merge(gc,left_on='pos',right_on='pos',how='left')
{{< / highlight >}}


{{< highlight py3 >}}
tn_gc.head()
{{< / highlight >}}

{{< highlight py3 >}}
       pos  blunt  cap  dual  erm  pen  tuf        gene        gc
0  2400002    0.0  0.0   1.0  0.0  0.0  1.0  intergenic  0.225490
1  2400004    1.0  0.0   5.0  0.0  0.0  1.0  intergenic  0.225490
2  2400006    1.0  0.0   5.0  1.0  0.0  1.0  intergenic  0.215686
3  2400009    2.0  2.0   8.0  1.0  0.0  0.0  intergenic  0.225490
4  2400029    6.0  1.0   0.0  1.0  0.0  1.0  intergenic  0.215686
{{< / highlight >}}


{{< highlight py3 >}}
# This is the list of column containing construct data

list(tn_gc)[1:7]
{{< / highlight >}}

{{< highlight py3 >}}
    ['blunt', 'cap', 'dual', 'erm', 'pen', 'tuf']
{{< / highlight >}}


## "Melting data"

Visualization work much better with so called [narrow data](https://en.wikipedia.org/wiki/Wide_and_narrow_data). To convert our existing dataset into "narrow" form we will melt it down:

![](https://pandas.pydata.org/pandas-docs/stable/_images/reshaping_melt.png)

(This image and a much more detailed explanation of dataframe reshaping can be found in [Pandas Doc Pages](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)).


{{< highlight py3 >}}
# Melt tn_gc in tdf

tdf = pd.melt(tn_gc, id_vars=['pos','gc','gene'],value_vars=list(tn_gc)[1:7],var_name="construct",value_name="count").sort_values(by='pos')
{{< / highlight >}}


{{< highlight py3 >}}
tdf.head()
{{< / highlight >}}

{{< highlight py3 >}}
         pos        gc        gene construct  count
406329     4  0.339286  intergenic       cap    1.0
1486729    4  0.339286  intergenic       tuf    0.0
1216629    4  0.339286  intergenic       pen    0.0
676429     4  0.339286  intergenic      dual    0.0
136229     4  0.339286  intergenic     blunt    0.0
{{< / highlight >}}


{{< highlight py3 >}}
# Set genic and non-genic categories

tdf.loc[tdf['gene'] == 'intergenic','genic'] = 'no'
tdf.loc[tdf['gene'] != 'intergenic','genic'] = 'yes'
{{< / highlight >}}


{{< highlight py3 >}}
tdf.head()
{{< / highlight >}}

{{< highlight py3 >}}
        pos        gc        gene construct  count genic
406329     4  0.339286  intergenic       cap    1.0    no
1486729    4  0.339286  intergenic       tuf    0.0    no
1216629    4  0.339286  intergenic       pen    0.0    no
676429     4  0.339286  intergenic      dual    0.0    no
136229     4  0.339286  intergenic     blunt    0.0    no
{{< / highlight >}}


# Visualizing the distribution of a dataset
When dealing with a set of data, often the first thing you’ll want to do is get a sense for how the variables are distributed. This chapter of the tutorial will give a brief introduction to some of the tools in seaborn for examining univariate and bivariate distributions. You may also want to look at the categorical plots chapter for examples of functions that make it easy to compare the distribution of a variable across levels of other variables.

These examples are taken from [official seaborn tutorials](https://seaborn.pydata.org/tutorial.html).

## Plotting univariate distributions
The most convenient way to take a quick look at a univariate distribution in seaborn is the [`distplot()`](https://seaborn.pydata.org/generated/seaborn.distplot.html#seaborn.distplot) function. By default, this will draw a [histogram](https://en.wikipedia.org/wiki/Histogram) and fit a kernel density estimate [KDE](https://en.wikipedia.org/wiki/Kernel_density_estimation)

{{< highlight py3 >}}
# Distribution of GC content 

sns.distplot(tdf['gc'])
{{< / highlight >}}

![png](/images/output_26_1.png)


{{< highlight py3 >}}
# Distribution of read counts is a bit gloomy

sns.distplot(tdf['count'])
{{< / highlight >}}

![png](/images/output_27_1.png)

{{< highlight py3 >}}
# We can narrow it down

sns.distplot(tdf['count'][(tdf['count']>6)&(tdf['count']<100)])
{{< / highlight >}}

![png](/images/output_28_1.png)

{{< highlight py3 >}}
# Or increase the number of bins and change the scale

g=sns.distplot(tdf['count'],bins=10000)
g.set(xscale="log")
{{< / highlight >}}

![png](/images/output_29_1.png)


{{< highlight py3 >}}
# And also get rif of zero counts

g=sns.distplot(tdf['count'][tdf['count']>0],bins=10000)
g.set(xscale="log")

{{< / highlight >}}

![png](/images/output_30_1.png)

{{< highlight py3 >}}
# Plotting the relationship between GC count and insertion frequency

sns.jointplot(x="count", y="gc", data=tdf[tdf['count']>10]);
{{< / highlight >}}

![png](/images/output_31_0.png)


# Visualizing statistical relationships
Statistical analysis is a process of understanding how variables in a dataset relate to each other and how those relationships depend on other variables. Visualization can be a core component of this process because, when data are visualized properly, the human visual system can see trends and patterns that indicate a relationship.

We will discuss three seaborn functions in this tutorial. The one we will use most is [ `relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot). This is a [figure-level function](https://seaborn.pydata.org/introduction.html#intro-func-types) for visualizing statistical relationships using two common approaches: scatter plots and line plots. [ `relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot) combines a [FacetGrid](https://seaborn.pydata.org/generated/seaborn.FacetGrid.html#seaborn.FacetGrid) with one of two axes-level functions:

 - [`scatterplot()`](https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot) (with `kind="scatter"`; the default)
 - [`lineplot()`](https://seaborn.pydata.org/generated/seaborn.lineplot.html#seaborn.lineplot) (with `kind="line"`)
 
As we will see, these functions can be quite illuminating because they use simple and easily-understood representations of data that can nevertheless represent complex dataset structures. They can do so because they plot two-dimensional graphics that can be enhanced by mapping up to three additional variables using the semantics of hue, size, and style.

## Relating variables with scatter plots
The scatter plot is a mainstay of statistical visualization. It depicts the joint distribution of two variables using a cloud of points, where each point represents an observation in the dataset. This depiction allows the eye to infer a substantial amount of information about whether there is any meaningful relationship between them.

There are several ways to draw a scatter plot in seaborn. The most basic, which should be used when both variables are numeric, is the [`scatterplot()`](https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot) function. The [`scatterplot()`](https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot) is the default kind in [`relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot) (it can also be forced by setting `kind="scatter"`):


{{< highlight py3 >}}
sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100])
{{< / highlight >}}

![png](/images/output_35_1.png)

While the points are plotted in two dimensions, another dimension can be added to the plot by coloring the points according to a third variable. In seaborn, this is referred to as using a “hue semantic”, because the color of the point gains meaning:

{{< highlight py3 >}}
sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100],hue='construct')
{{< / highlight >}}

![png](//images/output_37_1.png)

{{< highlight py3 >}}
g = sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100],hue='construct')
g.set(yscale="log")
{{< / highlight >}}

![png](/images/output_38_1.png)

To emphasize the difference between the classes, and to improve accessibility, you can use a different marker style for each class:

{{< highlight py3 >}}
sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100],hue='construct',style='genic')
{{< / highlight >}}

![png](/images/output_40_1.png)


# Categorical scatterplots

The default representation of the data in [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot) uses a scatterplot. There are actually two different categorical scatter plots in seaborn. They take different approaches to resolving the main challenge in representing categorical data with a scatter plot, which is that all of the points belonging to one category would fall on the same position along the axis corresponding to the categorical variable. The approach used by [`stripplot()`](https://seaborn.pydata.org/generated/seaborn.stripplot.html#seaborn.stripplot), which is the default “kind” in [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot) is to adjust the positions of points on the categorical axis with a small amount of random “jitter”:


{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100]);
{{< / highlight >}}

![png](/images/output_43_0.png)

The `jitter` parameter controls the magnitude of jitter or disables it altogether:

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100],jitter=False);
{{< / highlight >}}

![png](/images/output_45_0.png)

The second approach adjusts the points along the categorical axis using an algorithm that prevents them from overlapping. It can give a better representation of the distribution of observations, although it only works well for relatively small datasets. This kind of plot is sometimes called a “beeswarm” and is drawn in seaborn by [`swarmplot()`](https://seaborn.pydata.org/generated/seaborn.swarmplot.html#seaborn.swarmplot), which is activated by setting `kind="swarm"` in [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot):

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100],kind="swarm")
{{< / highlight >}}

![png](/images/output_47_0.png)

Similar to the relational plots, it’s possible to add another dimension to a categorical plot by using a `hue` semantic. (The categorical plots do not currently support `size` or `style` semantics). Each different categorical plotting function handles the `hue` semantic differently. For the scatter plots, it is only necessary to change the color of the points:

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100],kind="swarm",hue='genic')
{{< / highlight >}}

![png](/images/output_49_1.png)

We’ve referred to the idea of “categorical axis”. In these examples, that’s always corresponded to the horizontal axis. But it’s often helpful to put the categorical variable on the vertical axis (particularly when the category names are relatively long or there are many categories). To do this, swap the assignment of variables to axes:

{{< highlight py3 >}}
sns.catplot(x="count", y="construct", data=tdf[tdf['count']>100],kind="swarm",hue='genic')
{{< / highlight >}}

![png](/images/output_51_1.png)

## Distributions of observations within categories
As the size of the dataset grows,, categorical scatter plots become limited in the information they can provide about the distribution of values within each category. When this happens, there are several approaches for summarizing the distributional information in ways that facilitate easy comparisons across the category levels.

### Boxplots
The first is the familiar [`boxplot()`](https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot). This kind of plot shows the three quartile values of the distribution along with extreme values. The “whiskers” extend to points that lie within 1.5 IQRs of the lower and upper quartile, and then observations that fall outside this range are displayed independently. This means that each value in the boxplot corresponds to an actual observation in the data.


{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="box")
{{< / highlight >}}

![png](/images/output_54_1.png)

When adding a `hue` semantic, the box for each level of the semantic variable is moved along the categorical axis so they don’t overlap:

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="box",hue='genic')
{{< / highlight >}}

![png](/images/output_56_1.png)

A related function, [`boxenplot()`](https://seaborn.pydata.org/generated/seaborn.boxenplot.html#seaborn.boxenplot), draws a plot that is similar to a box plot but optimized for showing more information about the shape of the distribution. It is best suited for larger datasets:

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="boxen")
{{< / highlight >}}

![png](/images/output_58_1.png)


### Violinplots
A different approach is a [`violinplot()`](https://seaborn.pydata.org/generated/seaborn.violinplot.html#seaborn.violinplot), which combines a boxplot with the kernel density estimation procedure:

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="violin")
{{< / highlight >}}

![png](/images/output_60_1.png)

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="violin",hue='genic')
{{< / highlight >}}

![png](/images/output_61_1.png)

It’s also possible to “split” the violins when the hue parameter has only two levels, which can allow for a more efficient use of space:

{{< highlight py3 >}}
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="violin",hue='genic',split=True)
{{< / highlight >}}

![png](/images/output_63_1.png)


Finally, there are several options for the plot that is drawn on the interior of the violins, including ways to show each individual observation instead of the summary boxplot values:

## Statistical estimation within categories
For other applications, rather than showing the distribution within each category, you might want to show an estimate of the central tendency of the values. Seaborn has two main ways to show this information. Importantly, the basic API for these functions is identical to that for the ones discussed above.

### Bar plots
A familiar style of plot that accomplishes this goal is a bar plot. In seaborn, the [`barplot()`](https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot) function operates on a full dataset and applies a function to obtain the estimate (taking the mean by default). When there are multiple observations in each category, it also uses bootstrapping to compute a confidence interval around the estimate and plots that using error bars:

{{< highlight py3 >}}
sns.catplot(x="construct",y="count",hue="genic",kind="bar",data=tdf)
{{< / highlight >}}

![png](/images/output_67_1.png)

A special case for the bar plot is when you want to show the number of observations in each category rather than computing a statistic for a second variable. This is similar to a histogram over a categorical, rather than quantitative, variable. In seaborn, it’s easy to do so with the [`countplot()`](https://seaborn.pydata.org/generated/seaborn.countplot.html#seaborn.countplot) function:


{{< highlight py3 >}}
sns.catplot(x="genic",kind="count",data=tdf)
{{< / highlight >}}

![png](/images/output_69_1.png)

## Showing multiple relationships with facets
Just like [`relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot), the fact that [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot) is built on a [`FacetGrid`](https://seaborn.pydata.org/generated/seaborn.FacetGrid.html#seaborn.FacetGrid) means that it is easy to add faceting variables to visualize higher-dimensional relationships:

{{< highlight py3 >}}
sns.catplot(x="genic", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<1000)],kind="boxen",col='construct',col_wrap=2)
{{< / highlight >}}

![png](/images/output_71_1.png)

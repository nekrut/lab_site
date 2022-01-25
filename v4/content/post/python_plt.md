---
title: "Getting interested in Python"
date: 2019-10-09
author: Anton
tags: [python, plotting]
show_summary: false 
---

{{< background "warning" >}}
This lecture draws extensively from Seaborn tutorials.
{{< /background >}}


# A primer of plotting with Python


```python
# Colaboratory has an old version of seaborn, so let's upgrade 
!pip install seaborn --upgrade
```

    Requirement already up-to-date: seaborn in /usr/local/lib/python3.6/dist-packages (0.9.0)
    Requirement already satisfied, skipping upgrade: numpy>=1.9.3 in /usr/local/lib/python3.6/dist-packages (from seaborn) (1.16.5)
    Requirement already satisfied, skipping upgrade: pandas>=0.15.2 in /usr/local/lib/python3.6/dist-packages (from seaborn) (0.24.2)
    Requirement already satisfied, skipping upgrade: scipy>=0.14.0 in /usr/local/lib/python3.6/dist-packages (from seaborn) (1.3.1)
    Requirement already satisfied, skipping upgrade: matplotlib>=1.4.3 in /usr/local/lib/python3.6/dist-packages (from seaborn) (3.0.3)
    Requirement already satisfied, skipping upgrade: python-dateutil>=2.5.0 in /usr/local/lib/python3.6/dist-packages (from pandas>=0.15.2->seaborn) (2.5.3)
    Requirement already satisfied, skipping upgrade: pytz>=2011k in /usr/local/lib/python3.6/dist-packages (from pandas>=0.15.2->seaborn) (2018.9)
    Requirement already satisfied, skipping upgrade: pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.1 in /usr/local/lib/python3.6/dist-packages (from matplotlib>=1.4.3->seaborn) (2.4.2)
    Requirement already satisfied, skipping upgrade: cycler>=0.10 in /usr/local/lib/python3.6/dist-packages (from matplotlib>=1.4.3->seaborn) (0.10.0)
    Requirement already satisfied, skipping upgrade: kiwisolver>=1.0.1 in /usr/local/lib/python3.6/dist-packages (from matplotlib>=1.4.3->seaborn) (1.1.0)
    Requirement already satisfied, skipping upgrade: six>=1.5 in /usr/local/lib/python3.6/dist-packages (from python-dateutil>=2.5.0->pandas>=0.15.2->seaborn) (1.12.0)
    Requirement already satisfied, skipping upgrade: setuptools in /usr/local/lib/python3.6/dist-packages (from kiwisolver>=1.0.1->matplotlib>=1.4.3->seaborn) (41.2.0)



```python
import seaborn as sns
sns.set(style="ticks")

import pandas as pd
import matplotlib.pyplot as plt
```

# Why plotting?
We will use [Ascombe's quartet](https://en.wikipedia.org/wiki/Anscombe%27s_quartet) build in into Seaborn to answer this questions


```python
# Load the example dataset for Anscombe's quartet
df = sns.load_dataset("anscombe")
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>dataset</th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>I</td>
      <td>10.0</td>
      <td>8.04</td>
    </tr>
    <tr>
      <th>1</th>
      <td>I</td>
      <td>8.0</td>
      <td>6.95</td>
    </tr>
    <tr>
      <th>2</th>
      <td>I</td>
      <td>13.0</td>
      <td>7.58</td>
    </tr>
    <tr>
      <th>3</th>
      <td>I</td>
      <td>9.0</td>
      <td>8.81</td>
    </tr>
    <tr>
      <th>4</th>
      <td>I</td>
      <td>11.0</td>
      <td>8.33</td>
    </tr>
    <tr>
      <th>5</th>
      <td>I</td>
      <td>14.0</td>
      <td>9.96</td>
    </tr>
    <tr>
      <th>6</th>
      <td>I</td>
      <td>6.0</td>
      <td>7.24</td>
    </tr>
    <tr>
      <th>7</th>
      <td>I</td>
      <td>4.0</td>
      <td>4.26</td>
    </tr>
    <tr>
      <th>8</th>
      <td>I</td>
      <td>12.0</td>
      <td>10.84</td>
    </tr>
    <tr>
      <th>9</th>
      <td>I</td>
      <td>7.0</td>
      <td>4.82</td>
    </tr>
    <tr>
      <th>10</th>
      <td>I</td>
      <td>5.0</td>
      <td>5.68</td>
    </tr>
    <tr>
      <th>11</th>
      <td>II</td>
      <td>10.0</td>
      <td>9.14</td>
    </tr>
    <tr>
      <th>12</th>
      <td>II</td>
      <td>8.0</td>
      <td>8.14</td>
    </tr>
    <tr>
      <th>13</th>
      <td>II</td>
      <td>13.0</td>
      <td>8.74</td>
    </tr>
    <tr>
      <th>14</th>
      <td>II</td>
      <td>9.0</td>
      <td>8.77</td>
    </tr>
    <tr>
      <th>15</th>
      <td>II</td>
      <td>11.0</td>
      <td>9.26</td>
    </tr>
    <tr>
      <th>16</th>
      <td>II</td>
      <td>14.0</td>
      <td>8.10</td>
    </tr>
    <tr>
      <th>17</th>
      <td>II</td>
      <td>6.0</td>
      <td>6.13</td>
    </tr>
    <tr>
      <th>18</th>
      <td>II</td>
      <td>4.0</td>
      <td>3.10</td>
    </tr>
    <tr>
      <th>19</th>
      <td>II</td>
      <td>12.0</td>
      <td>9.13</td>
    </tr>
    <tr>
      <th>20</th>
      <td>II</td>
      <td>7.0</td>
      <td>7.26</td>
    </tr>
    <tr>
      <th>21</th>
      <td>II</td>
      <td>5.0</td>
      <td>4.74</td>
    </tr>
    <tr>
      <th>22</th>
      <td>III</td>
      <td>10.0</td>
      <td>7.46</td>
    </tr>
    <tr>
      <th>23</th>
      <td>III</td>
      <td>8.0</td>
      <td>6.77</td>
    </tr>
    <tr>
      <th>24</th>
      <td>III</td>
      <td>13.0</td>
      <td>12.74</td>
    </tr>
    <tr>
      <th>25</th>
      <td>III</td>
      <td>9.0</td>
      <td>7.11</td>
    </tr>
    <tr>
      <th>26</th>
      <td>III</td>
      <td>11.0</td>
      <td>7.81</td>
    </tr>
    <tr>
      <th>27</th>
      <td>III</td>
      <td>14.0</td>
      <td>8.84</td>
    </tr>
    <tr>
      <th>28</th>
      <td>III</td>
      <td>6.0</td>
      <td>6.08</td>
    </tr>
    <tr>
      <th>29</th>
      <td>III</td>
      <td>4.0</td>
      <td>5.39</td>
    </tr>
    <tr>
      <th>30</th>
      <td>III</td>
      <td>12.0</td>
      <td>8.15</td>
    </tr>
    <tr>
      <th>31</th>
      <td>III</td>
      <td>7.0</td>
      <td>6.42</td>
    </tr>
    <tr>
      <th>32</th>
      <td>III</td>
      <td>5.0</td>
      <td>5.73</td>
    </tr>
    <tr>
      <th>33</th>
      <td>IV</td>
      <td>8.0</td>
      <td>6.58</td>
    </tr>
    <tr>
      <th>34</th>
      <td>IV</td>
      <td>8.0</td>
      <td>5.76</td>
    </tr>
    <tr>
      <th>35</th>
      <td>IV</td>
      <td>8.0</td>
      <td>7.71</td>
    </tr>
    <tr>
      <th>36</th>
      <td>IV</td>
      <td>8.0</td>
      <td>8.84</td>
    </tr>
    <tr>
      <th>37</th>
      <td>IV</td>
      <td>8.0</td>
      <td>8.47</td>
    </tr>
    <tr>
      <th>38</th>
      <td>IV</td>
      <td>8.0</td>
      <td>7.04</td>
    </tr>
    <tr>
      <th>39</th>
      <td>IV</td>
      <td>8.0</td>
      <td>5.25</td>
    </tr>
    <tr>
      <th>40</th>
      <td>IV</td>
      <td>19.0</td>
      <td>12.50</td>
    </tr>
    <tr>
      <th>41</th>
      <td>IV</td>
      <td>8.0</td>
      <td>5.56</td>
    </tr>
    <tr>
      <th>42</th>
      <td>IV</td>
      <td>8.0</td>
      <td>7.91</td>
    </tr>
    <tr>
      <th>43</th>
      <td>IV</td>
      <td>8.0</td>
      <td>6.89</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.groupby('dataset').describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="8" halign="left">x</th>
      <th colspan="8" halign="left">y</th>
    </tr>
    <tr>
      <th></th>
      <th>count</th>
      <th>mean</th>
      <th>std</th>
      <th>min</th>
      <th>25%</th>
      <th>50%</th>
      <th>75%</th>
      <th>max</th>
      <th>count</th>
      <th>mean</th>
      <th>std</th>
      <th>min</th>
      <th>25%</th>
      <th>50%</th>
      <th>75%</th>
      <th>max</th>
    </tr>
    <tr>
      <th>dataset</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>I</th>
      <td>11.0</td>
      <td>9.0</td>
      <td>3.316625</td>
      <td>4.0</td>
      <td>6.5</td>
      <td>9.0</td>
      <td>11.5</td>
      <td>14.0</td>
      <td>11.0</td>
      <td>7.500909</td>
      <td>2.031568</td>
      <td>4.26</td>
      <td>6.315</td>
      <td>7.58</td>
      <td>8.57</td>
      <td>10.84</td>
    </tr>
    <tr>
      <th>II</th>
      <td>11.0</td>
      <td>9.0</td>
      <td>3.316625</td>
      <td>4.0</td>
      <td>6.5</td>
      <td>9.0</td>
      <td>11.5</td>
      <td>14.0</td>
      <td>11.0</td>
      <td>7.500909</td>
      <td>2.031657</td>
      <td>3.10</td>
      <td>6.695</td>
      <td>8.14</td>
      <td>8.95</td>
      <td>9.26</td>
    </tr>
    <tr>
      <th>III</th>
      <td>11.0</td>
      <td>9.0</td>
      <td>3.316625</td>
      <td>4.0</td>
      <td>6.5</td>
      <td>9.0</td>
      <td>11.5</td>
      <td>14.0</td>
      <td>11.0</td>
      <td>7.500000</td>
      <td>2.030424</td>
      <td>5.39</td>
      <td>6.250</td>
      <td>7.11</td>
      <td>7.98</td>
      <td>12.74</td>
    </tr>
    <tr>
      <th>IV</th>
      <td>11.0</td>
      <td>9.0</td>
      <td>3.316625</td>
      <td>8.0</td>
      <td>8.0</td>
      <td>8.0</td>
      <td>8.0</td>
      <td>19.0</td>
      <td>11.0</td>
      <td>7.500909</td>
      <td>2.030579</td>
      <td>5.25</td>
      <td>6.170</td>
      <td>7.04</td>
      <td>8.19</td>
      <td>12.50</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Show the results of a linear regression within each dataset
sns.lmplot(x="x", y="y", col="dataset", hue="dataset", data=df,
           col_wrap=2
           )
```




    <seaborn.axisgrid.FacetGrid at 0x7f48c69e4a58>




![png](/lab_site/images/output_7_1.png)


## Let's look at TnSeq data again


```bash
%%bash
wget https://nekrut.github.io/BMMB554/tnseq_untreated.txt.gz
wget https://nekrut.github.io/BMMB554/ta_gc.txt
```

    --2019-10-09 12:53:42--  https://nekrut.github.io/BMMB554/tnseq_untreated.txt.gz
    Resolving nekrut.github.io (nekrut.github.io)... 185.199.109.153, 185.199.111.153, 185.199.110.153, ...
    Connecting to nekrut.github.io (nekrut.github.io)|185.199.109.153|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 2012967 (1.9M) [application/gzip]
    Saving to: ‘tnseq_untreated.txt.gz’
    
         0K .......... .......... .......... .......... ..........  2% 3.34M 1s
        50K .......... .......... .......... .......... ..........  5% 6.68M 0s
       100K .......... .......... .......... .......... ..........  7% 78.0M 0s
       150K .......... .......... .......... .......... .......... 10% 77.4M 0s
       200K .......... .......... .......... .......... .......... 12% 7.39M 0s
       250K .......... .......... .......... .......... .......... 15% 82.6M 0s
       300K .......... .......... .......... .......... .......... 17% 88.7M 0s
       350K .......... .......... .......... .......... .......... 20% 8.46M 0s
       400K .......... .......... .......... .......... .......... 22% 34.1M 0s
       450K .......... .......... .......... .......... .......... 25% 86.6M 0s
       500K .......... .......... .......... .......... .......... 27% 89.8M 0s
       550K .......... .......... .......... .......... .......... 30% 79.4M 0s
       600K .......... .......... .......... .......... .......... 33% 89.7M 0s
       650K .......... .......... .......... .......... .......... 35% 92.8M 0s
       700K .......... .......... .......... .......... .......... 38% 86.4M 0s
       750K .......... .......... .......... .......... .......... 40% 20.9M 0s
       800K .......... .......... .......... .......... .......... 43% 79.8M 0s
       850K .......... .......... .......... .......... .......... 45% 90.6M 0s
       900K .......... .......... .......... .......... .......... 48% 73.6M 0s
       950K .......... .......... .......... .......... .......... 50% 79.1M 0s
      1000K .......... .......... .......... .......... .......... 53% 92.4M 0s
      1050K .......... .......... .......... .......... .......... 55% 88.6M 0s
      1100K .......... .......... .......... .......... .......... 58%  161M 0s
      1150K .......... .......... .......... .......... .......... 61%  318M 0s
      1200K .......... .......... .......... .......... .......... 63%  391M 0s
      1250K .......... .......... .......... .......... .......... 66%  412M 0s
      1300K .......... .......... .......... .......... .......... 68% 14.4M 0s
      1350K .......... .......... .......... .......... .......... 71% 77.2M 0s
      1400K .......... .......... .......... .......... .......... 73% 76.1M 0s
      1450K .......... .......... .......... .......... .......... 76% 78.8M 0s
      1500K .......... .......... .......... .......... .......... 78% 38.7M 0s
      1550K .......... .......... .......... .......... .......... 81% 81.5M 0s
      1600K .......... .......... .......... .......... .......... 83% 80.2M 0s
      1650K .......... .......... .......... .......... .......... 86% 89.5M 0s
      1700K .......... .......... .......... .......... .......... 89%  111M 0s
      1750K .......... .......... .......... .......... .......... 91%  356M 0s
      1800K .......... .......... .......... .......... .......... 94%  444M 0s
      1850K .......... .......... .......... .......... .......... 96%  441M 0s
      1900K .......... .......... .......... .......... .......... 99%  436M 0s
      1950K .......... .....                                      100%  239M=0.06s
    
    2019-10-09 12:53:42 (33.5 MB/s) - ‘tnseq_untreated.txt.gz’ saved [2012967/2012967]
    
    --2019-10-09 12:53:42--  https://nekrut.github.io/BMMB554/ta_gc.txt
    Resolving nekrut.github.io (nekrut.github.io)... 185.199.109.153, 185.199.111.153, 185.199.110.153, ...
    Connecting to nekrut.github.io (nekrut.github.io)|185.199.109.153|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 7315570 (7.0M) [text/plain]
    Saving to: ‘ta_gc.txt’
    
         0K .......... .......... .......... .......... ..........  0% 3.55M 2s
        50K .......... .......... .......... .......... ..........  1% 6.93M 1s
       100K .......... .......... .......... .......... ..........  2% 44.8M 1s
       150K .......... .......... .......... .......... ..........  2% 52.3M 1s
       200K .......... .......... .......... .......... ..........  3% 8.89M 1s
       250K .......... .......... .......... .......... ..........  4% 82.7M 1s
       300K .......... .......... .......... .......... ..........  4% 83.2M 1s
       350K .......... .......... .......... .......... ..........  5% 76.3M 1s
       400K .......... .......... .......... .......... ..........  6% 8.46M 1s
       450K .......... .......... .......... .......... ..........  6% 72.8M 0s
       500K .......... .......... .......... .......... ..........  7% 83.9M 0s
       550K .......... .......... .......... .......... ..........  8% 79.6M 0s
       600K .......... .......... .......... .......... ..........  9% 88.5M 0s
       650K .......... .......... .......... .......... ..........  9% 92.6M 0s
       700K .......... .......... .......... .......... .......... 10% 88.1M 0s
       750K .......... .......... .......... .......... .......... 11% 78.6M 0s
       800K .......... .......... .......... .......... .......... 11% 16.2M 0s
       850K .......... .......... .......... .......... .......... 12% 32.5M 0s
       900K .......... .......... .......... .......... .......... 13% 87.2M 0s
       950K .......... .......... .......... .......... .......... 13% 77.2M 0s
      1000K .......... .......... .......... .......... .......... 14%  337M 0s
      1050K .......... .......... .......... .......... .......... 15%  292M 0s
      1100K .......... .......... .......... .......... .......... 16%  415M 0s
      1150K .......... .......... .......... .......... .......... 16%  343M 0s
      1200K .......... .......... .......... .......... .......... 17%  421M 0s
      1250K .......... .......... .......... .......... .......... 18% 14.2M 0s
      1300K .......... .......... .......... .......... .......... 18% 34.6M 0s
      1350K .......... .......... .......... .......... .......... 19% 66.9M 0s
      1400K .......... .......... .......... .......... .......... 20% 91.7M 0s
      1450K .......... .......... .......... .......... .......... 20% 91.0M 0s
      1500K .......... .......... .......... .......... .......... 21% 94.0M 0s
      1550K .......... .......... .......... .......... .......... 22% 77.2M 0s
      1600K .......... .......... .......... .......... .......... 23% 92.7M 0s
      1650K .......... .......... .......... .......... .......... 23% 90.8M 0s
      1700K .......... .......... .......... .......... .......... 24% 92.8M 0s
      1750K .......... .......... .......... .......... .......... 25%  198M 0s
      1800K .......... .......... .......... .......... .......... 25%  420M 0s
      1850K .......... .......... .......... .......... .......... 26%  406M 0s
      1900K .......... .......... .......... .......... .......... 27% 92.2M 0s
      1950K .......... .......... .......... .......... .......... 27% 63.8M 0s
      2000K .......... .......... .......... .......... .......... 28% 73.1M 0s
      2050K .......... .......... .......... .......... .......... 29%  107M 0s
      2100K .......... .......... .......... .......... .......... 30%  379M 0s
      2150K .......... .......... .......... .......... .......... 30%  279M 0s
      2200K .......... .......... .......... .......... .......... 31%  415M 0s
      2250K .......... .......... .......... .......... .......... 32%  440M 0s
      2300K .......... .......... .......... .......... .......... 32%  427M 0s
      2350K .......... .......... .......... .......... .......... 33%  356M 0s
      2400K .......... .......... .......... .......... .......... 34%  438M 0s
      2450K .......... .......... .......... .......... .......... 34%  431M 0s
      2500K .......... .......... .......... .......... .......... 35%  441M 0s
      2550K .......... .......... .......... .......... .......... 36%  309M 0s
      2600K .......... .......... .......... .......... .......... 37%  412M 0s
      2650K .......... .......... .......... .......... .......... 37%  435M 0s
      2700K .......... .......... .......... .......... .......... 38%  433M 0s
      2750K .......... .......... .......... .......... .......... 39%  368M 0s
      2800K .......... .......... .......... .......... .......... 39%  423M 0s
      2850K .......... .......... .......... .......... .......... 40%  445M 0s
      2900K .......... .......... .......... .......... .......... 41%  438M 0s
      2950K .......... .......... .......... .......... .......... 41%  382M 0s
      3000K .......... .......... .......... .......... .......... 42%  336M 0s
      3050K .......... .......... .......... .......... .......... 43%  425M 0s
      3100K .......... .......... .......... .......... .......... 44%  425M 0s
      3150K .......... .......... .......... .......... .......... 44%  358M 0s
      3200K .......... .......... .......... .......... .......... 45%  424M 0s
      3250K .......... .......... .......... .......... .......... 46%  419M 0s
      3300K .......... .......... .......... .......... .......... 46% 22.2M 0s
      3350K .......... .......... .......... .......... .......... 47% 62.9M 0s
      3400K .......... .......... .......... .......... .......... 48% 77.6M 0s
      3450K .......... .......... .......... .......... .......... 48% 79.5M 0s
      3500K .......... .......... .......... .......... .......... 49% 60.7M 0s
      3550K .......... .......... .......... .......... .......... 50% 75.5M 0s
      3600K .......... .......... .......... .......... .......... 51% 95.5M 0s
      3650K .......... .......... .......... .......... .......... 51% 89.5M 0s
      3700K .......... .......... .......... .......... .......... 52% 93.6M 0s
      3750K .......... .......... .......... .......... .......... 53% 53.8M 0s
      3800K .......... .......... .......... .......... .......... 53% 79.8M 0s
      3850K .......... .......... .......... .......... .......... 54% 70.4M 0s
      3900K .......... .......... .......... .......... .......... 55% 77.5M 0s
      3950K .......... .......... .......... .......... .......... 55% 77.2M 0s
      4000K .......... .......... .......... .......... .......... 56% 69.6M 0s
      4050K .......... .......... .......... .......... .......... 57% 82.1M 0s
      4100K .......... .......... .......... .......... .......... 58% 76.5M 0s
      4150K .......... .......... .......... .......... .......... 58% 63.7M 0s
      4200K .......... .......... .......... .......... .......... 59% 81.5M 0s
      4250K .......... .......... .......... .......... .......... 60% 77.9M 0s
      4300K .......... .......... .......... .......... .......... 60% 81.9M 0s
      4350K .......... .......... .......... .......... .......... 61% 66.9M 0s
      4400K .......... .......... .......... .......... .......... 62% 75.2M 0s
      4450K .......... .......... .......... .......... .......... 62% 84.8M 0s
      4500K .......... .......... .......... .......... .......... 63%  176M 0s
      4550K .......... .......... .......... .......... .......... 64%  298M 0s
      4600K .......... .......... .......... .......... .......... 65%  243M 0s
      4650K .......... .......... .......... .......... .......... 65%  270M 0s
      4700K .......... .......... .......... .......... .......... 66%  340M 0s
      4750K .......... .......... .......... .......... .......... 67%  284M 0s
      4800K .......... .......... .......... .......... .......... 67%  364M 0s
      4850K .......... .......... .......... .......... .......... 68%  432M 0s
      4900K .......... .......... .......... .......... .......... 69%  429M 0s
      4950K .......... .......... .......... .......... .......... 69%  371M 0s
      5000K .......... .......... .......... .......... .......... 70%  428M 0s
      5050K .......... .......... .......... .......... .......... 71%  434M 0s
      5100K .......... .......... .......... .......... .......... 72%  413M 0s
      5150K .......... .......... .......... .......... .......... 72%  304M 0s
      5200K .......... .......... .......... .......... .......... 73%  431M 0s
      5250K .......... .......... .......... .......... .......... 74%  441M 0s
      5300K .......... .......... .......... .......... .......... 74%  432M 0s
      5350K .......... .......... .......... .......... .......... 75% 56.1M 0s
      5400K .......... .......... .......... .......... .......... 76%  441M 0s
      5450K .......... .......... .......... .......... .......... 76%  449M 0s
      5500K .......... .......... .......... .......... .......... 77%  432M 0s
      5550K .......... .......... .......... .......... .......... 78%  374M 0s
      5600K .......... .......... .......... .......... .......... 79%  462M 0s
      5650K .......... .......... .......... .......... .......... 79%  454M 0s
      5700K .......... .......... .......... .......... .......... 80%  375M 0s
      5750K .......... .......... .......... .......... .......... 81%  406M 0s
      5800K .......... .......... .......... .......... .......... 81%  457M 0s
      5850K .......... .......... .......... .......... .......... 82%  458M 0s
      5900K .......... .......... .......... .......... .......... 83%  456M 0s
      5950K .......... .......... .......... .......... .......... 83%  360M 0s
      6000K .......... .......... .......... .......... .......... 84%  450M 0s
      6050K .......... .......... .......... .......... .......... 85%  455M 0s
      6100K .......... .......... .......... .......... .......... 86%  446M 0s
      6150K .......... .......... .......... .......... .......... 86%  290M 0s
      6200K .......... .......... .......... .......... .......... 87%  437M 0s
      6250K .......... .......... .......... .......... .......... 88%  447M 0s
      6300K .......... .......... .......... .......... .......... 88%  410M 0s
      6350K .......... .......... .......... .......... .......... 89%  362M 0s
      6400K .......... .......... .......... .......... .......... 90%  438M 0s
      6450K .......... .......... .......... .......... .......... 90%  449M 0s
      6500K .......... .......... .......... .......... .......... 91%  441M 0s
      6550K .......... .......... .......... .......... .......... 92%  325M 0s
      6600K .......... .......... .......... .......... .......... 93%  445M 0s
      6650K .......... .......... .......... .......... .......... 93%  461M 0s
      6700K .......... .......... .......... .......... .......... 94%  445M 0s
      6750K .......... .......... .......... .......... .......... 95%  357M 0s
      6800K .......... .......... .......... .......... .......... 95%  385M 0s
      6850K .......... .......... .......... .......... .......... 96%  445M 0s
      6900K .......... .......... .......... .......... .......... 97%  439M 0s
      6950K .......... .......... .......... .......... .......... 97%  134M 0s
      7000K .......... .......... .......... .......... .......... 98% 93.8M 0s
      7050K .......... .......... .......... .......... .......... 99% 91.6M 0s
      7100K .......... .......... .......... .......... ....      100% 83.3M=0.09s
    
    2019-10-09 12:53:42 (79.5 MB/s) - ‘ta_gc.txt’ saved [7315570/7315570]
    



```python
data_file = 'tnseq_untreated.txt.gz'
```


```python
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
```


```python
# Reading TnSeq data into a dataframe

tnseq = pd.read_table('data.txt', header=None, names=['pos','blunt','cap','dual','erm','pen','tuf','gene'])
```

    /usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:2: FutureWarning: read_table is deprecated, use read_csv instead, passing sep='\t'.
      



```python
# Reading GC content data

gc = pd.read_table('ta_gc.txt', header=None, names=['pos','gc'])
```

    /usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:2: FutureWarning: read_table is deprecated, use read_csv instead, passing sep='\t'.
      



```python
tnseq.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pos</th>
      <th>blunt</th>
      <th>cap</th>
      <th>dual</th>
      <th>erm</th>
      <th>pen</th>
      <th>tuf</th>
      <th>gene</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2400002</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2400004</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2400006</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2400009</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>intergenic</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2400029</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
    </tr>
  </tbody>
</table>
</div>




```python
gc.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pos</th>
      <th>gc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4</td>
      <td>0.339286</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10</td>
      <td>0.354839</td>
    </tr>
    <tr>
      <th>2</th>
      <td>16</td>
      <td>0.367647</td>
    </tr>
    <tr>
      <th>3</th>
      <td>42</td>
      <td>0.372340</td>
    </tr>
    <tr>
      <th>4</th>
      <td>79</td>
      <td>0.303922</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Join tnseq and GC content data together

tn_gc = tnseq.merge(gc,left_on='pos',right_on='pos',how='left')
```


```python
tn_gc.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pos</th>
      <th>blunt</th>
      <th>cap</th>
      <th>dual</th>
      <th>erm</th>
      <th>pen</th>
      <th>tuf</th>
      <th>gene</th>
      <th>gc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2400002</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
      <td>0.225490</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2400004</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
      <td>0.225490</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2400006</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
      <td>0.215686</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2400009</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>intergenic</td>
      <td>0.225490</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2400029</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>intergenic</td>
      <td>0.215686</td>
    </tr>
  </tbody>
</table>
</div>




```python
# This is the list of column containing construct data

list(tn_gc)[1:7]
```




    ['blunt', 'cap', 'dual', 'erm', 'pen', 'tuf']



## "Melting data"

Visualization work much better with so called [narrow data](https://en.wikipedia.org/wiki/Wide_and_narrow_data). To convert our existing dataset into "narrow" form we will melt it down:

![](https://pandas.pydata.org/pandas-docs/stable/_images/reshaping_melt.png)

(This image and a much more detailed explanation of dataframe reshaping can be found in [Pandas Doc Pages](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)).


```python
# Melt tn_gc in tdf

tdf = pd.melt(tn_gc, id_vars=['pos','gc','gene'],value_vars=list(tn_gc)[1:7],var_name="construct",value_name="count").sort_values(by='pos')
```


```python
tdf.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pos</th>
      <th>gc</th>
      <th>gene</th>
      <th>construct</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>406329</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>cap</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1486729</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>tuf</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1216629</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>pen</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>676429</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>dual</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>136229</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>blunt</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Set genic and non-genic categories

tdf.loc[tdf['gene'] == 'intergenic','genic'] = 'no'
tdf.loc[tdf['gene'] != 'intergenic','genic'] = 'yes'
```


```python
tdf.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pos</th>
      <th>gc</th>
      <th>gene</th>
      <th>construct</th>
      <th>count</th>
      <th>genic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>406329</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>cap</td>
      <td>1.0</td>
      <td>no</td>
    </tr>
    <tr>
      <th>1486729</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>tuf</td>
      <td>0.0</td>
      <td>no</td>
    </tr>
    <tr>
      <th>1216629</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>pen</td>
      <td>0.0</td>
      <td>no</td>
    </tr>
    <tr>
      <th>676429</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>dual</td>
      <td>0.0</td>
      <td>no</td>
    </tr>
    <tr>
      <th>136229</th>
      <td>4</td>
      <td>0.339286</td>
      <td>intergenic</td>
      <td>blunt</td>
      <td>0.0</td>
      <td>no</td>
    </tr>
  </tbody>
</table>
</div>



# Visualizing the distribution of a dataset
When dealing with a set of data, often the first thing you’ll want to do is get a sense for how the variables are distributed. This chapter of the tutorial will give a brief introduction to some of the tools in seaborn for examining univariate and bivariate distributions. You may also want to look at the categorical plots chapter for examples of functions that make it easy to compare the distribution of a variable across levels of other variables.

These examples are taken from [official seaborn tutorials](https://seaborn.pydata.org/tutorial.html).

## Plotting univariate distributions
The most convenient way to take a quick look at a univariate distribution in seaborn is the [`distplot()`](https://seaborn.pydata.org/generated/seaborn.distplot.html#seaborn.distplot) function. By default, this will draw a [histogram](https://en.wikipedia.org/wiki/Histogram) and fit a kernel density estimate [KDE](https://en.wikipedia.org/wiki/Kernel_density_estimation)




```python
# Distribution of GC content 

sns.distplot(tdf['gc'])
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f48c6a0c6d8>




![png](/lab_site/images/output_26_1.png)



```python
# Distribution of read counts is a bit gloomy

sns.distplot(tdf['count'])
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f48c3f54cf8>




![png](/lab_site/images/output_27_1.png)



```python
# We can narrow it down

sns.distplot(tdf['count'][(tdf['count']>6)&(tdf['count']<100)])
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f48c3f12be0>




![png](/lab_site/images/output_28_1.png)



```python
# Or increase the number of bins and change the scale

g=sns.distplot(tdf['count'],bins=10000)
g.set(xscale="log")
```




    [None]




![png](/lab_site/images/output_29_1.png)



```python
# And also get rif of zero counts

g=sns.distplot(tdf['count'][tdf['count']>0],bins=10000)
g.set(xscale="log")

```




    [None]




![png](/lab_site/images/output_30_1.png)



```python
# Plotting the relationship between GC count and insertion frequency

sns.jointplot(x="count", y="gc", data=tdf[tdf['count']>10]);
```


![png](/lab_site/images/output_31_0.png)



```python

```

# Visualizing statistical relationships
Statistical analysis is a process of understanding how variables in a dataset relate to each other and how those relationships depend on other variables. Visualization can be a core component of this process because, when data are visualized properly, the human visual system can see trends and patterns that indicate a relationship.

We will discuss three seaborn functions in this tutorial. The one we will use most is [ `relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot). This is a [figure-level function](https://seaborn.pydata.org/introduction.html#intro-func-types) for visualizing statistical relationships using two common approaches: scatter plots and line plots. [ `relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot) combines a [FacetGrid](https://seaborn.pydata.org/generated/seaborn.FacetGrid.html#seaborn.FacetGrid) with one of two axes-level functions:

 - [`scatterplot()`](https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot) (with `kind="scatter"`; the default)
 - [`lineplot()`](https://seaborn.pydata.org/generated/seaborn.lineplot.html#seaborn.lineplot) (with `kind="line"`)
 
As we will see, these functions can be quite illuminating because they use simple and easily-understood representations of data that can nevertheless represent complex dataset structures. They can do so because they plot two-dimensional graphics that can be enhanced by mapping up to three additional variables using the semantics of hue, size, and style.

## Relating variables with scatter plots
The scatter plot is a mainstay of statistical visualization. It depicts the joint distribution of two variables using a cloud of points, where each point represents an observation in the dataset. This depiction allows the eye to infer a substantial amount of information about whether there is any meaningful relationship between them.

There are several ways to draw a scatter plot in seaborn. The most basic, which should be used when both variables are numeric, is the [`scatterplot()`](https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot) function. The [`scatterplot()`](https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot) is the default kind in [`relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot) (it can also be forced by setting `kind="scatter"`):


```python
sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100])
```




    <seaborn.axisgrid.FacetGrid at 0x7fe15c2e0940>




![png](/lab_site/images/output_35_1.png)


While the points are plotted in two dimensions, another dimension can be added to the plot by coloring the points according to a third variable. In seaborn, this is referred to as using a “hue semantic”, because the color of the point gains meaning:


```python
sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100],hue='construct')
```




    <seaborn.axisgrid.FacetGrid at 0x7f1a5d68df60>




![png](//lab_site/images/output_37_1.png)



```python
g = sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100],hue='construct')
g.set(yscale="log")
```




    <seaborn.axisgrid.FacetGrid at 0x7fe15beb6860>




![png](/lab_site/images/output_38_1.png)


To emphasize the difference between the classes, and to improve accessibility, you can use a different marker style for each class:


```python
sns.relplot(x='gc',y='count',data=tdf[tdf['count']>100],hue='construct',style='genic')
```




    <seaborn.axisgrid.FacetGrid at 0x7f961d061da0>




![png](/lab_site/images/output_40_1.png)



```python

```

# Categorical scatterplots
The default representation of the data in [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot) uses a scatterplot. There are actually two different categorical scatter plots in seaborn. They take different approaches to resolving the main challenge in representing categorical data with a scatter plot, which is that all of the points belonging to one category would fall on the same position along the axis corresponding to the categorical variable. The approach used by [`stripplot()`](https://seaborn.pydata.org/generated/seaborn.stripplot.html#seaborn.stripplot), which is the default “kind” in [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot) is to adjust the positions of points on the categorical axis with a small amount of random “jitter”:


```python
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100]);
```


![png](/lab_site/images/output_43_0.png)


The `jitter` parameter controls the magnitude of jitter or disables it altogether:


```python
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100],jitter=False);
```


![png](/lab_site/images/output_45_0.png)


The second approach adjusts the points along the categorical axis using an algorithm that prevents them from overlapping. It can give a better representation of the distribution of observations, although it only works well for relatively small datasets. This kind of plot is sometimes called a “beeswarm” and is drawn in seaborn by [`swarmplot()`](https://seaborn.pydata.org/generated/seaborn.swarmplot.html#seaborn.swarmplot), which is activated by setting `kind="swarm"` in [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot):


```python
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100],kind="swarm")
```


![png](/lab_site/images/output_47_0.png)


Similar to the relational plots, it’s possible to add another dimension to a categorical plot by using a `hue` semantic. (The categorical plots do not currently support `size` or `style` semantics). Each different categorical plotting function handles the `hue` semantic differently. For the scatter plots, it is only necessary to change the color of the points:


```python
sns.catplot(x="construct", y="count", data=tdf[tdf['count']>100],kind="swarm",hue='genic')
```




    <seaborn.axisgrid.FacetGrid at 0x7f961cb03cf8>




![png](/lab_site/images/output_49_1.png)


We’ve referred to the idea of “categorical axis”. In these examples, that’s always corresponded to the horizontal axis. But it’s often helpful to put the categorical variable on the vertical axis (particularly when the category names are relatively long or there are many categories). To do this, swap the assignment of variables to axes:


```python
sns.catplot(x="count", y="construct", data=tdf[tdf['count']>100],kind="swarm",hue='genic')
```




    <seaborn.axisgrid.FacetGrid at 0x7f961cb03c50>




![png](/lab_site/images/output_51_1.png)


## Distributions of observations within categories
As the size of the dataset grows,, categorical scatter plots become limited in the information they can provide about the distribution of values within each category. When this happens, there are several approaches for summarizing the distributional information in ways that facilitate easy comparisons across the category levels.



### Boxplots
The first is the familiar [`boxplot()`](https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot). This kind of plot shows the three quartile values of the distribution along with extreme values. The “whiskers” extend to points that lie within 1.5 IQRs of the lower and upper quartile, and then observations that fall outside this range are displayed independently. This means that each value in the boxplot corresponds to an actual observation in the data.


```python
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="box")
```




    <seaborn.axisgrid.FacetGrid at 0x7f961c9ea7f0>




![png](/lab_site/images/output_54_1.png)


When adding a `hue` semantic, the box for each level of the semantic variable is moved along the categorical axis so they don’t overlap:


```python
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="box",hue='genic')
```




    <seaborn.axisgrid.FacetGrid at 0x7f961d0a32e8>




![png](/lab_site/images/output_56_1.png)


A related function, [`boxenplot()`](https://seaborn.pydata.org/generated/seaborn.boxenplot.html#seaborn.boxenplot), draws a plot that is similar to a box plot but optimized for showing more information about the shape of the distribution. It is best suited for larger datasets:



```python
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="boxen")
```




    <seaborn.axisgrid.FacetGrid at 0x7f961b104c88>




![png](/lab_site/images/output_58_1.png)


### Violinplots
A different approach is a [`violinplot()`](https://seaborn.pydata.org/generated/seaborn.violinplot.html#seaborn.violinplot), which combines a boxplot with the kernel density estimation procedure:




```python
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="violin")
```




    <seaborn.axisgrid.FacetGrid at 0x7f96165426d8>




![png](/lab_site/images/output_60_1.png)



```python
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="violin",hue='genic')
```




    <seaborn.axisgrid.FacetGrid at 0x7f961cad2898>




![png](/lab_site/images/output_61_1.png)


It’s also possible to “split” the violins when the hue parameter has only two levels, which can allow for a more efficient use of space:


```python
sns.catplot(x="construct", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<100)],kind="violin",hue='genic',split=True)
```




    <seaborn.axisgrid.FacetGrid at 0x7f961c335ba8>




![png](/lab_site/images/output_63_1.png)


Finally, there are several options for the plot that is drawn on the interior of the violins, including ways to show each individual observation instead of the summary boxplot values:

## Statistical estimation within categories
For other applications, rather than showing the distribution within each category, you might want to show an estimate of the central tendency of the values. Seaborn has two main ways to show this information. Importantly, the basic API for these functions is identical to that for the ones discussed above.



### Bar plots
A familiar style of plot that accomplishes this goal is a bar plot. In seaborn, the [`barplot()`](https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot) function operates on a full dataset and applies a function to obtain the estimate (taking the mean by default). When there are multiple observations in each category, it also uses bootstrapping to compute a confidence interval around the estimate and plots that using error bars:


```python
sns.catplot(x="construct",y="count",hue="genic",kind="bar",data=tdf)
```




    <seaborn.axisgrid.FacetGrid at 0x7ff86739ffd0>




![png](/lab_site/images/output_67_1.png)


A special case for the bar plot is when you want to show the number of observations in each category rather than computing a statistic for a second variable. This is similar to a histogram over a categorical, rather than quantitative, variable. In seaborn, it’s easy to do so with the [`countplot()`](https://seaborn.pydata.org/generated/seaborn.countplot.html#seaborn.countplot) function:


```python
sns.catplot(x="genic",kind="count",data=tdf)
```




    <seaborn.axisgrid.FacetGrid at 0x7ff8650535f8>




![png](/lab_site/images/output_69_1.png)


## Showing multiple relationships with facets
Just like [`relplot()`](https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot), the fact that [`catplot()`](https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot) is built on a [`FacetGrid`](https://seaborn.pydata.org/generated/seaborn.FacetGrid.html#seaborn.FacetGrid) means that it is easy to add faceting variables to visualize higher-dimensional relationships:


```python
sns.catplot(x="genic", y="count", data=tdf[(tdf['count']>10) & (tdf['count']<1000)],kind="boxen",col='construct',col_wrap=2)
```




    <seaborn.axisgrid.FacetGrid at 0x7ff864e76470>




![png](/lab_site/images/output_71_1.png)




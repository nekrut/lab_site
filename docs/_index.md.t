---
title: AN Lab
draft: false
---
<style>
    #map{ height: 480px }
</style>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"
   integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
   crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"
   integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og=="
   crossorigin=""></script>
<script type="text/javascript" src="http://maps.stamen.com/js/tile.stamen.js?v1.3.0"></script>

<script>

 // replace "toner" here with "terrain" or "watercolor"
var layer = new L.StamenTileLayer("terrain");
var map = new L.Map("map", {
    center: new L.LatLng(40.79988, -77.86244),
    zoom: 16
});
var marker = L.marker([40.79988, -77.86259], { color: 'red'}).addTo(map);
map.addLayer(layer);
marker.bindPopup("<b>AN Lab</b><br>Wartik 505").openPopup();

 </script>



A part of Galaxy 




<div id="map"></div>

<ul class="nav nav-tabs mb-3" id="nav-tab" role="tablist">
  <li class="nav-item">
    <a class="nav-link active" id="pills-latest-tab" data-toggle="tab" href="#latest" role="tab" aria-controls="latest" aria-selected="true">Latest</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="pills-themes-tab" data-toggle="tab" href="#themes" role="tab" aria-controls="themes" aria-selected="false">Themes</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="pills-pulse-tab" data-toggle="tab" href="#pulse" role="tab" aria-controls="pulse" aria-selected="false">Pulse</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="pills-coordinates-tab" data-toggle="tab" href="#coord" role="tab" aria-controls="coord" aria-selected="false">Coordinates</a>
  </li>
</ul>


<div class="tab-content" id="myTabContent">
	<div class="tab-pane fade show active" id="latest" role="tabpanel" aria-labelledby="latest-tab">
		<h2>A high resolution view of adaptive event dynamics in a plasmid</h2>	
		<small>GBE [10.1093/gbe/evz197](https://doi.org/10.1093/gbe/evz197)</small>
		<img src="/images/han_fig1.png" />
		<hr>
		<small>The four replicates of the short term (R1, R2) and long term (R6, R7) turbidostat runs. OD600 values were constantly monitored and maintained at 0.8. Samples were taken every 12 h. Dips in OD<sub>600</sub> values represent sampling points. At each sampling point, ⅔ of the turbidostat volume was extracted for duplex sequencing. 
		</small>
	</div>
	<div class="tab-pane fade" id="themes" role="tabpanel" aria-labelledby="proj-tab">
  		<div class="card" id="plasmid">
  			<div class="card-header">
    			<h4>Mutational dynamics</h4>
 			</div>
  			<div class="card-body">
    			<p class="card-text">
    				Bacterial plasmids are self-replicating genetic elements that are fundamentally important to the evolution and adaptability of their hosts. As any genetic element, plasmids are subject to mutation. The fate of these mutations can be quite complex because forces affecting their frequencies are operating on two levels: intra-cellular andinter-cellular. We use experimental evolution approaches to deconvolute these processes at the level of individual cells.
    			</p>
    			<a target="_blank" href="https://www.ncbi.nlm.nih.gov/pubmed?term=((plasmid%5BTitle%5D)%20OR%20phage%5BTitle%5D)%20AND%20nekrutenko%5BAuthor%5D" class="btn btn-success btn-sm"><i data-feather="book-open"></i></a>
  			</div>
		</div>
		<div class="card" id="mt">
  			<div class="card-header">
    			<h4>Mitochondrial heteroplasmy</h4>
  			</div>
  			<div class="card-body">
    			<p class="card-text">
    				Human mitochondrial genomes are not unlike plasmids - they exist in multiple numbers inside each organell and may differ from each other. These differences are called heteroplasmies. Some heteroplasmies may be deleterious negatively affecting mitochondrial function. However, the extent of this negative effect often depends of their frequency. Because mitochondria is maternally inherited one can acquire deleterious heteroplmies only from their mother. But the frequency of transmitted heteroplasmies is unpredictable due to a bottlenck during oocyte maturation. We are trying to understand the dynamics of heteroplasmy inheritance by analyzing large numbers of mother/child pairs. 
    			</p>
    			<a target="_blank" href="https://www.ncbi.nlm.nih.gov/pubmed/?term=27566673+or+25313049+or+24641477+or+21699709" class="btn btn-success btn-sm"><i data-feather="book-open"></i></a>
  			</div>
		</div>
	</div>
  	<div class="tab-pane fade" id="pulse" role="tabpanel" aria-labelledby="pulse">
  			<a class="twitter-timeline" data-lang="en" data-theme="light" data-link-color="#2B7BB9" href="https://twitter.com/galaxyproject?ref_src=twsrc%5Etfw">Tweets by galaxyproject</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
		</div>
	</div>
	<div class="tab-pane fade" id="coord" role="tabpanel" aria-labelledby="coord">
  		<div id="map"></div>
  	</div>
 </div>
 
 
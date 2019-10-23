---
date: "2019-10-21"
title:
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



<div class="card mb-3">
  <div id="map"></div>
  <div class="card-body">
    <h5 class="card-title">Coordinates</h5>
    <p class="card-text">
    Nekrutenko Lab<br>
    Wartik 505<br>
    Department of Biochemistry and Molecular Biology<br>
    The Pennsylvania State University<br>
    University Park, PA 16802, USA<br>
    814.865.4752<br>
  </p>
    <a href="mailto:anton@nekrut.org" target="_blank" class="btn btn-secondary"><i data-feather="send"></i></a>
  </div>
</div>

<script>
// replace "toner" here with "terrain" or "watercolor"
var layer = new L.StamenTileLayer("terrain");
var map = new L.Map("map", {
center: new L.LatLng(40.79988, -77.86244),
zoom: 16
});
var marker = L.marker([40.79988, -77.86259]).addTo(map);
map.addLayer(layer);
marker.bindPopup("<b>AN Lab</b><br>Wartik 505").openPopup();
</script>
let map;

function initMap(lat, long) {
  const center = { lat: lat, lng: long }
  map = new google.maps.Map(document.getElementById("map"), {
    center: center,
    zoom: 15,
  });
  const marker = new google.maps.Marker({
    position: center,
    map: map,
  });
}

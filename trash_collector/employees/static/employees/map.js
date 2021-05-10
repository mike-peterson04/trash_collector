// Initialize and add the map
let map;

function initMap() {
  const center = '50131'
  map = new google.maps.Map(document.getElementById("map"), {
    center: center,
    zoom: 15,
  });
  const marker = new google.maps.Marker({
    position: center,
    map: map,
  });
}

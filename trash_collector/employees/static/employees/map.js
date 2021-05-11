let map;

function initMap() {
  const center = { lat: 41.57419394907601, lng: -93.8033035605153 }
  map = new google.maps.Map(document.getElementById("map"), {
    center: center,
    zoom: 15,
  });
  const marker = new google.maps.Marker({
    position: center,
    map: map,
  });
}

function openMap() {
  var locationInput = document.getElementById('location').value;
  var mapFrame = document.getElementById('mapFrame');
  var mapModal = document.getElementById('mapModal');
  
  // You can replace the following URL with the map URL of your choice
  var mapUrl = 'https://www.google.com/maps/embed/v1/place?q=' + encodeURIComponent(locationInput) + '&key=YOUR_GOOGLE_MAPS_API_KEY';

  mapFrame.src = mapUrl;
  mapModal.style.display = 'block';
}

function closeMap() {
  var mapModal = document.getElementById('mapModal');
  mapModal.style.display = 'none';
}
// === main.js ===
import { initMap, getMap, setUserMarker } from './mapManager.js';
import { initLayers } from './iconLayerManager.js';
import { loadPOIs } from './poiManager.js';

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  const map = getMap();
  initLayers(map);
  loadPOIs();

  const locationBtn = document.getElementById('get-location');
  if (locationBtn) {
    locationBtn.addEventListener('click', () => {
      if (!navigator.geolocation) {
        alert('Geolocalizzazione non supportata');
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setUserMarker(latitude, longitude);
        },
        () => alert('Impossibile ottenere la posizione')
      );
    });
  }
});

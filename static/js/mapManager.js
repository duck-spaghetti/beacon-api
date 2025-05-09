// === mapManager.js ===
import { getIcon } from './iconManager.js';

let map = null;
let userMarker = null;

const centralItalyBounds = L.latLngBounds([41.0, 11.0], [44.0, 14.0]);

export function initMap() {
  map = L.map('map', {
    attributionControl: false,
    maxBounds: centralItalyBounds,
    maxBoundsViscosity: 1.0,
    minZoom: 10,
    maxZoom: 18
  }).setView([41.9028, 12.4964], 13);

  map.on('drag', () => map.panInsideBounds(centralItalyBounds, { animate: false }));

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Selezione manuale posizione utente
  map.on('click', (e) => {
    if (window.uiState?.userSelecting) {
      const { lat, lng } = e.latlng;
      window.uiState.setUserPosition(lat, lng);
    }
  });
}

export function getMap() {
  return map;
}

export function setUserMarker(lat, lng, label = 'Sei qui') {
  if (userMarker) map.removeLayer(userMarker);

  userMarker = L.marker([lat, lng], { icon: getIcon('user') })
    .addTo(map)
    .bindPopup(label)
    .openPopup();

  map.setView([lat, lng], 14);
}

export function onMapClick(callback) {
  map.on('click', callback);
}

window.setUserMarker = setUserMarker;
window.getMap = getMap;

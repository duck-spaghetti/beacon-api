// === poiManager.js ===
const lang = document.body.dataset.lang;

import { getMap } from './mapManager.js';
import { getIcon } from './iconManager.js';

let allMarkers = [];
let map = null;
let clusterGroup = null;

export async function loadPOIs() {
  try {
    const response = await axios.get('/api/services');
    const services = response.data;
    map = getMap();
    const listView = document.getElementById('list-view');

    clusterGroup = L.markerClusterGroup();
    map.addLayer(clusterGroup);

    for (const service of services) {
////      const lat = parseFloat(service.lon.replace(',', '.'));
////      const lon = parseFloat(service.lat.replace(',', '.'));
      const lat = service.latitude;
      const lon = service.longitude;
      const tipo = service.type.toLowerCase();
      const icon = getIcon(tipo);

      if (!isNaN(lat) && !isNaN(lon)) {
        const marker = L.marker([lat, lon], { icon });

        marker._popupLoaded = false;
        marker.on('click', () => {
          if (marker._popupLoaded) return;
          marker._popupLoaded = true;
          marker.bindPopup('Caricamento...').openPopup();

          axios.get('/api/card-template', {
            params: {
              lat: lat,
              lon: lon,
              tipo: service.type,
              info: service.description,
              address: service.address,
              phone: service.phone,
              name: service.name,
              view: 'popup',
              lang: lang
            }
          }).then(res => marker.setPopupContent(res.data))
            .catch(() => marker.setPopupContent('<p>Errore nel caricamento</p>'));
        });

        axios.get('/api/card-template', {
          params: {
              lat: lat,
              lon: lon,
              tipo: service.type,
              info: service.description,
              address: service.address,
              phone: service.phone,
              name: service.name,
              view: 'list',
              lang: lang
          }
        }).then(res => {
          const cardWrapper = document.createElement('div');
          cardWrapper.innerHTML = res.data;
          const cardEl = cardWrapper.firstElementChild;
          listView.appendChild(cardEl);

          allMarkers.push({ tipo, marker, card: cardEl, lat, lon });

          if (allMarkers.length === services.length) {
            if (window.uiState?.activeFilters) {
              filterPOIs(window.uiState.activeFilters);
            }
          }
        });
      }
    }
  } catch (err) {
    console.error('Errore nel caricamento dei POI:', err);
  }
}

export function filterPOIs(activeTypes) {
  allMarkers.forEach(({ tipo, marker, card }) => {
    if (activeTypes.includes(tipo)) {
      if (!clusterGroup.hasLayer(marker)) clusterGroup.addLayer(marker);
      card.style.display = 'block';
    } else {
      if (clusterGroup.hasLayer(marker)) clusterGroup.removeLayer(marker);
      card.style.display = 'none';
    }
  });
}

export function sortPOIsByDistance(lat, lon) {
  if (!lat || !lon) return;
  const listView = document.getElementById('list-view');

  const toRad = deg => deg * Math.PI / 180;
  const getDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // km
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const visibleMarkers = allMarkers.filter(m => m.card.style.display !== 'none');

  visibleMarkers.sort((a, b) => {
    const distA = getDistance(lat, lon, a.lat, a.lon);
    const distB = getDistance(lat, lon, b.lat, b.lon);
    return distA - distB;
  });

  visibleMarkers.forEach(({ card }) => listView.appendChild(card));
}

// Alpine compatibility
window.poiManager = {
  filterPOIs,
  sortPOIsByDistance
};

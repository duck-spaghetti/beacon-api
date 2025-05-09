// === iconLayerManager.js ===
const layerKeys = ['dormire', 'documenti', 'mangiare', 'lavarsi', 'ascolto'];
const layers = {};

export function initLayers(map) {
  layerKeys.forEach(key => {
    layers[key] = L.layerGroup().addTo(map);
  });
}

export function getLayer(key) {
  return layers[key];
}

export function showLayer(map, key) {
  if (layers[key]) map.addLayer(layers[key]);
}

export function hideLayer(map, key) {
  if (layers[key]) map.removeLayer(layers[key]);
}

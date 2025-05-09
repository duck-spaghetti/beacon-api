// === iconManager.js ===
export const icons = {
    dormire: L.icon({ iconUrl: 'static/assets/icons/sleep.svg', iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] }),
    documenti: L.icon({ iconUrl: 'static/assets/icons/documents.svg', iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] }),
    mangiare: L.icon({ iconUrl: 'static/assets/icons/eat.svg', iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] }),
    lavarsi: L.icon({ iconUrl: 'static/assets/icons/shower.svg', iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] }),
    ascolto: L.icon({ iconUrl: 'static/assets/icons/listen.svg', iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] }),
    user: L.icon({ iconUrl: 'static/assets/icons/user_position.svg', iconSize: [48, 48], iconAnchor: [16, 32], popupAnchor: [0, -32] })
  };
  
  export function getIcon(type) {
    return icons[type] || icons.dormire;
  }
  
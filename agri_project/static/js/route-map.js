/**
 * Leaflet Map Integration for Secure Route Form
 */
document.addEventListener('DOMContentLoaded', function() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // 1. Setup Data from Template
    const geojsonField = document.getElementById('id_route_path_geojson');
    // Default to a general center or use the user's location if available
    let initialLat = 0;
    let initialLng = 0;
    let initialZoom = 2;

    // 2. Initialize Map
    const map = L.map('map').setView([initialLat, initialLng], initialZoom);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    let marker = null;

    // 3. Load Existing Data (For Edit View)
    if (geojsonField && geojsonField.value) {
        try {
            const existingData = JSON.parse(geojsonField.value);
            if (existingData.type === 'Point') {
                const lat = existingData.coordinates[1];
                const lng = existingData.coordinates[0];
                
                marker = L.marker([lat, lng]).addTo(map);
                map.setView([lat, lng], 15);
            }
        } catch (e) {
            console.error("Error parsing GeoJSON data", e);
        }
    }

    // 4. Handle Click to Pin Location
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;

        // Update or Create Marker
        if (marker) {
            marker.setLatLng(e.latlng);
        } else {
            marker = L.marker([lat, lng]).addTo(map);
        }

        // Update the Hidden Input for Django
        const geoData = {
            "type": "Point",
            "coordinates": [lng, lat]
        };
        geojsonField.value = JSON.stringify(geoData);
    });
});
/**
 * Map Initialization and Management
 * Handles Leaflet map setup, layers, and map interactions
 */

class MapManager {
    constructor() {
        this.map = null;
        this.incidentLayer = null;
        this.stationLayer = null;
        this.heatmapLayer = null;
        this.lgaLayer = null;
    }

    init() {
        // Initialize map centered on Nigeria
        this.map = L.map('map').setView([9.0820, 8.6753], 6);

        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Initialize marker cluster group for incidents
        this.incidentLayer = L.markerClusterGroup({
            showCoverageOnHover: false,
            spiderfyOnMaxZoom: true,
            removeOutsideVisibleBounds: true
        });
        this.map.addLayer(this.incidentLayer);

        // Initialize station layer
        this.stationLayer = L.markerClusterGroup();
        this.map.addLayer(this.stationLayer);

        // Expose map globally for other modules
        window._map = this.map;

        return this.map;
    }

    addIncidentMarker(incident) {
        if (!this.incidentLayer) return;

        const marker = L.marker([incident.geometry.coordinates[1], incident.geometry.coordinates[0]], {
            icon: this.getIncidentIcon(incident.properties.report_type)
        });

        marker.bindPopup(`
            <div class="p-2">
                <h3 class="font-bold">${incident.properties.title}</h3>
                <p class="text-sm text-gray-600">${incident.properties.description}</p>
                <span class="inline-block mt-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                    ${incident.properties.report_type}
                </span>
            </div>
        `);

        this.incidentLayer.addLayer(marker);
    }

    addStationMarker(station, type = 'police') {
        if (!this.stationLayer) return;

        const marker = L.marker([station.geometry.coordinates[1], station.geometry.coordinates[0]], {
            icon: this.getStationIcon(type)
        });

        marker.bindPopup(`
            <div class="p-2">
                <h3 class="font-bold">${station.properties.name}</h3>
                <p class="text-sm text-gray-600">${station.properties.address}</p>
                <p class="text-sm text-gray-500">${station.properties.state}, ${station.properties.lga}</p>
            </div>
        `);

        this.stationLayer.addLayer(marker);
    }

    getIncidentIcon(type) {
        const colors = {
            crime: '#ef4444',
            violence: '#f97316',
            fire: '#dc2626',
            flood: '#3b82f6',
            accident: '#eab308'
        };

        return L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${colors[type] || '#6b7280'}; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
    }

    getStationIcon(type) {
        const colors = {
            police: '#1d4ed8',
            amotekun: '#15803d'
        };

        return L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${colors[type] || '#6b7280'}; width: 35px; height: 35px; border-radius: 8px; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
            iconSize: [35, 35],
            iconAnchor: [17, 17]
        });
    }

    clearIncidents() {
        if (this.incidentLayer) {
            this.incidentLayer.clearLayers();
        }
    }

    clearStations() {
        if (this.stationLayer) {
            this.stationLayer.clearLayers();
        }
    }

    addHeatmap(data) {
        if (this.heatmapLayer) {
            this.map.removeLayer(this.heatmapLayer);
        }

        const heatData = data.map(point => [point.latitude, point.longitude, point.count || 1]);
        this.heatmapLayer = L.heatLayer(heatData, {
            radius: 25,
            blur: 15,
            maxZoom: 12,
            max: 10
        }).addTo(this.map);
    }

    fitBounds(bounds) {
        if (this.map && bounds) {
            this.map.fitBounds(bounds, { padding: [50, 50] });
        }
    }

    onMapClick(callback) {
        if (this.map) {
            this.map.on('click', callback);
        }
    }

    offMapClick(callback) {
        if (this.map) {
            this.map.off('click', callback);
        }
    }
}

// Initialize map manager
const mapManager = new MapManager();

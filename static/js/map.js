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
        this.map = L.map('map', {
            zoomControl: false  // Move zoom control away from buttons area
        }).setView([9.0820, 8.6753], 6);

        // Add zoom control to top-left
        L.control.zoom({ position: 'topleft' }).addTo(this.map);

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
        
        // Handle both GeoJSON Feature format and flat object format
        let lat, lng, reportType, title, description;
        
        if (incident.geometry && incident.geometry.coordinates) {
            lng = incident.geometry.coordinates[0];
            lat = incident.geometry.coordinates[1];
            reportType = incident.properties?.report_type;
            title = incident.properties?.title;
            description = incident.properties?.description;
        } else if (incident.latitude && incident.longitude) {
            lat = incident.latitude;
            lng = incident.longitude;
            reportType = incident.report_type;
            title = incident.title;
            description = incident.description;
        } else if (incident.geometry?.type === 'Point') {
            lng = incident.geometry.coordinates[0];
            lat = incident.geometry.coordinates[1];
            reportType = incident.report_type;
            title = incident.title;
            description = incident.description;
        } else {
            console.warn('Invalid incident format:', incident);
            return;
        }

        const marker = L.marker([lat, lng], {
            icon: this.getIncidentIcon(reportType)
        });

        marker.bindPopup(`
            <div style="padding: 8px;">
                <h3 style="font-weight: bold; margin-bottom: 4px;">${title || 'Untitled'}</h3>
                <p style="font-size: 12px; color: #666; margin-bottom: 6px;">${description || ''}</p>
                <span style="display: inline-block; font-size: 10px; background: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 4px;">
                    ${reportType || 'unknown'}
                </span>
            </div>
        `);

        this.incidentLayer.addLayer(marker);
    }

    addStationMarker(station, type = 'police') {
        if (!this.stationLayer) return;
        
        // Handle both GeoJSON Feature format and flat object format
        let lat, lng, name, address, state, lga;
        
        if (station.geometry && station.geometry.coordinates) {
            lng = station.geometry.coordinates[0];
            lat = station.geometry.coordinates[1];
            name = station.properties?.name;
            address = station.properties?.address;
            state = station.properties?.state;
            lga = station.properties?.lga;
        } else if (station.latitude && station.longitude) {
            lat = station.latitude;
            lng = station.longitude;
            name = station.name;
            address = station.address;
            state = station.state;
            lga = station.lga;
        } else {
            console.warn('Invalid station format:', station);
            return;
        }

        const marker = L.marker([lat, lng], {
            icon: this.getStationIcon(type)
        });

        marker.bindPopup(`
            <div style="padding: 8px;">
                <h3 style="font-weight: bold; margin-bottom: 4px;">${name || 'Unknown'}</h3>
                <p style="font-size: 12px; color: #666; margin-bottom: 4px;">${address || ''}</p>
                <p style="font-size: 11px; color: #999;">${state || ''}, ${lga || ''}</p>
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
            amotekun: '#15803d',
            hospital: '#dc2626'
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

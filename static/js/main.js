/**
 * Main Application Entry Point
 * Initializes all modules and coordinates application startup
 */

class Application {
    constructor() {
        this.mapManager = null;
        this.dataLoader = null;
        this.modalManager = null;
        this.dropdownManager = null;
        this.uiManager = null;
    }

    async init() {
        console.log('Initializing Amotekun Application...');
        
        try {
            this.uiManager = uiManager;
            this.modalManager = modalManager;
            this.modalManager.init();
            this.dropdownManager = dropdownManager;
            this.dropdownManager.init();
            this.dataLoader = dataLoader;
            this.mapManager = mapManager;
            this.map = this.mapManager.init();
            await this.loadInitialData();
            this.setupMapInteractions();
            window.refreshIncidents = () => this.refreshIncidents();
            console.log('Application initialized successfully');
        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.uiManager.showNotification('Failed to initialize application', 'error');
        }
    }

    async loadInitialData() {
        try {
            const incidents = await this.dataLoader.loadIncidents();
            this.displayIncidents(incidents);
            const policeStations = await this.dataLoader.loadPoliceStations();
            const amotekunStations = await this.dataLoader.loadAmotekunStations();
            this.displayStations(policeStations, 'police');
            this.displayStations(amotekunStations, 'amotekun');
            try {
                const hospitals = await this.dataLoader.loadHospitals();
                this.displayStations(hospitals, 'hospital');
            } catch (e) {
                console.warn('Hospitals not available:', e);
            }
            await this.dataLoader.loadLGAData();
            await this.dataLoader.loadStateData();
        } catch (error) {
            console.error('Failed to load initial data:', error);
        }
    }

    displayIncidents(incidents) {
        this.mapManager.clearIncidents();
        incidents.forEach(incident => {
            this.mapManager.addIncidentMarker(incident);
        });
    }

    displayStations(stations, type) {
        stations.forEach(station => {
            this.mapManager.addStationMarker(station, type);
        });
    }

    setupMapInteractions() {
        // Map click handler is set up below
    }

    async refreshIncidents() {
        try {
            const incidents = await this.dataLoader.loadIncidents();
            if (incidents && incidents.length > 0) {
                this.displayIncidents(incidents);
            }
        } catch (error) {
            console.error('Failed to refresh incidents:', error);
        }
    }

    async refreshStations() {
        try {
            const policeStations = await this.dataLoader.loadPoliceStations();
            const amotekunStations = await this.dataLoader.loadAmotekunStations();
            const hospitals = await this.dataLoader.loadHospitals();
            this.mapManager.clearStations();
            this.displayStations(policeStations, 'police');
            this.displayStations(amotekunStations, 'amotekun');
            this.displayStations(hospitals, 'hospital');
            this.uiManager.showNotification('Stations refreshed', 'success');
        } catch (error) {
            console.error('Failed to refresh stations:', error);
            this.uiManager.showNotification('Failed to refresh stations', 'error');
        }
    }

    async showHotspots() {
        try {
            const hotspots = await this.dataLoader.loadHotspots();
            const heatmapData = hotspots.map(h => ({
                latitude: h.latitude,
                longitude: h.longitude,
                count: h.count
            }));
            this.mapManager.addHeatmap(heatmapData);
            this.uiManager.showNotification('Hotspots displayed', 'success');
        } catch (error) {
            console.error('Failed to show hotspots:', error);
            this.uiManager.showNotification('Failed to show hotspots', 'error');
        }
    }

    async findNearestStation(lat, lon, type = 'police') {
        try {
            const result = await stationAPI.getNearest(lat, lon, type, 1);
            if (result.features && result.features.length > 0) {
                const station = result.features[0];
                this.uiManager.showNotification(
                    `Nearest ${type} station: ${station.properties.name}`,
                    'info'
                );
                return station;
            } else {
                this.uiManager.showNotification('No station found', 'warning');
                return null;
            }
        } catch (error) {
            console.error('Failed to find nearest station:', error);
            this.uiManager.showNotification('Failed to find nearest station', 'error');
            return null;
        }
    }
}

// Geocoding with Nominatim (OpenStreetMap) + Toast notifications
function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: #333; color: white; padding: 12px 20px; border-radius: 6px; z-index: 10000; font-size: 14px;';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

async function geocodeLocation(query) {
    if (!query || !query.trim()) return null;
    
    try {
        const response = await fetch(
            'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(query) + '&limit=1'
        );
        const data = await response.json();
        if (data && data.length > 0) {
            return {
                lat: parseFloat(data[0].lat),
                lng: parseFloat(data[0].lon),
                display_name: data[0].display_name
            };
        }
        return null;
    } catch (error) {
        console.error('Geocode error:', error);
        return null;
    }
}

// Initialize application
let app;

window.addEventListener('load', async () => {
    const incidentBtn = document.getElementById('incident-btn');
    const dispatchBtn = document.getElementById('dispatch-btn');
    
    console.log('Buttons found:', !!incidentBtn, !!dispatchBtn);
    
    if (incidentBtn) {
        incidentBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('Incident button clicked');
            const sidebar = document.getElementById('incident-sidebar');
            if (sidebar) {
                sidebar.style.display = 'block';
            }
        });
    }
    
    if (dispatchBtn) {
        dispatchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('Dispatch button clicked');
            const sidebar = document.getElementById('dispatch-sidebar');
            if (sidebar) {
                sidebar.style.display = 'block';
            }
        });
    }
    
    // Geocode button handler
    const geocodeBtn = document.getElementById('geocode-btn');
    if (geocodeBtn) {
        geocodeBtn.addEventListener('click', async () => {
            const locationInput = document.getElementById('location_search');
            const latInput = document.getElementById('latitude');
            const lngInput = document.getElementById('longitude');
            
            if (!locationInput || !locationInput.value) {
                showToast('Please enter a location');
                return;
            }
            
            const result = await geocodeLocation(locationInput.value);
            if (result) {
                latInput.value = result.lat;
                lngInput.value = result.lng;
                if (window._map) {
                    window._map.setView([result.lat, result.lng], 14);
                }
            } else {
                showToast('Location not found');
            }
        });
    }
    
    // Initialize app
    if (typeof mapManager !== 'undefined') {
        app = new Application();
        await app.init();
        
        if (window._map) {
            window._map.on('click', function(e) {
                const latInput = document.getElementById('latitude');
                const lngInput = document.getElementById('longitude');
                if (latInput && lngInput) {
                    latInput.value = e.latlng.lat.toFixed(6);
                    lngInput.value = e.latlng.lng.toFixed(6);
                }
                const sidebar = document.getElementById('incident-sidebar');
                if (sidebar) {
                    sidebar.style.display = 'block';
                }
            });
        }

        // HTMX custom event triggered by incident-create view
        document.body.addEventListener('incidentAdded', function() {
            const sidebar = document.getElementById('incident-sidebar');
            if (sidebar) sidebar.style.display = 'none';
            
            // Add just-created incident to map
            const lat = document.getElementById('latitude')?.value;
            const lng = document.getElementById('longitude')?.value;
            const title = document.getElementById('title')?.value;
            const description = document.getElementById('description')?.value;
            const reportType = document.getElementById('report_type')?.value;
            
            if (lat && lng && app && app.mapManager) {
                app.mapManager.addIncidentMarker({
                    geometry: { coordinates: [parseFloat(lng), parseFloat(lat)] },
                    properties: { title, description, report_type: reportType }
                });
                showToast('Incident reported successfully');
            }
        });

        // HTMX custom event triggered by dispatch-create
        document.body.addEventListener('dispatchAdded', function() {
            const sidebar = document.getElementById('dispatch-sidebar');
            if (sidebar) sidebar.style.display = 'none';
            showToast('Dispatch created successfully');
        });
    }
});

window.app = app;
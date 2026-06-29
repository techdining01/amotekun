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
            // Initialize UI components first
            this.uiManager = uiManager;
            
            // Initialize modal manager
            this.modalManager = modalManager;
            this.modalManager.init();
            
            // Initialize dropdown manager
            this.dropdownManager = dropdownManager;
            this.dropdownManager.init();
            
            // Initialize data loader
            this.dataLoader = dataLoader;
            
            // Initialize map
            this.mapManager = mapManager;
            this.map = this.mapManager.init();
            
            // Load initial data
            await this.loadInitialData();
            
            // Setup map interactions
            this.setupMapInteractions();
            
            // Expose refresh function globally
            window.refreshIncidents = () => this.refreshIncidents();
            
            console.log('Application initialized successfully');
        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.uiManager.showNotification('Failed to initialize application', 'error');
        }
    }

    async loadInitialData() {
        try {
            // Load incidents
            const incidents = await this.dataLoader.loadIncidents();
            this.displayIncidents(incidents);
            
            // Load stations
            const policeStations = await this.dataLoader.loadPoliceStations();
            const amotekunStations = await this.dataLoader.loadAmotekunStations();
            this.displayStations(policeStations, 'police');
            this.displayStations(amotekunStations, 'amotekun');
            
            // Load GeoJSON data (for location lookup)
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
        // Map click handler is set up in modal manager
        // Additional map interactions can be added here
    }

    async refreshIncidents() {
        try {
            const incidents = await this.dataLoader.loadIncidents();
            this.displayIncidents(incidents);
            this.uiManager.showNotification('Incidents refreshed', 'success');
        } catch (error) {
            console.error('Failed to refresh incidents:', error);
            this.uiManager.showNotification('Failed to refresh incidents', 'error');
        }
    }

    async refreshStations() {
        try {
            const policeStations = await this.dataLoader.loadPoliceStations();
            const amotekunStations = await this.dataLoader.loadAmotekunStations();
            this.mapManager.clearStations();
            this.displayStations(policeStations, 'police');
            this.displayStations(amotekunStations, 'amotekun');
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

// Initialize application when DOM is ready
let app;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', async () => {
        app = new Application();
        await app.init();
    });
} else {
    app = new Application();
    app.init();
}

// Expose app instance globally
window.app = app;

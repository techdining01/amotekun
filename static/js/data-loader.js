/**
 * Data Loader Module
 * Handles loading and managing GeoJSON data and incidents
 */

class DataLoader {
    constructor() {
        this.lgaData = null;
        this.stateData = null;
        this.incidents = [];
        this.stations = {
            police: [],
            amotekun: [],
            hospitals: []
        };
    }

    async loadGeoJSON(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Failed to load GeoJSON from ${url}`);
            }
            return await response.json();
        } catch (error) {
            console.error('GeoJSON load error:', error);
            throw error;
        }
    }

    async loadLGAData() {
        try {
            this.lgaData = await this.loadGeoJSON('/static/data/LGA_data.geojson');
            return this.lgaData;
        } catch (error) {
            console.error('Failed to load LGA data:', error);
            return null;
        }
    }

    async loadStateData() {
        try {
            this.stateData = await this.loadGeoJSON('/static/data/geoBoundaries-NGA-ADM1_simplified.geojson');
            return this.stateData;
        } catch (error) {
            console.error('Failed to load state data:', error);
            return null;
        }
    }

    async loadPoliceStations() {
        try {
            const data = await stationAPI.getPoliceStations();
            if (data && data.features) {
                this.stations.police = data.features;
            } else if (Array.isArray(data)) {
                this.stations.police = data;
            } else if (data && Array.isArray(data.results)) {
                this.stations.police = data.results;
            } else {
                this.stations.police = [];
            }
            return this.stations.police;
        } catch (error) {
            console.error('Failed to load police stations:', error);
            return [];
        }
    }

    async loadAmotekunStations() {
        try {
            const data = await stationAPI.getAmotekunStations();
            if (data && data.features) {
                this.stations.amotekun = data.features;
            } else if (Array.isArray(data)) {
                this.stations.amotekun = data;
            } else if (data && Array.isArray(data.results)) {
                this.stations.amotekun = data.results;
            } else {
                this.stations.amotekun = [];
            }
            return this.stations.amotekun;
        } catch (error) {
            console.error('Failed to load Amotekun stations:', error);
            return [];
        }
    }

    async loadHospitals() {
        try {
            const data = await stationAPI.getHospitals();
            if (data && data.features) {
                this.stations.hospitals = data.features;
            } else if (Array.isArray(data)) {
                this.stations.hospitals = data;
            } else if (data && Array.isArray(data.results)) {
                this.stations.hospitals = data.results;
            } else {
                this.stations.hospitals = [];
            }
            return this.stations.hospitals;
        } catch (error) {
            console.error('Failed to load hospitals:', error);
            return [];
        }
    }

    async loadIncidents() {
        try {
            const data = await incidentAPI.getAll();
            // Handle GeoJSON FeatureCollection or direct array
            if (data && data.features) {
                this.incidents = data.features;
            } else if (Array.isArray(data)) {
                this.incidents = data;
            } else if (data && Array.isArray(data.results)) {
                this.incidents = data.results;
            } else {
                this.incidents = [];
            }
            return this.incidents;
        } catch (error) {
            console.error('Failed to load incidents:', error);
            return [];
        }
    }

    async loadHotspots() {
        try {
            const data = await incidentAPI.getHotspots();
            return data;
        } catch (error) {
            console.error('Failed to load hotspots:', error);
            return [];
        }
    }

    getIncidents() {
        return this.incidents;
    }

    getStations(type = 'all') {
        if (type === 'police') return this.stations.police;
        if (type === 'amotekun') return this.stations.amotekun;
        if (type === 'hospitals') return this.stations.hospitals;
        return [...this.stations.police, ...this.stations.amotekun, ...this.stations.hospitals];
    }

    getLGAData() {
        return this.lgaData;
    }

    getStateData() {
        return this.stateData;
    }

    findLGAByPoint(lat, lng) {
        if (!this.lgaData) return null;

        const point = turf.point([lng, lat]);
        
        for (const feature of this.lgaData.features) {
            if (turf.booleanPointInPolygon(point, feature)) {
                return feature;
            }
        }
        
        return null;
    }

    findStateByPoint(lat, lng) {
        if (!this.stateData) return null;

        const point = turf.point([lng, lat]);
        
        for (const feature of this.stateData.features) {
            if (turf.booleanPointInPolygon(point, feature)) {
                return feature;
            }
        }
        
        return null;
    }
}

// Initialize data loader
const dataLoader = new DataLoader();

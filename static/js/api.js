/**
 * API Service Module
 * Handles all API calls to the backend
 */

class APIService {
    constructor() {
        this.baseURL = '/api';
    }

    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    }

    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    }

    async put(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('PUT request failed:', error);
            throw error;
        }
    }

    async delete(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('DELETE request failed:', error);
            throw error;
        }
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return '';
    }
}

// Incident API methods
class IncidentAPI extends APIService {
    async getAll() {
        return await this.get('/incidents/');
    }

    async getById(id) {
        return await this.get(`/incidents/${id}/`);
    }

    async create(data) {
        return await this.post('/incidents/', data);
    }

    async update(id, data) {
        return await this.put(`/incidents/${id}/`, data);
    }

    async delete(id) {
        return await this.delete(`/incidents/${id}/`);
    }

    async getByType(type) {
        return await this.get(`/incidents/type/${type}/`);
    }

    async getHotspots() {
        return await this.get('/hotspots/');
    }
}

// Station API methods
class StationAPI extends APIService {
    async getNearest(lat, lon, type = 'police', limit = 1) {
        return await this.get(`/stations/nearest/?lat=${lat}&lon=${lon}&type=${type}&limit=${limit}`);
    }

    async getPoliceStations() {
        return await this.get('/stations/police/');
    }

    async getAmotekunStations() {
        return await this.get('/stations/amotekun/');
    }

    async getHospitals() {
        return await this.get('/stations/hospitals/');
    }

    async getRoute(srcLat, srcLon, dstLat, dstLon) {
        return await this.get(`/stations/route/?src_lat=${srcLat}&src_lon=${srcLon}&dst_lat=${dstLat}&dst_lon=${dstLon}`);
    }
}

// Dispatch API methods
class DispatchAPI extends APIService {
    async getAll() {
        return await this.get('/dispatch/dispatches/');
    }

    async getById(id) {
        return await this.get(`/dispatch/dispatches/${id}/`);
    }

    async create(data) {
        return await this.post('/dispatch/dispatches/', data);
    }

    async update(id, data) {
        return await this.put(`/dispatch/dispatches/${id}/`, data);
    }

    async delete(id) {
        return await this.delete(`/dispatch/dispatches/${id}/`);
    }
}

// Geography API methods
class GeographyAPI extends APIService {
    async getYorubaLGAs() {
        return await this.get('/yoruba-lgas/');
    }

    async getStateLGAs(stateName) {
        return await this.get(`/state-lgas/${stateName}/`);
    }

    async getLGACentroid(id) {
        return await this.get(`/lga-centroid/${id}/`);
    }

    async getNearbyFacilities(lat, lng, type, radius) {
        return await this.get(`/geography/boundaries/?lat=${lat}&lng=${lng}&type=${type}&radius=${radius}`);
    }

    async getNearestBoundaries(lat, lng, type, limit) {
        return await this.get(`/geography/boundaries/nearest/?lat=${lat}&lng=${lng}&type=${type}&limit=${limit}`);
    }

    async getBoundariesWithin(lat, lng, radius) {
        return await this.get(`/geography/boundaries/within/?lat=${lat}&lng=${lng}&radius=${radius}`);
    }

    async getBuffer(lat, lng, radius) {
        return await this.get(`/geography/boundaries/buffer/?lat=${lat}&lng=${lng}&radius=${radius}`);
    }
}

// Analytics/Hotspot API methods
class AnalyticsAPI extends APIService {
    async getHotspots() {
        return await this.get('/analytics/hotspots/crime/');
    }

    async generateHotspots(data) {
        return await this.post('/analytics/hotspots/generate/', data);
    }

    async getAnalyses() {
        return await this.get('/analytics/analyses/');
    }
}

// Mobile API methods
class MobileAPI extends APIService {
    async getIncidents() {
        return await this.get('/mobile/incidents/');
    }

    async getNearbyIncidents(lat, lng, radius) {
        return await this.get(`/mobile/incidents/nearby/?lat=${lat}&lng=${lng}&radius=${radius}`);
    }

    async getFacilities(lat, lng, type, radius) {
        return await this.get(`/mobile/facilities/?lat=${lat}&lng=${lng}&type=${type}&radius=${radius}`);
    }

    async getDispatches() {
        return await this.get('/mobile/dispatch/');
    }

    async acceptDispatch(id) {
        return await this.post(`/mobile/dispatch/${id}/accept/`);
    }

    async completeDispatch(id) {
        return await this.post(`/mobile/dispatch/${id}/complete/`);
    }

    async uploadMedia(formData) {
        return await fetch(`${this.baseURL}/mobile/media/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCSRFToken()
            },
            body: formData
        }).then(r => r.json());
    }
}

// Initialize API services
const incidentAPI = new IncidentAPI();
const stationAPI = new StationAPI();
const dispatchAPI = new DispatchAPI();
const geographyAPI = new GeographyAPI();
const analyticsAPI = new AnalyticsAPI();
const mobileAPI = new MobileAPI();

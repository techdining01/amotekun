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
}

// Initialize API services
const incidentAPI = new IncidentAPI();
const stationAPI = new StationAPI();
const dispatchAPI = new DispatchAPI();
const geographyAPI = new GeographyAPI();

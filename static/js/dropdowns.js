/**
 * Dropdown Population Module
 * Handles populating form dropdowns with data from API
 */

class DropdownManager {
    constructor() {
        this.selectors = {
            incident: 'dispatch-incident',
            police: 'dispatch-police',
            amotekun: 'dispatch-amotekun'
        };
    }

    async populateIncidents() {
        try {
            const data = await incidentAPI.getAll();
            const select = document.getElementById(this.selectors.incident);
            
            if (!select) return;
            
            select.innerHTML = '';
            
            const features = data.features || data || [];
            features.forEach(item => {
                const id = item.id;
                const title = item.properties ? item.properties.title : item.title;
                if (id && title) {
                    const option = document.createElement('option');
                    option.value = id;
                    option.textContent = title;
                    select.appendChild(option);
                }
            });
        } catch (error) {
            console.error('Failed to populate incidents dropdown:', error);
        }
    }

    async populatePoliceStations() {
        try {
            const data = await stationAPI.getPoliceStations();
            const select = document.getElementById(this.selectors.police);
            
            if (!select) return;
            
            select.innerHTML = '<option value="">None</option>';
            
            const stations = data.features || data || [];
            stations.forEach(station => {
                const id = station.id;
                const name = station.properties ? station.properties.name : station.name;
                if (id && name) {
                    const option = document.createElement('option');
                    option.value = id;
                    option.textContent = name;
                    select.appendChild(option);
                }
            });
        } catch (error) {
            console.error('Failed to populate police stations dropdown:', error);
        }
    }

    async populateAmotekunStations() {
        try {
            const data = await stationAPI.getAmotekunStations();
            const select = document.getElementById(this.selectors.amotekun);
            
            if (!select) return;
            
            select.innerHTML = '<option value="">None</option>';
            
            const stations = data.features || data || [];
            stations.forEach(station => {
                const id = station.id;
                const name = station.properties ? station.properties.name : station.name;
                if (id && name) {
                    const option = document.createElement('option');
                    option.value = id;
                    option.textContent = name;
                    select.appendChild(option);
                }
            });
        } catch (error) {
            console.error('Failed to populate Amotekun stations dropdown:', error);
        }
    }

    async populateAll() {
        await Promise.all([
            this.populateIncidents(),
            this.populatePoliceStations(),
            this.populateAmotekunStations()
        ]);
    }

    init() {
        // Populate dropdowns on DOM load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.populateAll());
        } else {
            this.populateAll();
        }
    }
}

// Initialize dropdown manager
const dropdownManager = new DropdownManager();

// Expose functions globally for backward compatibility
window.populateDispatchIncidents = () => dropdownManager.populateIncidents();
window.populateDispatchPolice = () => dropdownManager.populatePoliceStations();
window.populateDispatchAmotekun = () => dropdownManager.populateAmotekunStations();

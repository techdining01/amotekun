# JavaScript Modules Documentation

## Overview
The JavaScript code has been modularized into separate files for better maintainability and organization. Each module has a specific responsibility.

## Module Structure

### 1. `api.js` - API Service Layer
**Purpose:** Handles all HTTP requests to the backend API

**Classes:**
- `APIService` - Base class for API calls (GET, POST, PUT, DELETE)
- `IncidentAPI` - Incident-specific API methods
- `StationAPI` - Station-specific API methods  
- `DispatchAPI` - Dispatch-specific API methods
- `GeographyAPI` - Geography/LGA-specific API methods

**Global Instances:**
- `incidentAPI`
- `stationAPI`
- `dispatchAPI`
- `geographyAPI`

### 2. `map.js` - Map Management
**Purpose:** Manages Leaflet map initialization, layers, and interactions

**Class:** `MapManager`

**Key Methods:**
- `init()` - Initialize the map
- `addIncidentMarker(incident)` - Add incident marker to map
- `addStationMarker(station, type)` - Add station marker to map
- `clearIncidents()` - Clear all incident markers
- `clearStations()` - Clear all station markers
- `addHeatmap(data)` - Add heatmap layer
- `fitBounds(bounds)` - Fit map to bounds
- `onMapClick(callback)` - Register click handler
- `offMapClick(callback)` - Remove click handler

**Global Instance:** `mapManager`

### 3. `data-loader.js` - Data Loading
**Purpose:** Loads and manages GeoJSON data and application data

**Class:** `DataLoader`

**Key Methods:**
- `loadGeoJSON(url)` - Load GeoJSON from URL
- `loadLGAData()` - Load LGA boundaries
- `loadStateData()` - Load state boundaries
- `loadPoliceStations()` - Load police stations from API
- `loadAmotekunStations()` - Load Amotekun stations from API
- `loadIncidents()` - Load incidents from API
- `loadHotspots()` - Load hotspot data
- `findLGAByPoint(lat, lng)` - Find LGA at coordinates
- `findStateByPoint(lat, lng)` - Find state at coordinates

**Global Instance:** `dataLoader`

### 4. `modals.js` - Modal Management
**Purpose:** Manages Alpine.js modal stores for incident and dispatch modals

**Class:** `ModalManager`

**Key Methods:**
- `initIncidentModal()` - Initialize incident modal Alpine store
- `initDispatchModal()` - Initialize dispatch modal Alpine store
- `openIncidentModal(lat, lng)` - Open incident modal
- `closeIncidentModal()` - Close incident modal
- `openDispatchModal(incidentId)` - Open dispatch modal
- `closeDispatchModal()` - Close dispatch modal

**Global Instance:** `modalManager`

### 5. `dropdowns.js` - Dropdown Population
**Purpose:** Populates form dropdowns with data from API

**Class:** `DropdownManager`

**Key Methods:**
- `populateIncidents()` - Populate incident dropdown
- `populatePoliceStations()` - Populate police station dropdown
- `populateAmotekunStations()` - Populate Amotekun station dropdown
- `populateAll()` - Populate all dropdowns

**Global Instance:** `dropdownManager`

**Global Functions (for backward compatibility):**
- `window.populateDispatchIncidents()`
- `window.populateDispatchPolice()`
- `window.populateDispatchAmotekun()`

### 6. `ui-components.js` - UI Components
**Purpose:** Handles UI interactions, notifications, and visual feedback

**Class:** `UIManager`

**Key Methods:**
- `showNotification(message, type, duration)` - Show toast notification
- `showLoading(target)` - Show loading overlay
- `hideLoading(loadingElement)` - Hide loading overlay
- `toggleSidebar()` - Toggle sidebar visibility
- `setActiveTab(tabId)` - Switch active tab
- `formatDateTime(dateString)` - Format date/time
- `formatRelativeTime(dateString)` - Format relative time (e.g., "2 hours ago")
- `getStatusBadge(status)` - Get HTML for status badge
- `getIncidentTypeBadge(type)` - Get HTML for incident type badge

**Global Instance:** `uiManager`

### 7. `main.js` - Application Entry Point
**Purpose:** Initializes all modules and coordinates application startup

**Class:** `Application`

**Key Methods:**
- `init()` - Initialize application
- `loadInitialData()` - Load initial data on startup
- `displayIncidents(incidents)` - Display incidents on map
- `displayStations(stations, type)` - Display stations on map
- `setupMapInteractions()` - Setup map event handlers
- `refreshIncidents()` - Refresh incident data
- `refreshStations()` - Refresh station data
- `showHotspots()` - Display heatmap of hotspots
- `findNearestStation(lat, lon, type)` - Find nearest station

**Global Instance:** `app`

## Loading Order
The modules must be loaded in this order in your HTML:

1. `api.js` - API services (no dependencies)
2. `map.js` - Map management (no dependencies)
3. `data-loader.js` - Data loading (depends on api.js)
4. `modals.js` - Modal management (no dependencies)
5. `dropdowns.js` - Dropdown population (depends on api.js)
6. `ui-components.js` - UI components (no dependencies)
7. `main.js` - Application entry point (depends on all above)

## Usage Example

```html
<script src="{% static 'js/api.js' %}"></script>
<script src="{% static 'js/map.js' %}"></script>
<script src="{% static 'js/data-loader.js' %}"></script>
<script src="{% static 'js/modals.js' %}"></script>
<script src="{% static 'js/dropdowns.js' %}"></script>
<script src="{% static 'js/ui-components.js' %}"></script>
<script src="{% static 'js/main.js' %}"></script>
```

## Global Functions Available

- `window.refreshIncidents()` - Refresh incident data on map
- `window.populateDispatchIncidents()` - Populate incident dropdown
- `window.populateDispatchPolice()` - Populate police station dropdown
- `window.populateDispatchAmotekun()` - Populate Amotekun station dropdown
- `window._map` - Global Leaflet map instance
- `window.app` - Global application instance

## Adding New Modules

When adding new modules:

1. Create a new file in `static/js/`
2. Use a descriptive filename (e.g., `analytics.js`, `notifications.js`)
3. Create a class with a single responsibility
4. Initialize a global instance at the bottom of the file
5. Add the script tag to `templates/index.html` in the correct order
6. Update this README with the new module documentation

## Migration Notes

The old `app.js` file was corrupted with null bytes and has been replaced with this modular structure. All functionality has been preserved and improved with better organization.

If you need to reference the old file, it has been backed up as `app.js.backup` (if it could be salvaged).

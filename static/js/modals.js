/**
 * Modal Management Module
 * Handles incident and dispatch modal state and interactions
 */

class ModalManager {
    constructor() {
        this.incidentModal = {
            isOpen: false,
            latitude: null,
            longitude: null
        };
        
        this.dispatchModal = {
            isOpen: false
        };
    }

    initIncidentModal() {
        const self = this;
        
        // Register Alpine.js store for incident modal
        document.addEventListener('alpine:init', () => {
            Alpine.store('incidentModal', {
                isOpen: false,
                latitude: null,
                longitude: null,
                open(lat, lng) {
                    if (lat && lng) {
                        this.latitude = lat;
                        this.longitude = lng;
                        document.getElementById('latitude').value = lat;
                        document.getElementById('longitude').value = lng;
                    }
                    this.isOpen = true;
                    if (window._map && window._mapClickHandler) {
                        window._map.off('click', window._mapClickHandler);
                    }
                },
                close() {
                    this.isOpen = false;
                    this.latitude = null;
                    this.longitude = null;
                    if (window._map && window._mapClickHandler) {
                        window._map.on('click', window._mapClickHandler);
                    }
                },
                init() {
                    const checkMap = setInterval(() => {
                        if (window._map) {
                            clearInterval(checkMap);
                            window._mapClickHandler = function(e) {
                                Alpine.store('incidentModal').open(e.latlng.lat, e.latlng.lng);
                            };
                            window._map.on('click', window._mapClickHandler);
                        }
                    }, 100);
                    
                    document.body.addEventListener('htmx:afterSwap', function(evt) {
                        if (evt.detail.target.id === 'incidents-list') {
                            Alpine.store('incidentModal').close();
                            setTimeout(() => {
                                if (window.refreshIncidents) window.refreshIncidents();
                                if (window.populateDispatchIncidents) window.populateDispatchIncidents();
                            }, 100);
                        }
                    });
                }
            });
        });
    }

    initDispatchModal() {
        document.addEventListener('alpine:init', () => {
            Alpine.store('dispatchModal', {
                isOpen: false,
                open(incidentId = null) {
                    this.isOpen = true;
                    if (incidentId) {
                        document.getElementById('dispatch-incident').value = incidentId;
                    }
                },
                close() {
                    this.isOpen = false;
                }
            });
            
            document.body.addEventListener('htmx:afterSwap', function(evt) {
                if (evt.detail.target.id === 'dispatches-list') {
                    if (window.Alpine && window.Alpine.store('dispatchModal')) {
                        window.Alpine.store('dispatchModal').close();
                    }
                }
            });
        });
    }

    openIncidentModal(lat, lng) {
        if (window.Alpine && window.Alpine.store('incidentModal')) {
            window.Alpine.store('incidentModal').open(lat, lng);
        }
    }

    closeIncidentModal() {
        if (window.Alpine && window.Alpine.store('incidentModal')) {
            window.Alpine.store('incidentModal').close();
        }
    }

    openDispatchModal(incidentId = null) {
        if (window.Alpine && window.Alpine.store('dispatchModal')) {
            window.Alpine.store('dispatchModal').open(incidentId);
        }
    }

    closeDispatchModal() {
        if (window.Alpine && window.Alpine.store('dispatchModal')) {
            window.Alpine.store('dispatchModal').close();
        }
    }

    init() {
        this.initIncidentModal();
        this.initDispatchModal();
    }
}

// Initialize modal manager
const modalManager = new ModalManager();

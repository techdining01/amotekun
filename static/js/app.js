// =====================================
// MAP INITIALIZATION (CLEAN)
// =====================================

const map = L.map('map').setView([7.2, 4.5], 7);

// expose map for testing/debugging (groups exposed after they're created)
window._map = map;

// =====================================
// BASEMAP
// =====================================

const osm = L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        attribution: '&copy; OpenStreetMap contributors'
    }
).addTo(map);



// =====================================
// PERMANENT LAYER GROUPS
// =====================================

const yorubaStatesGroup = L.layerGroup().addTo(map);

const yorubaLgaGroup = L.layerGroup().addTo(map);

// Not added to map by default; controlled via layer controls
const nigeriaLgaGroup = L.layerGroup();

// IncidentGroup removed — cluster group will be used for incident overlays

const heatmapGroup = L.layerGroup();

const intelligenceGroup = L.layerGroup().addTo(map);

const activeStateLgaGroup = L.layerGroup().addTo(map);

// expose groups for testing/debugging
window._yorubaStatesGroup = yorubaStatesGroup;
window._nigeriaLgaGroup = nigeriaLgaGroup;
window._activeStateLgaGroup = activeStateLgaGroup;

// track currently highlighted state name
let currentHighlightedState = null;
// expose test-friendly aliases
window.activeStateLgaGroup = activeStateLgaGroup;
window.currentHighlightedState = currentHighlightedState;


// =====================================
// LAYER CONTROLS
// =====================================

const baseLayers = {
    "OpenStreetMap": osm
};



const overlays = {

    "Yoruba States": yorubaStatesGroup,

    "Yoruba LGAs": yorubaLgaGroup,

    "Nigeria LGAs": nigeriaLgaGroup,

    "Heatmaps": heatmapGroup,

    "Intelligence": intelligenceGroup,

    "Active State/LGA": activeStateLgaGroup
};

const layerControl = L.control.layers(
    baseLayers,
    overlays,
    {
        collapsed: false
    }
).addTo(map);


// =====================================
// CONFIG
// =====================================

const yorubaStates = [
    "Lagos",
    "Ogun",
    "Oyo",
    "Osun",
    "Ondo",
    "Ekiti"
];

// Small UI control: dropdown to pick a Yoruba state (reliable trigger)
const StateSelector = L.Control.extend({
    onAdd: function(map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        container.style.background = '#fff';
        container.style.padding = '6px';
        const select = document.createElement('select');
        select.style.fontSize = '12px';
        select.style.padding = '2px';
        yorubaStates.forEach(s => {
            const o = document.createElement('option');
            o.value = s; o.text = s; select.appendChild(o);
        });
        select.addEventListener('change', (e) => {
            const v = e.target.value;
            if (v) window.highlightStateByName(v);
        });
        container.appendChild(select);
        L.DomEvent.disableClickPropagation(container);
        return container;
    }
});

map.addControl(new StateSelector({ position: 'topright' }));


// =====================================
// 1. YORUBA STATES (ADM1)
// =====================================

fetch('static/data/geoBoundaries-NGA-ADM1_simplified.geojson')
    .then(res => res.json())
    .then(data => {

        const filteredStates = {
            type: "FeatureCollection",
            features: data.features.filter(f =>
                yorubaStates.includes(f.properties.shapeName)
            )
        };

        const layer = L.geoJSON(filteredStates, {
            style: () => ({
                color: "#a1867b",
                weight: 1,
                fillColor: "#90ee90",
                fillOpacity: 0.4
            }),
            onEachFeature: (feature, layer) => {
                const stateName = feature.properties.shapeName;

                layer.bindPopup(`<b>State:</b> ${stateName}`, { autoPan: false });

                // CLICK STATE
                layer.on('click', () => {
                    try {
                        const center = layer.getBounds().getCenter();
                        const targetZoom = 8;
                        map.setView([center.lat, center.lng], targetZoom, { animate: true });
                        setTimeout(() => { try { layer.openPopup(); } catch (e) {} }, 400);
                        try { highlightStateStyles(stateName); } catch (e) {}
                    } catch (e) { console.error('ZOOM ERROR', e); }

                    try { loadStateLGAs(stateName); } catch (e) {}

                    try {
                        const stateBounds = layer.getBounds();
                        setTimeout(() => {
                            nigeriaLgaGroup.eachLayer(l => {
                                try {
                                    if (!l.getBounds) return;
                                    if (l.getBounds().intersects(stateBounds)) {
                                        if (l.setStyle) l.setStyle({ color: "#98a094e8", weight: 1, fillOpacity: 0.12 });
                                    } else {
                                        if (l.setStyle) l.setStyle({ color: "#98a094e8", weight: 1, fillOpacity: 0.03 });
                                    }
                                } catch (e) {}
                            });
                        }, 250);
                    } catch (e) {}
                });
            }
        }).addTo(yorubaStatesGroup);

    }).catch(err => {
        console.error('YORUBA STATES GEOJSON LOAD ERROR:', err);
    });
            

    

// =====================================
// 2. LGAs (ALL + YORUBA FILTERED)
// =====================================

fetch('/static/data/LGA_data.geojson')
    .then(res => res.json())
    .then(data => {

        // -----------------------------
        // ALL LGAs (Nigeria)
        // -----------------------------
        const layer = L.geoJSON(data, {
            style: {
                color: "#98a094e8",
                weight: 1,
                fillOpacity: 0.05
            }
        }).addTo(nigeriaLgaGroup);


        // -----------------------------
        // YORUBA LGAs ONLY
        // -----------------------------
        fetch('/api/yoruba-lgas/')
            .then(res => res.json())
            .then(data => {

                console.log("YORUBA LGA DATA:", data);

                data.features.forEach((feature, index) => {

                    try {

                        L.geoJSON(feature, {

                            style: {
                                color: "#98a094e8",
                                weight: 1,
                                fillOpacity: 0.12
                            }

                        }).addTo(yorubaLgaGroup);

                    } catch (err) {

                        console.error(
                            "BROKEN FEATURE:",
                            index,
                            feature,
                            err
                        );

                    }

                });

            });

        // =====================================
        // 4. INCIDENTS / REPORTS LAYER
        // =====================================

        const incidentClusterGroup = L.markerClusterGroup({
            chunkedLoading: true,
            spiderfyOnMaxZoom: true,
            showCoverageOnHover: false,
            maxClusterRadius: 60
        });

        // Add to overlays for layer control and register with the control
        overlays["Incident Clusters"] = incidentClusterGroup;

        // add to map immediately (IMPORTANT)
        map.addLayer(incidentClusterGroup);

        // update the layers control UI so these overlays appear
        layerControl.addOverlay(incidentClusterGroup, "Incident Clusters");
        


        // Heatmaps and intelligence layers 

        const heatData = [];

        const heatLayer = L.heatLayer(heatData, {
            radius: 25,
            blur: 18,
            maxZoom: 12
        });

        // add heatLayer to heatmapGroup, then add group to map
        heatmapGroup.addLayer(heatLayer);
        map.addLayer(heatmapGroup);

        // NOTE: heatLayer is already in `heatmapGroup` which is added to the map

        // Fetch reports once and use for both clusters and heatmap
        fetch('/api/incidents/')
            .then(response => response.json())
            .then(data => {

                console.log("REPORT DATA:", data);

                data.features.forEach(feature => {

                    const coords = feature.geometry.coordinates;

                    // GeoJSON = [lng, lat]
                    const lat = coords[1];
                    const lng = coords[0];

                    // Incident cluster marker
                    const marker = L.marker([lat, lng]);

                    marker.bindPopup(`
            <b>${feature.properties.title}</b><br>
            ${feature.properties.description}<br>
            <b>Type:</b> ${feature.properties.report_type}
        `);

                    incidentClusterGroup.addLayer(marker);

                    // Heatmap data
                    // i will increase intensity later
                    heatData.push([lat, lng, 1]);
                });

                // IMPORTANT: refresh heat layer after data loads
                heatLayer.setLatLngs(heatData);

            })
            .catch(error => {
                console.error("REPORTS/HEATMAP ERROR:", error);
            }); 
        })

        // Helper to recurse into a layer and its sublayers
        function _recurseLayers(layer, cb) {
            try { cb(layer); } catch (e) {}
            try { if (layer.getLayers) layer.getLayers().forEach(sub => _recurseLayers(sub, cb)); } catch (e) {}
        }

        // Reset function to restore default styles for LGAs and states
        function resetHighlights() {
            try {
                nigeriaLgaGroup.eachLayer(l => {
                    if (l.setStyle) l.setStyle({ color: "#98a094e8", weight: 1, fillOpacity: 0.05 });
                });
            } catch (e) {}

            try {
                yorubaLgaGroup.eachLayer(l => {
                    if (l.setStyle) l.setStyle({ color: "#98a094e8", weight: 1, fillOpacity: 0.12 });
                });
            } catch (e) {}

            try {
                yorubaStatesGroup.eachLayer(s => _recurseLayers(s, layer => {
                    if (layer.setStyle) layer.setStyle({ fillColor: "#90ee90", fillOpacity: 0.4, color: "#a1867b", weight: 1 });
                }));
            } catch (e) {}

            try { currentHighlightedState = null; window.currentHighlightedState = null; } catch (e) {}
        }

        // Highlight the specified Yoruba state and dim others (recurses into FeatureGroups)
        function highlightStateStyles(name) {
            try {
                yorubaStatesGroup.eachLayer(s => _recurseLayers(s, layer => {
                    try {
                        const props = layer.feature && layer.feature.properties;
                        if (props && props.shapeName === name) {
                            if (layer.setStyle) layer.setStyle({ fillColor: "#ffa500", fillOpacity: 0.45, color: "#cc5500", weight: 2 });
                        } else {
                            if (layer.setStyle) layer.setStyle({ fillColor: "#90ee90", fillOpacity: 0.15, color: "#a1867b", weight: 1 });
                        }
                    } catch (e) {}
                }));
            } catch (e) {}
        }

        // Load LGAs for a state into `activeStateLgaGroup`
        function loadStateLGAs(stateName) {
            try { activeStateLgaGroup.clearLayers(); } catch (e) {}

            fetch(`/api/state-lgas/${stateName}/`)
                .then(res => res.json())
                .then(data => {
                    const lgaLayer = L.geoJSON(data, {
                        style: {
                            color: "#ff7800",
                            weight: 2,
                            fillOpacity: 0.2
                        },
                        onEachFeature: (feature, layer) => {
                            layer.bindPopup(`<b>LGA:</b> ${feature.properties.name}`);
                        }
                    });

                    activeStateLgaGroup.addLayer(lgaLayer);
                    // dim others by bounds intersection
                    try {
                        const stateLayer = (function findLayer(){
                            let found = null;
                            const search = (layer) => {
                                try {
                                    const props = layer.feature && layer.feature.properties;
                                    if (props && props.shapeName === stateName) { found = layer; return; }
                                } catch (e) {}
                                try { if (layer.getLayers) layer.getLayers().forEach(search); } catch (e) {}
                            };
                            yorubaStatesGroup.eachLayer(l => search(l));
                            return found;
                        })();

                        if (stateLayer) {
                            const stateBounds = stateLayer.getBounds();
                            setTimeout(() => {
                                nigeriaLgaGroup.eachLayer(l => {
                                    try {
                                        if (!l.getBounds) return;
                                        if (l.getBounds().intersects(stateBounds)) {
                                            if (l.setStyle) l.setStyle({ color: "#98a094e8", weight: 1, fillOpacity: 0.12 });
                                        } else {
                                            if (l.setStyle) l.setStyle({ color: "#98a094e8", weight: 1, fillOpacity: 0.03 });
                                        }
                                    } catch (e) {}
                                });
                            }, 200);
                        }
                    } catch (e) {}

                    currentHighlightedState = stateName;
                    try { window.currentHighlightedState = currentHighlightedState; } catch (e) {}
                })
                .catch(err => {
                    console.error("STATE LGA LOAD ERROR:", err);
                });
        }

        // clicking on the map: detect which state (if any) contains the click and highlight/load LGAs
        map.on('click', (e) => {
            try {
                const latlng = e.latlng;
                let clickedState = null;
                let clickedLayer = null;

                const search = (layer) => {
                    try {
                        const props = layer.feature && layer.feature.properties;
                        if (props && props.shapeName) {
                            // use turf.booleanPointInPolygon when available for robust point-in-polygon
                            try {
                                if (typeof turf !== 'undefined' && layer.feature) {
                                    const pt = turf.point([latlng.lng, latlng.lat]);
                                    if (turf.booleanPointInPolygon(pt, layer.feature)) {
                                        clickedState = props.shapeName;
                                        clickedLayer = layer;
                                        return;
                                    }
                                } else if (layer.getBounds && layer.getBounds().contains(latlng)) {
                                    // fallback to bounds containment
                                    clickedState = props.shapeName;
                                    clickedLayer = layer;
                                    return;
                                }
                            } catch (e) {}
                        }
                    } catch (e) {}
                    try { if (layer.getLayers) layer.getLayers().forEach(search); } catch (e) {}
                };

                yorubaStatesGroup.eachLayer(l => search(l));

                if (!clickedState) {
                    // fallback: choose nearest state's centroid if click is close to a state
                    try {
                        const cp = e.containerPoint;
                        let minDist = Infinity;
                        let nearest = null;
                        yorubaStatesGroup.eachLayer(l => _recurseLayers(l, layer => {
                            try {
                                const props = layer.feature && layer.feature.properties;
                                if (props && props.shapeName) {
                                    const c = layer.getBounds().getCenter();
                                    const p = window._map.latLngToContainerPoint([c.lat, c.lng]);
                                    const d = Math.hypot(p.x - cp.x, p.y - cp.y);
                                    if (d < minDist) { minDist = d; nearest = { name: props.shapeName, layer }; }
                                }
                            } catch (e) {}
                        }));

                        // pixel threshold: 50px
                        if (nearest && minDist <= 50) {
                            clickedState = nearest.name;
                            clickedLayer = nearest.layer;
                        }
                    } catch (e) {}
                }

                if (clickedState) {
                    // if a different state, highlight and load LGAs
                    if (currentHighlightedState !== clickedState) {
                        highlightStateStyles(clickedState);
                        loadStateLGAs(clickedState);
                    } else {
                        // same state clicked: ensure LGAs shown
                        if (!activeStateLgaGroup.getLayers().length) loadStateLGAs(clickedState);
                    }
                } else {
                    // clicked outside any state polygon: clear selection
                    resetHighlights();
                    try { activeStateLgaGroup.clearLayers(); } catch (e) {}
                    currentHighlightedState = null;
                }
            } catch (e) {}
        });


        // Expose helper for automated testing: trigger a state click by name
        window.highlightStateByName = function(name) {
            let found = false;
            try {
                const searchLayer = (layer) => {
                    try {
                        const props = layer.feature && layer.feature.properties;
                        if (props && props.shapeName === name) {
                            found = true;
                            try {
                                const center = layer.getBounds().getCenter();
                                const targetZoom = 8;
                                window._map.setView([center.lat, center.lng], targetZoom, { animate: true });
                                setTimeout(() => { try { if (layer.openPopup) layer.openPopup(); } catch (e) {} }, 400);
                                try { highlightStateStyles(name); } catch (e) {}
                                try { loadStateLGAs(name); } catch (e) {}
                            } catch (e) {}
                            return;
                        }
                    } catch (e) {}

                    // recurse into sublayers (FeatureGroup/LayerGroup)
                    try {
                        if (layer.getLayers) {
                            layer.getLayers().forEach(sub => searchLayer(sub));
                        }
                    } catch (e) {}
                };

                yorubaStatesGroup.eachLayer(layer => searchLayer(layer));
            } catch (e) {}
            return found;
        };

    
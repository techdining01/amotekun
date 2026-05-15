// =====================================
// MAP INITIALIZATION (CLEAN)
// =====================================

const map = L.map('map').setView([7.2, 4.5], 7);

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

const nigeriaLgaGroup = L.layerGroup();

const reportsGroup = L.layerGroup().addTo(map);

const heatmapGroup = L.layerGroup();

const intelligenceGroup = L.layerGroup();


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

    "Reports": reportsGroup,

    "Heatmaps": heatmapGroup,

    "Intelligence": intelligenceGroup
};

L.control.layers(
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

    const layer =L.geoJSON(filteredStates, {
        style: () => ({
            color: "#006400",
            weight: 1,
            fillColor: "#90ee90",
            fillOpacity: 0.4
        }),
        onEachFeature: (feature, layer) => {
            layer.bindPopup(
                `<b>State:</b> ${feature.properties.shapeName}`
            );
        }
    }).addTo(yorubaStatesGroup);

})
.catch(err => console.error("STATES ERROR:", err));

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
            const layer = L.geoJSON(data, {

                style: {
                    color: 'orange',
                    weight: 1,
                    fillColor: 'yellow',
                    fillOpacity: 0.5
                },

                onEachFeature: (feature, layer) => {

                    layer.bindPopup(`
                        <b>LGA:</b> ${feature.properties.name}
                    `);

                }

            }).addTo(yorubaLgaGroup);
            map.fitBounds(layer.getBounds());

        })
        .catch(err => console.error(
            "YORUBA LGA ERROR:",
            err
        ));


// =====================================
// 4. INCIDENTS / REPORTS LAYER
// =====================================

fetch('/api/reports/')
.then(res => res.json())
.then(data => {

    const layer = L.geoJSON(data, {

        pointToLayer: (feature, latlng) => {

            return L.marker(latlng);

        },

        onEachFeature: (feature, layer) => {

            layer.bindPopup(`
                <b>${feature.properties.title}</b><br>
                ${feature.properties.description}
            `);

        }

    }).addTo(reportsGroup);

});
})
.catch(err => console.error("LGA ERROR:", err));
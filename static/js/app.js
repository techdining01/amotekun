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
// LAYER GROUPS
// =====================================

const yorubaStatesGroup = L.layerGroup();

const yorubaLgaGroup = L.layerGroup();

const nigeriaLgaGroup = L.layerGroup();

const reportsGroup = L.layerGroup();

const heatmapGroup = L.layerGroup();

const intelligenceGroup = L.layerGroup();


yorubaStatesGroup.addTo(map);

yorubaLgaGroup.addTo(map);

reportsGroup.addTo(map);



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

    const yorubaStatesLayer = L.geoJSON(filteredStates, {
        style: () => ({
            color: "#006400",
            weight: 2,
            fillColor: "#90ee90",
            fillOpacity: 0.4
        }),
        onEachFeature: (feature, layer) => {
            layer.bindPopup(
                `<b>State:</b> ${feature.properties.shapeName}`
            );
        }
    }).addTo(yorubaStatesGroup);

    map.fitBounds(yorubaStatesLayer.getBounds());
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
    const allLgaLayer = L.geoJSON(data, {
        style: {
            color: "#98a094e8",
            weight: 1,
            fillOpacity: 0.05
        }
    });

    // -----------------------------
    // YORUBA LGAs ONLY
    // -----------------------------
    fetch('/api/yoruba-lgas/')
    .then(res => res.json())
    .then(data => {

        const yorubaLgaLayer = L.geoJSON(data, {

            style: {
                color: 'orange',
                weight: 1,
                fillColor: 'yellow',
                fillOpacity: 0.2
            },

            onEachFeature: (feature, layer) => {

                layer.bindPopup(`
                    <b>LGA:</b> ${feature.properties.name}
                `);

            }

        }).addTo(yorubaLgaGroup);

    });

    // // -----------------------------
    // // LAYER CONTROL (SAFE)
    // // -----------------------------
    // L.control.layers(
    //     {
    //         "OpenStreetMap": osm
    //     },
    //     {
    //         "Yoruba States": statesLayer,
    //         "Yoruba LGAs": yorubaLgaLayer,
    //         "All LGAs (Nigeria)": allLgaLayer
    //     }
    // ).addTo(map);

})
.catch(err => console.error("LGA ERROR:", err));

// =====================================
// 3. USER LOCATION (GPS)
// =====================================

// if (navigator.geolocation) {

//     navigator.geolocation.getCurrentPosition(
//         (position) => {

//             const lat = position.coords.latitude;
//             const lng = position.coords.longitude;

//             console.log("USER LOCATION:", lat, lng);

//             map.setView([lat, lng], 12);

//             L.marker([lat, lng])
//                 .addTo(map)
//                 .bindPopup("Your Location")
//                 .openPopup();

//             L.circle([lat, lng], {
//                 radius: position.coords.accuracy,
//                 color: "blue",
//                 fillColor: "rgb(134, 236, 108)",
//                 fillOpacity: 0.2
//             }).addTo(map);
//         },
//         (error) => {
//             console.error("GEO ERROR:", error);
//         }
//     );
// }

// navigator.geolocation.getCurrentPosition(

//     successCallback,

//     errorCallback,

//     {
//         enableHighAccuracy: true,
//         timeout: 10000,
//         maximumAge: 0
//     }
// );

// =====================================
// 4. INCIDENTS / REPORTS LAYER
// =====================================

fetch('/api/reports/')
.then(res => {
    if (!res.ok) throw new Error("Network response not OK");
    return res.json();
})
.then(data => {

    console.log("REPORT DATA:", data);

    const reportsLayer = L.geoJSON(data, {

        pointToLayer: (feature, latlng) =>
            L.marker(latlng),

        onEachFeature: (feature, layer) => {

            layer.bindPopup(`
                <b>${feature.properties.title}</b><br>
                ${feature.properties.description}<br>
                <b>Type:</b> ${feature.properties.report_type}
            `);
        }
    }).addTo(reportsGroup);

})
.catch(err => console.error("REPORT ERROR:", err));


// =====================================
// LAYER CONTROLS
// =====================================

const baseLayers = {
    "OpenStreetMap": osm
};

const overlayLayers = {

    "Yoruba States": yorubaStatesGroup,

    "Yoruba LGAs": yorubaLgaGroup,

    "Nigeria LGAs": nigeriaLgaGroup,

    "Incident Reports": reportsGroup,

    "Heatmaps": heatmapGroup,

    "Intelligence": intelligenceGroup
};

L.control.layers(
    baseLayers,
    overlayLayers,
    {
        collapsed: false
    }
).addTo(map);
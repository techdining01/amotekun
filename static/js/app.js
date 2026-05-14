
// =====================================
// INITIALIZE MAP
// =====================================

const map = L.map('map').setView([7.2, 4.5], 7);

// let statesLayer;

// let lgaLayer;

// let incidentsLayer;


// =====================================
// BASEMAP
// =====================================

const osm = L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        attribution: '&copy; OpenStreetMap contributors'
    }
);

osm.addTo(map);


// =====================================
// YORUBA STATES
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
// STATES LAYER
// =====================================

let statesLayer;


// Load ADM1 states GeoJSON
fetch('static/data/geoBoundaries-NGA-ADM1_simplified.geojson')

.then(response => response.json())

.then(data => {

    // Filter Yoruba states
    const filteredStates = {

        type: "FeatureCollection",

        features: data.features.filter(feature => {

            return yorubaStates.includes(
                feature.properties.shapeName
            );

        })

    };


    // Create GeoJSON layer
    statesLayer = L.geoJSON(filteredStates, {

        style: function(feature) {

            return {
                color: "green",
                weight: 2,
                fillColor: "lightgreen",
                fillOpacity: 0.4
            };

        },


        onEachFeature: function(feature, layer) {

            layer.bindPopup(`
                <b>State:</b>
                ${feature.properties.shapeName}
            `);

        }

    }).addTo(map);


    // Zoom map to Yoruba states
    map.fitBounds(statesLayer.getBounds());

})

.catch(error => {

    console.error(
        'Error loading states GeoJSON:',
        error
    );

});



// =====================================
// LGA LAYER
// =====================================

let lgaLayer;

fetch('/static/data/LGA_data.geojson')

.then(response => response.json())

.then(data => {

    console.log('LGA DATA:', data);

    lgaLayer = L.geoJSON(data, {

        style: function(feature) {

            return {

                color: 'orange',

                weight: 1,

                fillColor: 'yellow',

                fillOpacity: 0.05

            };

        },

        onEachFeature: function(feature, layer) {

            layer.bindPopup(`

                <b>LGA:</b>

                ${feature.properties.shapeName}

            `);

        }

    }).addTo(map);


    // Add layer control ONLY after layer exists
    L.control.layers(

        {
            'OpenStreetMap': osm
        },

        {
            'LGAs': lgaLayer
        }

    ).addTo(map);

})

.catch(error => {

    console.error(
        'LGA FETCH ERROR:',
        error
    );

const yorubaStates = [

    'Lagos',
    'Ogun',
    'Oyo',
    'Osun',
    'Ondo',
    'Ekiti'

];

const filteredFeatures = data.features.filter(feature => {

    return yorubaStates.includes(
        feature.properties.shapeGroup
    );

});



});



// =====================================
// CURRENT GPS LOCATION
// =====================================

navigator.geolocation.getCurrentPosition(

    function(position) {

        const lat = position.coords.latitude;

        const lng = position.coords.longitude;


        // User marker
        const userMarker = L.marker([lat, lng])

            .addTo(map)

            .bindPopup('ibadan')


        // Accuracy circle
        const accuracyCircle = L.circle([lat, lng], {

            radius: position.coords.accuracy,

            color: 'blue',

            fillColor: '#30f',

            fillOpacity: 0.2

        }).addTo(map);

    },

    function(error) {

        console.error(
            'Geolocation error:',
            error
        );

    }

);


// =====================================
// LAYER CONTROLS
// =====================================

const baseLayers = {
    "OpenStreetMap": osm
};


const overlays = {
    "States": statesLayer,
    "LGAs": lgaLayer,
    
};


L.control.layers(
    baseLayers,
    overlays
).addTo(map);




// =====================================
// REPORTS LAYER
// =====================================

fetch('/api/reports/')

.then(response => response.json())

.then(data => {

    console.log('REPORT DATA:', data);

    L.geoJSON(data, {

        pointToLayer: function(feature, latlng) {

            return L.marker(latlng);

        },

        onEachFeature: function(feature, layer) {

            layer.bindPopup(`

                <b>${feature.properties.title}</b><br>

                ${feature.properties.description}<br>

                <b>Type:</b>

                ${feature.properties.incident_type}

            `);

        }

    }).addTo(map);

})

.catch(error => {

    console.error(
        'Incident fetch error:',
        error
    );

});


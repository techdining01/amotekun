let incidentLayer;

async function loadIncidents(){

    const response=await fetch(
        "/api/dashboard/incidents/"
    );

    const data=await response.json();

    if(incidentLayer){

        incidentLayer.clearLayers();

    }else{

        incidentLayer=L.layerGroup().addTo(map);

        layerControl.addOverlay(
            incidentLayer,
            "Incidents"
        );

    }

    data.forEach((incident)=>{

        if(
            !incident.latitude ||
            !incident.longitude
        ){

            return;

        }

        L.marker([
            incident.latitude,
            incident.longitude
        ])

        .bindPopup(

            `
            <strong>${incident.title}</strong><br>
            ${incident.status}
            `

        )

        .addTo(incidentLayer);

    });

}

// Register incidents layer with registry

layerRegistry.add("incidents",{

    loader:loadIncidents,

    refreshInterval:30000,

    defaultVisible:true,

    roles:[

        "SUPER_ADMIN",

        "ADMIN",

        "POLICE",

        "AMOTEKUN",

        "DISPATCHER",

        "ANALYST",
        
        "RESPONDER"

    ]

});
let facilityLayer;

async function loadFacilities(){

    const response=await fetch(

        "/api/dashboard/facilities/"

    );

    const data=await response.json();

    if(facilityLayer){

        facilityLayer.clearLayers();

    }

    else{

        facilityLayer=L.layerGroup().addTo(map);

        layerControl.addOverlay(

            facilityLayer,

            "Facilities"

        );

    }

    data.forEach((facility)=>{

        L.circleMarker(

            [

                facility.latitude,

                facility.longitude

            ],

            {

                radius:7

            }

        )

        .bindPopup(

            facility.name

        )

        .addTo(facilityLayer);

    });

}

// Register facilities layer with registry

layerRegistry.add("facilities",{

    loader:loadFacilities,

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

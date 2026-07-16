let patrolLayer;

async function loadPatrols(){

    const response=await fetch(

        "/api/dashboard/patrols/"

    );

    const data=await response.json();

    if(patrolLayer){

        patrolLayer.clearLayers();

    }

    else{

        patrolLayer=L.layerGroup().addTo(map);

        layerControl.addOverlay(

            patrolLayer,

            "Patrols"

        );

    }

    data.forEach((patrol)=>{

        if(
            !patrol.latitude ||
            !patrol.longitude
        ){

            return;

        }

        L.marker([

            patrol.latitude,

            patrol.longitude

        ])

        .bindPopup(

            patrol.code

        )

        .addTo(

            patrolLayer

        );

    });

}

// Register patrol layer with registry

layerRegistry.add("patrols",{

    loader:loadPatrols,

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

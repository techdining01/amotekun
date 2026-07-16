let stateLayer;

async function loadStates(){

    const response=await fetch(

        "/api/dashboard/states/"

    );

    const geojson=await response.json();

    if(stateLayer){

        map.removeLayer(stateLayer);

    }

    stateLayer=L.geoJSON(

        geojson,

        {

            style:{

                color:"#2563eb",

                weight:2,

                fillOpacity:0.05,

            }

        }

    );

    stateLayer.addTo(map);

    layerControl.addOverlay(

        stateLayer,

        "States"

    );

}

// Register states layer with registry

layerRegistry.add("states",{

    loader:loadStates,

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
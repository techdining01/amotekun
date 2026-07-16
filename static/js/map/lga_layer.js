let lgaLayer;

async function loadLGAs(){

    const response=await fetch(

        "/api/dashboard/lgas/"

    );

    const geojson=await response.json();

    if(lgaLayer){

        map.removeLayer(lgaLayer);

    }

    lgaLayer=L.geoJSON(

        geojson,

        {

            style:{

                color:"#16a34a",

                weight:1,

            }

        }

    );

    layerControl.addOverlay(

        lgaLayer,

        "LGAs"

    );

}

// Register LGAs layer with registry

layerRegistry.add("lgas",{

    loader:loadLGAs,

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
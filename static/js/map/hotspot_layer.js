let hotspotLayer;

async function loadHotspots(){

    const response=await fetch(

        "/api/dashboard/hotspots/"

    );

    const hotspots=await response.json();

    if(hotspotLayer){

        hotspotLayer.clearLayers();

    }

    else{

        hotspotLayer=L.layerGroup().addTo(map);

    }

    hotspots.forEach(h=>{

        L.circle([

            h.latitude,

            h.longitude

        ],{

            radius:1000,

        })

        .bindPopup(

            "Risk Score : "+h.risk

        )

        .addTo(hotspotLayer);

    });

}

// Register hotspot layer with registry

layerRegistry.add("hotspots",{

    loader:loadHotspots,

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

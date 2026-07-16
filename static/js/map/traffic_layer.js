let trafficLayer;

async function loadTraffic(){

    const response=await fetch(

        "/api/dashboard/traffic/"

    );

    const traffic=await response.json();

    if(trafficLayer){

        trafficLayer.clearLayers();

    }

    else{

        trafficLayer=L.layerGroup().addTo(map);

    }

    traffic.forEach(item=>{

        L.circleMarker([

            item.latitude,

            item.longitude

        ])

        .bindPopup(

            "Speed : "+item.speed

        )

        .addTo(trafficLayer);

    });

}

// Register traffic layer with registry

layerRegistry.add("traffic",{

    loader:loadTraffic,

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
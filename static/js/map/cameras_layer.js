let cameraLayer;

async function loadCameras(){

    const response=await fetch(

        "/api/dashboard/cameras/"

    );

    const cameras=await response.json();

    if(cameraLayer){

        cameraLayer.clearLayers();

    }

    else{

        cameraLayer=L.layerGroup().addTo(map);

    }

    cameras.forEach(camera=>{

        L.marker([

            camera.lat,

            camera.lng

        ])

        .bindPopup(

            `<strong>${camera.name}</strong><br>${camera.status}`

        )

        .addTo(cameraLayer);

    });

}

// Register cameras layer with registry

layerRegistry.add("cameras",{

    loader:loadCameras,

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
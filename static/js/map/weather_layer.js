let weatherLayer;

async function loadWeather(){

    const response=await fetch(

        "/api/dashboard/weather/"

    );

    const weather=await response.json();

    console.log(weather);

}

// Register weather layer with registry

layerRegistry.add("weather",{

    loader:loadWeather,

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
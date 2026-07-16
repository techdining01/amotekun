let map;

let layerControl;

function initializeDashboardMap(
    elementId = "dashboard-map"
){

    map = L.map(elementId,{

        zoomControl:true,

        preferCanvas:true,

    });

    map.setView([8.8,8.0],6);

    L.tileLayer(

        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

        {

            maxZoom:19,

            attribution:"© OpenStreetMap"

        }

    ).addTo(map);

    layerControl=L.control.layers().addTo(map);

}


document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        if(
            document.getElementById(
                "dashboard-map"
            )
        ){

            initializeDashboardMap();

            loadIncidents();

            loadFacilities();

            loadPatrols();

            loadStates();

            loadLGAs();

            loadCameras();

            loadHotspots();

            loadTraffic();

            loadWeather();

        }

    }

);

window.layerManager=new LayerManager(map);

layerManager.register(

    "incidents",

    incidentLayer

);

permissionManager=new MapPermissionManager(

    document.body.dataset.role

);

permissionManager.initialize();

refreshManager.start();
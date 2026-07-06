
// <!-- ====================================================== -->
// <!-- HTMX EVENTS -->
// <!-- ====================================================== -->

document.body.addEventListener("htmx:beforeRequest",function(){

    document.getElementById("htmx-indicator")?.classList.remove("hidden");

});

document.body.addEventListener("htmx:afterRequest",function(){

    document.getElementById("htmx-indicator")?.classList.add("hidden");

});

document.body.addEventListener("htmx:responseError",function(){

    document.getElementById("htmx-indicator")?.classList.add("hidden");

});

document.body.addEventListener("htmx:sendError",function(){

    document.getElementById("htmx-indicator")?.classList.add("hidden");

});


// <!-- ====================================================== -->
// <!-- CSRF FOR HTMX -->
// <!-- ====================================================== -->

document.body.addEventListener("htmx:configRequest",function(event){

    event.detail.headers["X-CSRFToken"]="{{ csrf_token }}";

});



//  ====================================================== -->
//  HTMX GLOBAL EVENTS -->
//  ====================================================== -->



document.body.addEventListener(

    "htmx:beforeRequest",

    () => {

        document.dispatchEvent(

            new CustomEvent("dashboard-loading-start")

        );

    }

);

document.body.addEventListener(

    "htmx:afterSwap",

    () => {

        document.dispatchEvent(

            new CustomEvent("dashboard-loading-stop")

        );

    }

);

document.addEventListener(

    "dashboard-loading-start",

    () => {

        const root = document.querySelector("[x-data]");

        if (root && root._x_dataStack) {

            root._x_dataStack[0].loading = true;

        }

    }

);

document.addEventListener(

    "dashboard-loading-stop",

    () => {

        const root = document.querySelector("[x-data]");

        if (root && root._x_dataStack) {

            root._x_dataStack[0].loading = false;

        }

    }

);








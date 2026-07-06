

// document.addEventListener("alpine:init", () => {

//     Alpine.store("dashboard", {

//         sidebarOpen: false,

//         notificationOpen: false,

//         profileOpen: false,

//         commandPalette: false,

//         darkMode: false,

//         loading: false,

//         refreshDashboard(){},

//         toggleSidebar(){},

//         toggleCommandPalette(){},

//         toggleFullscreen(){},

//     });

//     Alpine.data("dashboardLayout", () => ({

//         init(){

//             console.log("Dashboard Ready");

//         }

//     }));

// });


    //     /* ==============================
    //        LOADING
    //     ============================== */

    //     function startLoading() {

    //         this.loading = true;

    //     }

    //     function stopLoading() {

    //         this.loading = false;

    //     }

    //     /* ==============================
    //        RESPONSIVE
    //     ============================== */

    //    function registerResizeListener() {

    //         window.addEventListener(

    //             "resize",

    //             () => {

    //                 if (window.innerWidth >= 1024) {

    //                     this.sidebarOpen = true;

    //                 }

    //             }

    //         );

    //     }

function refreshDashboard() {

    htmx.trigger(document.body, "refresh-dashboard")

}

function toggleFullscreen() {

    if (!document.fullscreenElement) {

        document.documentElement.requestFullscreen()

    } else {

        document.exitFullscreen()

    }

}

function toggleCommandPalette(){

    this.commandPalette=!this.commandPalette

}


//  ====================================================== -->
//  DASHBOARD LAYOUT STORE -->
//  ====================================================== -->


document.addEventListener("alpine:init", () => {

    Alpine.data("dashboardLayout", () => ({

        /* ==============================
           GLOBAL UI
        ============================== */

        sidebarOpen: window.innerWidth >= 1024,

        loading: false,

        darkMode: false,

        notificationCount: 0,

        notificationsOpen: false,

        profileOpen: false,

        commandPalette: false,

        searchOpen: false,

        soundEnabled: true,

        /* ==============================
           INITIALIZE
        ============================== */

        init() {

            this.restoreTheme();

            this.restoreSidebar();

            this.restoreSound();

            this.registerKeyboardShortcuts();

            this.registerResizeListener();

            this.bootstrapNotifications();

        },

        /* ==============================
           SIDEBAR
        ============================== */

        toggleSidebar() {

            this.sidebarOpen = !this.sidebarOpen;

            localStorage.setItem(
                "sidebar-open",
                this.sidebarOpen
            );

        },

        closeSidebar() {

            if (window.innerWidth < 1024) {

                this.sidebarOpen = false;

            }

        },

        restoreSidebar() {

            if (window.innerWidth >= 1024) {

                this.sidebarOpen = true;

                return;

            }

            const state = localStorage.getItem("sidebar-open");

            this.sidebarOpen = state === "true";

        },

        /* ==============================
           THEME
        ============================== */

        toggleTheme() {

            this.darkMode = !this.darkMode;

            document.documentElement.classList.toggle(
                "dark",
                this.darkMode
            );

            localStorage.setItem(
                "dark-mode",
                this.darkMode
            );

        },

        restoreTheme() {

            this.darkMode =
                localStorage.getItem("dark-mode") === "true";

            document.documentElement.classList.toggle(
                "dark",
                this.darkMode
            );
        },
        ToggleCommandPalette(){
            this.commandPalette = !this.commandPalette;
            localStorage.setItem(
                "command-palette",
                this.commandPalette
            );
        },

        toggleFullscreen(){
            this.fullscreen = !this.fullscreen;
            localStorage.setItem(
                "fullscreen",
                this.fullscreen
            );
        },
    }));
});


/* ==============================
KEYBOARD SHORTCUTS
============================== */

function registerKeyboardShortcuts() {

window.addEventListener(

    "keydown",

    (event) => {

        /* CTRL + K */

        if (

            event.ctrlKey &&

            event.key.toLowerCase() === "k"

        ) {

            event.preventDefault();

            this.commandPalette =
                !this.commandPalette;

        }

        /* ESC */

        if (event.key === "Escape") {

            this.notificationsOpen = false;

            this.profileOpen = false;

            this.commandPalette = false;

            this.closeSidebar();

        }

        /* ALT + S */

        if (

            event.altKey &&

            event.key.toLowerCase() === "s"

        ) {

            event.preventDefault();

            this.toggleSidebar();

        }

    }

);

}


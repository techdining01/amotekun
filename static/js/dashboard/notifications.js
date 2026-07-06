
//  =====================================================
//  TOAST HELPER 
// ======================================================


function showToast(message,type="success"){

    const container=document.getElementById("toast-container");

    const toast=document.createElement("div");

    toast.className=

    `pointer-events-auto
     rounded-xl
     shadow-xl
     border
     bg-white
     p-4
     animate-in
     slide-in-from-right`;

    toast.innerHTML=`

        <div class="font-semibold">

            ${message}

        </div>

    `;

    container.appendChild(toast);

    setTimeout(()=>{

        toast.remove();

    },4000);

}



/* ==============================
    SOUND
============================== */

function toggleSound() {

    this.soundEnabled = !this.soundEnabled;

    localStorage.setItem(
        "sound-enabled",
        this.soundEnabled
    );

    if (window.soundAlerts) {

        window.soundAlerts.enabled =
            this.soundEnabled;

    }

}

function restoreSound() {

    const state = localStorage.getItem("sound-enabled");

    if (state !== null) {

        this.soundEnabled = state === "true";

    }

    if (window.soundAlerts) {

        window.soundAlerts.enabled =
            this.soundEnabled;

    }

}

/* ==============================
    NOTIFICATIONS
============================== */

function toggleNotifications() {

    this.notificationsOpen =
        !this.notificationsOpen;

}

async function bootstrapNotifications() {

    if (!window.notificationClient) return;

    try {

        await notificationClient.initialize();

        this.notificationCount =
            notificationClient.unreadCount || 0;

    }

    catch (e) {

        console.warn(e);

    }

}

function markAllRead() {

    if (!window.notificationClient) return;

    notificationClient
        .markAllAsRead()
        .finally(() => {

            this.notificationCount = 0;

        });

}

/* ==============================
    PROFILE
============================== */

function toggleProfile() {

    this.profileOpen =
        !this.profileOpen;

}
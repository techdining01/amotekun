// HTMX indicator — thin top bar only, never the full-page overlay
document.body.addEventListener("htmx:beforeRequest", function (e) {
    // Only show the top bar for non-polling requests (user-initiated)
    const trigger = e.detail.requestConfig?.triggerSpec?.trigger;
    const isPolling = trigger === "every" || (e.detail.elt?.getAttribute("hx-trigger") || "").includes("every");
    if (!isPolling) {
        document.getElementById("htmx-indicator")?.classList.remove("hidden");
    }
});

document.body.addEventListener("htmx:afterRequest", function () {
    document.getElementById("htmx-indicator")?.classList.add("hidden");
});

document.body.addEventListener("htmx:responseError", function () {
    document.getElementById("htmx-indicator")?.classList.add("hidden");
});

document.body.addEventListener("htmx:sendError", function () {
    document.getElementById("htmx-indicator")?.classList.add("hidden");
});

// CSRF token injection
document.body.addEventListener("htmx:configRequest", function (event) {
    const token = document.cookie.split(";")
        .map(c => c.trim())
        .find(c => c.startsWith("csrftoken="))
        ?.split("=")[1];
    if (token) event.detail.headers["X-CSRFToken"] = token;
});

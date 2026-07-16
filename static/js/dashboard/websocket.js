(() => {
    const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
    if (!isAuthenticated) return;

    let ws = null;
    let pingInterval = null;
    let reconnectTimeout = null;
    let reconnectDelay = 2000;
    const MAX_DELAY = 30000;

    function connect() {
        const proto = location.protocol === 'https:' ? 'wss' : 'ws';
        ws = new WebSocket(`${proto}://${location.host}/ws/notifications/`);

        ws.onopen = () => {
            reconnectDelay = 2000;
            // Ping every 25s to keep Redis connection alive
            pingInterval = setInterval(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'ping' }));
                }
            }, 25000);
        };

        ws.onmessage = (e) => {
            try {
                const data = JSON.parse(e.data);
                if (data.type === 'unread_count') {
                    updateBadge(data.count);
                } else if (data.type === 'notification') {
                    showToast(data.notification);
                    incrementBadge();
                    if (typeof soundAlerts !== 'undefined') {
                        soundAlerts.playForNotification(data.notification);
                    }
                }
            } catch (_) {}
        };

        ws.onclose = () => {
            clearInterval(pingInterval);
            reconnectTimeout = setTimeout(() => {
                reconnectDelay = Math.min(reconnectDelay * 1.5, MAX_DELAY);
                connect();
            }, reconnectDelay);
        };

        ws.onerror = () => ws.close();
    }

    function updateBadge(count) {
        const badge = document.querySelector('[x-text="notificationCount"]');
        if (badge && window.Alpine) {
            const el = badge.closest('[x-data]');
            if (el && el._x_dataStack) {
                el._x_dataStack[0].notificationCount = count;
            }
        }
    }

    function incrementBadge() {
        const badge = document.querySelector('[x-text="notificationCount"]');
        if (badge && window.Alpine) {
            const el = badge.closest('[x-data]');
            if (el && el._x_dataStack) {
                el._x_dataStack[0].notificationCount++;
            }
        }
    }

    const toastIcons = {
        incident_created: { emoji: '🚨', bg: 'bg-red-100', text: 'text-red-600' },
        dispatch_created: { emoji: '📡', bg: 'bg-orange-100', text: 'text-orange-600' },
        dispatch_assigned: { emoji: '🚑', bg: 'bg-orange-100', text: 'text-orange-600' },
        system_alert:     { emoji: '⚠️', bg: 'bg-yellow-100', text: 'text-yellow-600' },
    };

    function showToast(notification) {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const ic = toastIcons[notification.notification_type] || { emoji: 'ℹ️', bg: 'bg-blue-100', text: 'text-blue-600' };
        const toast = document.createElement('div');
        toast.className = 'pointer-events-auto flex items-start gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-lg transition-all duration-300';
        toast.innerHTML = `
            <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full ${ic.bg} ${ic.text} text-lg">${ic.emoji}</div>
            <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-slate-800">${notification.title || ''}</p>
                <p class="text-xs text-slate-500 mt-0.5 line-clamp-2">${notification.message || ''}</p>
            </div>
            <button onclick="this.closest('div.pointer-events-auto').remove()" class="text-slate-300 hover:text-slate-500 text-xs leading-none mt-0.5">✕</button>`;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 6000);
    }

    connect();
})();

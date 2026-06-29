/**
 * UI Components Module
 * Handles UI interactions, notifications, and visual feedback
 */

class UIManager {
    constructor() {
        this.notifications = [];
    }

    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-[2000] px-4 py-3 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
        
        const colors = {
            info: 'bg-blue-500 text-white',
            success: 'bg-green-500 text-white',
            warning: 'bg-yellow-500 text-white',
            error: 'bg-red-500 text-white'
        };
        
        notification.classList.add(...colors[type].split(' '));
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.classList.remove('translate-x-full');
        });
        
        // Remove after duration
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, duration);
    }

    showLoading(target) {
        const loading = document.createElement('div');
        loading.className = 'loading-overlay';
        loading.innerHTML = `
            <div class="flex items-center justify-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        `;
        loading.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;
        
        if (target) {
            target.style.position = 'relative';
            target.appendChild(loading);
        }
        
        return loading;
    }

    hideLoading(loadingElement) {
        if (loadingElement && loadingElement.parentNode) {
            loadingElement.parentNode.removeChild(loadingElement);
        }
    }

    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.toggle('hidden');
        }
    }

    setActiveTab(tabId) {
        // Remove active class from all tabs
        document.querySelectorAll('[data-tab]').forEach(tab => {
            tab.classList.remove('active', 'bg-blue-600', 'text-white');
            tab.classList.add('bg-gray-200', 'text-gray-700');
        });
        
        // Add active class to selected tab
        const activeTab = document.querySelector(`[data-tab="${tabId}"]`);
        if (activeTab) {
            activeTab.classList.remove('bg-gray-200', 'text-gray-700');
            activeTab.classList.add('active', 'bg-blue-600', 'text-white');
        }
        
        // Hide all tab content
        document.querySelectorAll('[data-tab-content]').forEach(content => {
            content.classList.add('hidden');
        });
        
        // Show selected tab content
        const activeContent = document.querySelector(`[data-tab-content="${tabId}"]`);
        if (activeContent) {
            activeContent.classList.remove('hidden');
        }
    }

    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('en-NG', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    formatRelativeTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    }

    getStatusBadge(status) {
        const colors = {
            pending: 'bg-yellow-100 text-yellow-800',
            dispatched: 'bg-blue-100 text-blue-800',
            in_progress: 'bg-purple-100 text-purple-800',
            resolved: 'bg-green-100 text-green-800',
            cancelled: 'bg-red-100 text-red-800'
        };
        
        return `<span class="px-2 py-1 text-xs font-medium rounded ${colors[status] || 'bg-gray-100 text-gray-800'}">${status.replace('_', ' ')}</span>`;
    }

    getIncidentTypeBadge(type) {
        const colors = {
            crime: 'bg-red-100 text-red-800',
            violence: 'bg-orange-100 text-orange-800',
            fire: 'bg-red-100 text-red-800',
            flood: 'bg-blue-100 text-blue-800',
            accident: 'bg-yellow-100 text-yellow-800'
        };
        
        return `<span class="px-2 py-1 text-xs font-medium rounded ${colors[type] || 'bg-gray-100 text-gray-800'}">${type}</span>`;
    }
}

// Initialize UI manager
const uiManager = new UIManager();

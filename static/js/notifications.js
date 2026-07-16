/**
 * WebSocket Notification Client
 * Handles real-time notifications via WebSocket connection
 */

class NotificationClient {
    constructor(options = {}) {
        this.wsUrl = options.wsUrl || `ws://${window.location.host}/ws/notifications/`;
        this.socket = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.handlers = [];
        this.unreadCount = 0;
    }
    
    /**
     * Connect to WebSocket server
     */
    connect() {
        try {
            this.socket = new WebSocket(this.wsUrl);
            
            this.socket.onopen = () => {
                console.log('WebSocket connected');
                this.connected = true;
                this.reconnectAttempts = 0;
                this.emit('connected');
            };
            
            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (e) {
                    console.error('Failed to parse WebSocket message:', e);
                }
            };
            
            this.socket.onclose = (event) => {
                console.log('WebSocket disconnected:', event.code, event.reason);
                this.connected = false;
                this.emit('disconnected');
                
                // Attempt to reconnect
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.reconnectAttempts++;
                    console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
                    setTimeout(() => this.connect(), this.reconnectDelay);
                }
            };
            
            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.emit('error', error);
            };
            
        } catch (e) {
            console.error('Failed to create WebSocket connection:', e);
        }
    }
    
    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
            this.connected = false;
        }
    }
    
    /**
     * Handle incoming WebSocket message
     * @param {Object} data - Message data
     */
    handleMessage(data) {
        switch (data.type) {
            case 'notification':
                this.unreadCount++;
                this.emit('notification', data.notification);
                this.emit('unreadCount', this.unreadCount);
                
                // Play sound alert
                if (typeof soundAlerts !== 'undefined') {
                    soundAlerts.playForNotification(data.notification);
                }
                break;
                
            case 'notification_update':
                this.emit('notificationUpdate', data.notification);
                break;
                
            case 'unread_count':
                this.unreadCount = data.count;
                this.emit('unreadCount', this.unreadCount);
                break;
                
            default:
                console.log('Unknown message type:', data.type);
        }
    }
    
    /**
     * Send message to WebSocket server
     * @param {Object} data - Message data
     */
    send(data) {
        if (this.connected && this.socket) {
            this.socket.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket not connected, cannot send message');
        }
    }
    
    /**
     * Mark notification as read
     * @param {number} notificationId
     */
    markAsRead(notificationId) {
        this.send({
            type: 'mark_read',
            notification_id: notificationId
        });
    }
    
    /**
     * Mark all notifications as read
     */
    markAllAsRead() {
        this.send({
            type: 'mark_all_read'
        });
        this.unreadCount = 0;
        this.emit('unreadCount', 0);
    }
    
    /**
     * Request unread count
     */
    requestUnreadCount() {
        this.send({
            type: 'get_unread_count'
        });
    }
    
    /**
     * Register event handler
     * @param {string} event - Event name
     * @param {Function} handler - Handler function
     */
    on(event, handler) {
        this.handlers.push({ event, handler });
    }
    
    /**
     * Remove event handler
     * @param {string} event - Event name
     * @param {Function} handler - Handler function
     */
    off(event, handler) {
        this.handlers = this.handlers.filter(h => 
            !(h.event === event && h.handler === handler)
        );
    }
    
    /**
     * Emit event to all handlers
     * @param {string} event - Event name
     * @param {*} data - Event data
     */
    emit(event, data) {
        this.handlers
            .filter(h => h.event === event)
            .forEach(h => h.handler(data));
    }
    
    /**
     * Check if connected
     * @returns {boolean}
     */
    isConnected() {
        return this.connected;
    }
}

// Global instance
let notificationClient = null;

function initNotifications() {
    if (!notificationClient) {
        notificationClient = new NotificationClient();
        notificationClient.connect();
    }
    return notificationClient;
}

// Auto-initialize disabled — websocket.js handles the connection for dashboard pages.
// Call initNotifications() manually only on non-dashboard pages if needed.

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NotificationClient, initNotifications };
}
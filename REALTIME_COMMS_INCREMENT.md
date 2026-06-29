# Realtime & Comms Increment

> **Note on naming (important):** This work was previously (incorrectly) labelled
> "Phase 9". In the locked roadmap, **Phase 9 = Traffic Intelligence**. The features
> below are a *cross-cutting Realtime & Comms increment* that primarily delivers
> **Phase 8 (Real-Time Alerts)** capabilities (notifications, operative chat, sound
> alerts) plus a **CCTV camera *registry*** that lays the foundation for
> **Phase 12 (CCTV Streaming & Analytics)**. Full RTSP ingest, WebRTC streaming,
> recording, and YOLO-based analytics remain **Phase 12** — see
> `project architecture.md` → "Video / Image / Alert Processing Pipeline".
>
> After this increment, development returns to **Phase 9 = Traffic Intelligence**.

## Scope of this increment
- Sound alerts (chat / critical / severity)
- Real-time notifications over WebSocket (Phase 8)
- Operative chat (REST today; WebSocket consumer is a follow-up — see "Next Steps")
- CCTV camera **registry** model (identification, location, station association) —
  this is metadata/management only; it does **not** stream or analyse video yet.

## Features Implemented

### 1. Sound Alert System

**Three Alert Types:**
- **Chat Alert** - For real-time chat messages and operative communication
- **Critical Alert** - For high-priority incidents and system alerts
- **Severity Alert** - Based on incident severity level (low, medium, high)

**Files:**
- `static/js/sound-alerts.js` - Sound alert management
- `static/audio/chat_alert.mp3` - Chat notification sound (placeholder)
- `static/audio/critical_alert.mp3` - Critical alert sound (placeholder)
- `static/audio/severity_alert.mp3` - Severity alert sound (placeholder)

**Usage:**
```javascript
// Play chat notification
soundAlerts.playChat();

// Play critical alert
soundAlerts.playCritical();

// Play severity alert with level
soundAlerts.playSeverity('high');

// Auto-play based on notification type
soundAlerts.playForNotification(notification);

// Control settings
soundAlerts.setEnabled(true);
soundAlerts.setVolume(0.7);
soundAlerts.stopAll();
```

**Volume Levels by Severity:**
- Low: 0.3
- Medium: 0.5
- High: 0.8

### 2. Real-Time Chat System

**Models:**
- `ChatRoom` - Chat rooms for operative communication
  - Room types: general, incident, dispatch, station
  - Can be linked to incidents, dispatches, or stations
- `ChatMessage` - Individual chat messages
  - Tracks sender, content, read status
  - Timestamped

**API Endpoints:**
- `GET /api/chat/rooms/` - List all chat rooms
- `POST /api/chat/rooms/` - Create chat room
- `GET /api/chat/rooms/<id>/` - Get room details
- `PUT /api/chat/rooms/<id>/` - Update room
- `DELETE /api/chat/rooms/<id>/` - Delete room
- `GET /api/chat/rooms/<id>/messages/` - Get room messages
- `POST /api/chat/rooms/<id>/mark_read/` - Mark messages as read
- `GET /api/chat/messages/` - List all messages
- `POST /api/chat/messages/` - Send message
- `GET /api/chat/messages/my_unread/` - Get unread messages

**Chat Room Types:**
- **General** - General operative communication
- **Incident** - Incident-specific coordination
- **Dispatch** - Dispatch team communication
- **Station** - Station-specific chat

### 3. CCTV Camera Integration

**Camera Model Features:**
- **Identification:**
  - `camera_id` - Unique camera identifier
  - `mac_address` - MAC address (e.g., 00:1A:2B:3C:4D:5E)
  - `serial_number` - Hardware serial number

- **Camera Types:**
  - Fixed
  - PTZ (Pan-Tilt-Zoom)
  - Dome
  - Bullet
  - Thermal

- **Location:**
  - GPS coordinates (PostGIS Point)
  - Address, city, state
  - Coverage radius (meters)
  - Viewing angle (degrees)
  - Direction (degrees, 0 = North)

- **Connection:**
  - IP address and port
  - RTSP stream URL
  - HLS stream URL
  - Authentication credentials

- **Station Association:**
  - Police station
  - Amotekun station

- **Status Tracking:**
  - Online/Offline/Maintenance/Error
  - Last online/offline timestamps

**Additional Models:**
- `CameraRecording` - Recording sessions with incident linkage
- `CameraAlert` - Camera-generated alerts (motion, intrusion, etc.)
  - Alert types: motion, intrusion, object left, face detected, license plate
  - Severity levels: low, medium, high, critical
  - Acknowledgment workflow

### 4. WebSocket Notification Client

**Features:**
- Automatic reconnection with exponential backoff
- Event-based architecture
- Unread count tracking
- Message handling for notifications and updates

**Usage:**
```javascript
// Initialize
const client = initNotifications();

// Event handlers
client.on('notification', (notification) => {
    console.log('New notification:', notification);
});

client.on('unreadCount', (count) => {
    console.log('Unread count:', count);
});

client.on('connected', () => {
    console.log('WebSocket connected');
});

// Actions
client.markAsRead(notificationId);
client.markAllAsRead();
client.requestUnreadCount();
```

## Setup Instructions

### 1. Run migrations
```bash
python manage.py makemigrations chat surveillance
python manage.py migrate
```

> The legacy Windows-only `setup_phase9.bat` is deprecated; use the cross-platform
> commands above (or `make migrate` once a Makefile is added).

### 2. Add Audio Files
Replace placeholder audio files in `static/audio/`:
- `chat_alert.mp3` - Chat notification sound
- `critical_alert.mp3` - Critical alert sound
- `severity_alert.mp3` - Severity alert sound

### 3. Test Chat System
```bash
# Create a chat room
curl -X POST http://localhost:8000/api/chat/rooms/ \
  -H "Authorization: Bearer <token>" \
  -d '{"name": "General Operations", "room_type": "general"}'

# Send a message
curl -X POST http://localhost:8000/api/chat/messages/ \
  -H "Authorization: Bearer <token>" \
  -d '{"room": 1, "content": "Test message"}'
```

### 4. Add Cameras via Admin
1. Go to `/admin/`
2. Navigate to Surveillance → Cameras
3. Add camera with:
   - Camera ID (unique identifier)
   - MAC address (optional)
   - Name and description
   - Location (GPS coordinates)
   - Stream URLs (RTSP/HLS)
   - Station association

## Integration with Dashboards

### Add to Base Dashboard Template
```html
<!-- In templates/dashboard/base_dashboard.html -->
<script src="{% static 'js/sound-alerts.js' %}"></script>
<script src="{% static 'js/notifications.js' %}"></script>
```

### Notification UI Component
```html
<div id="notification-panel" class="hidden">
    <div class="notification-header">
        <h3>Notifications</h3>
        <button onclick="notificationClient.markAllAsRead()">Mark All Read</button>
    </div>
    <div id="notification-list"></div>
</div>
```

### Chat UI Component
```html
<div id="chat-panel">
    <div class="chat-rooms">
        <!-- Room list -->
    </div>
    <div class="chat-messages">
        <!-- Messages -->
    </div>
    <div class="chat-input">
        <input type="text" id="message-input" placeholder="Type message...">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>
```

## Camera Feed Integration

### Display Camera Feed
```html
<video id="camera-feed" controls>
    <source src="{{ camera.hls_url }}" type="application/x-mpegURL">
</video>
```

### Camera Map Integration
```javascript
// Add camera markers to map
cameras.forEach(camera => {
    L.marker([camera.location.y, camera.location.x])
        .addTo(map)
        .bindPopup(`<b>${camera.name}</b><br>Status: ${camera.status}`);
});
```

## API Endpoints Summary

### Chat Endpoints
- `GET /api/chat/rooms/` - List rooms
- `POST /api/chat/rooms/` - Create room
- `GET /api/chat/rooms/<id>/messages/` - Get messages
- `POST /api/chat/messages/` - Send message
- `GET /api/chat/messages/my_unread/` - Get unread

### Surveillance Endpoints (to be implemented)
- `GET /api/surveillance/cameras/` - List cameras
- `POST /api/surveillance/cameras/` - Add camera
- `GET /api/surveillance/cameras/<id>/` - Get camera
- `PUT /api/surveillance/cameras/<id>/` - Update camera
- `GET /api/surveillance/cameras/<id>/recordings/` - Get recordings
- `GET /api/surveillance/cameras/<id>/alerts/` - Get alerts
- `POST /api/surveillance/cameras/<id>/alerts/<alert_id>/acknowledge/` - Acknowledge alert

## Sound Alert Configuration

### Notification Type Mapping
| Notification Type | Sound |
|-------------------|-------|
| chat_message | chat_alert |
| operator_communication | chat_alert |
| incident_created (critical) | critical_alert |
| incident_created (severity) | severity_alert |
| dispatch_assigned | chat_alert |
| dispatch_status_changed (in_progress) | severity_alert (high) |
| system_alert | critical_alert |

## Next Steps

1. **Frontend Integration**
   - Add notification panel to dashboards
   - Implement chat UI in officer/dispatcher dashboards
   - Add camera feed viewer
   - Integrate camera markers on map

2. **WebSocket Chat**
   - Create WebSocket consumer for real-time chat
   - Add typing indicators
   - Implement message receipts

3. **Camera Features**
   - Create REST API endpoints for cameras
   - Implement camera status monitoring
   - Add alert notification integration
   - Create camera management UI

4. **Testing**
   - Test sound alerts with actual audio files
   - Test chat with multiple users
   - Test camera stream integration
   - Load testing for WebSocket connections

## Troubleshooting

### Sound Alerts Not Playing
- Check browser autoplay policies
- Ensure audio files exist in correct location
- Check console for audio play errors
- Test with user interaction first

### WebSocket Not Connecting
- Verify Redis is running
- Check ASGI configuration
- Verify WebSocket URL is correct
- Check browser console for errors

### Camera Stream Not Loading
- Verify stream URL is accessible
- Check camera authentication
- Test stream URL in VLC player
- Check network connectivity

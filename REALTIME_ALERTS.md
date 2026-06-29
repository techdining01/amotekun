# Real-Time Alerts Documentation

## Overview
Phase 8 implements real-time notifications using Django Channels, WebSockets, and Redis. This enables live updates for dispatchers and officers when incidents are reported and dispatches change status.

## Architecture

### Components
1. **Django Channels** - WebSocket support for real-time communication
2. **Redis** - Channel layer backend for message broadcasting
3. **Notifications App** - Database-backed notification storage
4. **WebSocket Consumer** - Handles real-time connections
5. **Notification Service** - Centralized notification sending logic
6. **Django Signals** - Automatic notifications on model changes

## Setup Instructions

### 1. Install Dependencies
```bash
python -m pip install -e .
```

Or manually:
```bash
pip install channels>=4.2.0 channels-redis>=4.2.0 redis>=5.2.0
```

### 2. Apply Migrations
```bash
python manage.py makemigrations notifications
python manage.py migrate notifications
python manage.py makemigrations dispatch
python manage.py migrate dispatch
```

Or run:
```bash
setup_realtime.bat
```

### 3. Start Redis
Redis must be running for WebSocket notifications to work.

**Windows (with Redis installed):**
```bash
redis-server
``

**Docker:**
```bash
docker run -d -p 6379:6379 redis
```

### 4. Start Server with ASGI Support
For production WebSocket support, use Daphne:
```bash
daphne -b 0.0.0.0 -p 8000 incident.asgi:application
```

For development, runserver works but has WebSocket limitations:
```bash
python manage.py runserver
```

## Notification Types

| Type | Trigger | Recipients |
|------|---------|------------|
| `incident_created` | New incident reported | All dispatchers |
| `incident_updated` | Incident details changed | Reporter, dispatcher |
| `dispatch_created` | New dispatch created | Assigned officer, dispatcher |
| `dispatch_assigned` | Officer assigned to dispatch | Assigned officer |
| `dispatch_status_changed` | Dispatch status changes | Officer, dispatcher |
| `dispatch_cancelled` | Dispatch cancelled | Officer, dispatcher |
| `system_alert` | System-wide alerts | All users or specific roles |

## WebSocket API

### Connection
```javascript
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');
```

### Message Types

#### Client → Server

**Mark notification as read:**
```json
{
    "type": "mark_read",
    "notification_id": 123
}
```

**Mark all notifications as read:**
```json
{
    "type": "mark_all_read"
}
```

**Get unread count:**
```json
{
    "type": "get_unread_count"
}
```

#### Server → Client

**New notification:**
```json
{
    "type": "notification",
    "notification": {
        "id": 123,
        "notification_type": "dispatch_assigned",
        "title": "New Assignment",
        "message": "You have been assigned to dispatch for...",
        "data": {
            "dispatch_id": 456,
            "incident_id": 789
        },
        "is_read": false,
        "created_at": "2026-06-28T01:00:00Z"
    }
}
```

**Unread count:**
```json
{
    "type": "unread_count",
    "count": 5
}
```

## Notification Service API

### Send to Single User
```python
from notifications.services import notification_service

notification_service.send_notification(
    user=user,
    notification_type='dispatch_assigned',
    title='New Assignment',
    message='You have been assigned to dispatch...',
    data={'dispatch_id': 123}
)
```

### Send to Role
```python
notification_service.send_to_role(
    role='OFFICER',
    notification_type='system_alert',
    title='System Alert',
    message='Server maintenance in 1 hour'
)
```

### Send to Nearby Officers
```python
notification_service.send_to_officers_nearby(
    lat=6.5244,
    lon=3.3792,
    radius_km=10,
    notification_type='incident_created',
    title='Nearby Incident',
    message='New incident in your area'
)
```

## Automatic Notifications

### Incident Creation
When an incident is created, dispatchers automatically receive a notification via Django signals.

### Dispatch Status Changes
When dispatch status changes, both the assigned officer and dispatcher receive notifications.

### Officer Assignment
When an officer is assigned to a dispatch, they receive a notification.

## Database Schema

### Notification Model
```python
class Notification:
    recipient = ForeignKey(User)
    notification_type = CharField(choices)
    title = CharField(max_length=200)
    message = TextField()
    data = JSONField(default=dict)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

### Indexes
- Composite index on (recipient, is_read) for fast unread queries
- Index on created_at for chronological ordering

## Configuration

### Settings
```python
INSTALLED_APPS = [
    ...
    'channels',
    'notifications',
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

### ASGI Configuration
```python
# incident/asgi.py
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(incident.routing.websocket_urlpatterns)
    ),
})
```

## Testing

### Test WebSocket Connection
```javascript
// In browser console
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');
socket.onmessage = function(e) {
    console.log('Received:', JSON.parse(e.data));
};
```

### Test Notification Service
```python
from notifications.services import notification_service
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

notification_service.send_notification(
    user=user,
    notification_type='system_alert',
    title='Test',
    message='This is a test notification'
)
```

## Troubleshooting

### WebSocket Connection Fails
- Check Redis is running: `redis-cli ping` should return `PONG`
- Verify ASGI configuration in `asgi.py`
- Check firewall settings for WebSocket port

### Notifications Not Sending
- Check Redis connection in settings
- Verify notification service is imported
- Check Django signals are registered in `apps.py`

### Performance Issues
- Use Redis clustering for high volume
- Implement notification batching for bulk sends
- Add database connection pooling

## Security

### Authentication
- WebSocket connections require authenticated user
- Anonymous connections are closed immediately
- User-specific channels prevent cross-user access

### Authorization
- Role-based notification targeting
- Users can only mark their own notifications as read
- Notification data is scoped to recipient

## Next Steps

1. **Frontend Integration**
   - Add WebSocket client to dashboards
   - Implement notification UI components
   - Add sound alerts for urgent notifications

2. **Mobile Push Notifications**
   - Integrate Firebase Cloud Messaging
   - Add mobile device registration
   - Implement push notification fallback

3. **Notification Preferences**
   - Add user notification settings
   - Allow opt-out for non-critical alerts
   - Implement notification digest mode

4. **Analytics**
   - Track notification delivery rates
   - Monitor response times
   - Analyze notification effectiveness

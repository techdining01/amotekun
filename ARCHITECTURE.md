# Amotekun System Architecture

## Overview

This document describes the complete architecture for the Amotekun security and incident management system, organized into distinct layers with clear separation of concerns.

## Architecture Layers

### 1. Presentation Layer

**Responsibility:** Handles what users see and interact with.

**Design Philosophy:** Mobile-first, component-based architecture with minimal JavaScript footprint.

**Components:**
- **Map Interface** - Leaflet-based interactive map for incident reporting and visualization
- **Dashboard** - Role-based dashboards (Citizen, Officer, Dispatcher, Admin)
- **Incident Forms** - Forms for reporting various incident types
- **Facility Views** - Views for police stations, hospitals, Amotekun stations
- **Reports** - Analytics and reporting interfaces
- **Component Library** - Reusable UI components built with django-cotton

**Technologies:**
- **django-cotton** - Django component system for reusable, modular UI components (similar to shadcn/ui paradigm)
- **Tailwind CSS** - Utility-first CSS framework for styling
- **HTMX** - Server-side rendering with hypermedia-driven interactions (reduces JavaScript complexity)
- **Alpine.js** - Lightweight reactive framework for minimal client-side state management
- **Leaflet.js** - Interactive map library (primary JavaScript dependency)
- **WebSocket** - Real-time updates for live data
- **HTML5/CSS3** - Semantic markup and modern styling

**JavaScript Policy:**
- **Minimal JavaScript approach** - Only Leaflet.js for maps and Alpine.js for lightweight reactivity
- **HTMX for interactions** - Form submissions, modal updates, and dynamic content loading
- **Server-side rendering** - Django templates handle most UI logic
- **Component modularity** - django-cotton components for reusable UI patterns

### UI Component Architecture

**django-cotton Component System:**

The UI is built using django-cotton, a Django component system that provides reusable, modular components similar to the shadcn/ui paradigm. This approach ensures:

- **Reusable Components** - Buttons, cards, modals, forms built as independent components
- **Consistent Design** - Shared styling and behavior across the application
- **Server-Side Composition** - Components are composed in Django templates, not JavaScript
- **Tailwind Integration** - Components use Tailwind CSS classes for styling
- **Minimal JavaScript** - Most interactivity handled by HTMX, not custom JS

**Component Structure:**
```
templates/
├── components/
│   ├── base/
│   │   ├── button.html          # Reusable button component
│   │   ├── card.html            # Card container component
│   │   ├── modal.html           # Modal dialog component
│   │   ├── form.html            # Form wrapper component
│   │   └── input.html           # Input field component
│   ├── incident/
│   │   ├── incident_card.html   # Incident display card
│   │   ├── incident_form.html   # Incident reporting form
│   │   └── incident_list.html   # Incident list component
│   ├── facility/
│   │   ├── facility_marker.html # Map marker component
│   │   └── facility_card.html   # Facility info card
│   └── dashboard/
│       ├── stat_card.html       # Statistics card
│       ├── activity_feed.html   # Recent activity feed
│       └── alert_banner.html    # Alert notification banner
```

**HTMX Integration Patterns:**

HTMX is used for dynamic interactions without complex JavaScript:

- **Form Submissions** - `hx-post`, `hx-put` for AJAX form handling
- **Dynamic Content** - `hx-get` to load partial content
- **Modal Updates** - `hx-swap` to update specific DOM elements
- **Real-time Updates** - `hx-trigger` for WebSocket-driven updates
- **Lazy Loading** - `hx-load` for on-demand content loading

**Mobile-First Design Principles:**

- **Responsive Breakpoints** - Tailwind's mobile-first approach (sm:, md:, lg:, xl:)
- **Touch-Friendly** - Larger tap targets, swipe gestures for maps
- **Progressive Enhancement** - Core functionality works on mobile, enhanced on desktop
- **Performance Optimized** - Minimal assets, lazy loading for maps
- **Offline Capability** - Service workers for caching critical assets (future)

### Mobile Application Architecture

**Mobile App Integration:**

The Amotekun system supports mobile applications through two complementary approaches:

#### 1. Progressive Web App (PWA) - Primary Mobile Interface

**Technology Stack:**
- **Django + HTMX** - Server-side rendered mobile interface
- **Tailwind CSS** - Mobile-first responsive design
- **Service Workers** - Offline capability and caching
- **Web App Manifest** - Installable mobile app experience

**How It Works:**
- Citizens access the system via mobile browser
- PWA installation provides native-like experience
- HTMX handles dynamic content without complex JavaScript
- Leaflet.js provides mobile-optimized map interface
- Works offline for critical features (incident reporting)

**Benefits:**
- Single codebase for web and mobile
- No app store approval process
- Instant updates without deployment
- Lower development and maintenance cost
- Cross-platform compatibility

#### 2. Native Mobile Apps - Phase 10 (Future)

**Technology Stack:**
- **React Native / Flutter** - Cross-platform native development
- **Django REST Framework** - RESTful API backend
- **Token Authentication** - JWT-based mobile authentication
- **Push Notifications** - Firebase Cloud Messaging (FCM)

**How It Works:**
- Native apps consume Django REST APIs
- JWT tokens handle authentication
- Background sync for offline incident reporting
- Push notifications for real-time alerts
- Native device integration (camera, GPS, contacts)

**API Endpoints (Phase 10):**
```
/api/v1/mobile/
├── auth/              # Authentication endpoints
├── incidents/         # Incident CRUD operations
├── facilities/        # Facility search and details
├── dispatch/         # Officer dispatch management
├── notifications/     # Push notification registration
└── media/             # Image/video upload endpoints
```

**Mobile-Specific Features:**
- **Geofencing** - Location-based alerts and reporting
- **Camera Integration** - Direct photo/video capture for incidents
- **Background Location** - Continuous tracking for officers
- **Offline Mode** - Queue incidents when offline, sync when connected
- **Push Notifications** - Real-time alerts for critical incidents

**Data Flow for Mobile Users:**

```
Mobile User (PWA or Native App)
    │
    ▼
Mobile Interface (PWA) OR Native App
    │
    ├─ PWA: HTMX → Django Templates
    └─ Native: REST API → Django DRF
    │
    ▼
Django Business Layer
    │
    ▼
PostGIS Database
    │
    ▼
Real-time Updates (WebSocket)
    │
    ▼
Mobile Client Update
```

**Mobile Officer Workflow:**
1. **Login** - Authenticate via JWT (native) or session (PWA)
2. **Receive Dispatch** - Push notification + WebSocket update
3. **View Incident** - Mobile-optimized incident details
4. **Navigate** - Integration with native maps (Google Maps/Apple Maps)
5. **Update Status** - Real-time status updates via HTMX or REST API
6. **Upload Evidence** - Camera integration for photos/videos
7. **Complete Assignment** - Mark incident resolved with location data

### 2. Business Layer

**Responsibility:** Core business logic and data management.

**Location:** Lives mostly in Django.

**Responsibilities:**
- **Authentication** - User login, registration, session management
- **Authorization** - Role-based access control (RBAC)
- **Incident Lifecycle** - Creation, assignment, resolution workflows
- **Dispatch Workflow** - Officer assignment, status transitions
- **Notifications** - Real-time alerts via WebSocket
- **Reporting** - Audit logs and activity tracking

**Django Apps:**
- `accounts` - User management and authentication
- `core` - Core business logic and utilities
- `ui_components` - django-cotton UI component library
- `incidents` - Incident management (renamed from reports)
- `facilities` - Emergency facilities (renamed from stations)
- `dispatch` - Dispatch management
- `notifications` - Real-time notifications
- `chat` - Real-time operative communication
- `surveillance` - CCTV camera management
- `audit` - Audit logging

### 3. GIS Layer

**Responsibility:** Spatial operations and geospatial queries.

**Location:** Lives mostly in FastAPI (future implementation).

**Responsibilities:**
- **Nearest Facility** - Find nearest police/hospital/Amotekun station
- **Spatial Search** - Search within radius, polygon, buffer
- **GeoJSON** - Generate and consume GeoJSON data
- **Buffer Analysis** - Analyze areas around points
- **Polygon Operations** - Intersection, containment, area calculations
- **Routing** - Calculate optimal routes
- **Traffic** - Traffic data and analysis
- **Heatmaps** - Generate hotspot heatmaps

**Django Apps:**
- `geography` - Geographic data models (states, LGAs, boundaries)
- `maps` - Map-related services and APIs
- `traffic` - Traffic intelligence and analysis

**FastAPI Modules:**
```
routers/
├── gis.py          # General GIS operations
├── routing.py      # Route calculation
├── hotspots.py     # Hotspot analysis
├── traffic.py      # Traffic data
├── ai.py           # AI-powered spatial analysis
└── cctv.py         # CCTV spatial queries

services/
├── geo_service.py      # Core GIS operations
├── hotspot_engine.py   # Hotspot detection
├── route_engine.py     # Route calculation
├── traffic_engine.py   # Traffic analysis
├── ai_engine.py        # AI spatial operations
└── cctv_engine.py      # Camera spatial queries
```

### 4. AI Layer

**Responsibility:** Machine learning and computer vision.

**Location:** Future phase (Phase 11).

**Responsibilities:**
- **Incident Classification** - Auto-classify incident types
- **Crime Prediction** - Predict crime hotspots
- **Traffic Prediction** - Predict traffic patterns
- **Object Detection** - Detect objects in camera feeds
- **Crowd Detection** - Detect crowd formations
- **Vehicle Detection** - Detect and classify vehicles
- **Face Detection** - (Optional) Face recognition

**Technologies:**
- YOLO (You Only Look Once) for object detection
- TensorFlow/PyTorch for ML models
- OpenCV for image processing (if needed)

### 5. Infrastructure Layer

**Components:**
- **Docker** - Container orchestration
- **Nginx** - Reverse proxy and load balancer
- **Redis** - Caching and message broker
- **Celery** - Background task processing
- **PostGIS** - Spatial database extension for PostgreSQL

## Data Flow Examples

### Citizen Reports Incident

```
Citizen
    │
    ▼
Leaflet Map (Presentation)
    │
    ▼
Django API (Business)
    │
    ▼
PostGIS (Database)
    │
    ▼
FastAPI Spatial Engine (GIS) [Future]
    │
    ├── Find nearest Police
    ├── Find nearest Hospital
    ├── Calculate best route
    └── Update hotspot statistics
    │
    ▼
Dispatcher Dashboard (Presentation)
    │
    ▼
Officer Receives Assignment (Business)
```

### CCTV Flow (Phase 12)

```
RTSP Camera
    │
    ▼
MediaMTX (Stream Server)
    │
    ▼
WebRTC Stream (Live Viewing)
    │
    ▼
Browser (Presentation)
    │
    ▼
FastAPI (Processing)
    │
    ▼
YOLO Detection (AI)
    │
    ▼
Alert Engine (Business)
    │
    ▼
Django Dashboard (Presentation)
```

## Major Django Apps

| App | Purpose | Status |
|-----|---------|--------|
| accounts | User management | ✅ Complete |
| core | Core business logic | 📝 Planned |
| ui_components | django-cotton UI components | 🔄 In Progress |
| geography | Geographic data models (states, LGAs, boundaries) | 🔄 In Progress |
| maps | Map services | 📝 Planned |
| incidents | Incident management | ✅ Complete |
| facilities | Emergency facilities | ✅ Complete |
| dispatch | Dispatch management | ✅ Complete |
| notifications | Real-time notifications | ✅ Complete |
| chat | Operative communication | ✅ Complete |
| surveillance | CCTV management | ✅ Complete |
| traffic | Traffic intelligence | 🔄 In Progress |
| analytics | Analytics and reporting | 🔄 In Progress |
| reports | Audit and reports | 📝 Planned |
| audit | Audit logging | 📝 Planned |
| mobile | Mobile APIs (JWT, push, media) | ✅ Complete |

## Locked Roadmap

| Phase | Name | Status |
|-------|------|--------|
| Phase 1 | Foundation | ✅ Complete |
| Phase 2 | GIS Data | ✅ Complete |
| Phase 3 | Incident Reporting | ✅ Complete |
| Phase 4 | Emergency Facilities | ✅ Complete |
| **UI Modernization** | django-cotton, HTMX, Mobile-First | 🔄 In Progress |
| Phase 5 | Spatial Queries | 🔄 In Progress |
| Phase 6 | Hotspot Engine | 🔄 In Progress |
| Phase 7 | Dispatch Management | ✅ Complete |
| Phase 8 | Real-Time Alerts | ✅ Complete |
| **Realtime/Comms Increment** | Chat, Sound, CCTV | ✅ Complete |
| Phase 9 | Traffic Intelligence | 🔄 In Progress |
| Phase 10 | Mobile APIs | ✅ Complete |
| Phase 11 | AI Prediction | 🔄 In Progress |
| Phase 12 | CCTV Streaming & Analytics | 📝 Planned |

> Phase 10 is now complete. The project is moving into Phase 11: AI Prediction, with initial architecture and implementation planning underway.

## Traffic Intelligence Strategy (Locked Proposal)

### Vision

- Build a **Traffic Intelligence Platform**, not a traffic provider.
- Use external providers for raw observations while owning the intelligence layer.
- Enrich traffic with local incidents, CCTV events, dispatch state, and spatial context.
- Store historical snapshots so the platform learns from its own data.

### Architecture Overview

- `traffic` app collects provider feeds through a **Traffic Provider Adapter**.
- Collected data is normalized and stored in **PostgreSQL + PostGIS** as snapshots.
- A second layer enriches each snapshot with:
  - local incident reports
  - CCTV detections and camera alerts
  - nearby emergency facilities and routes
  - dispatch activity and response status
- Predictive and recommendation services run on top of the historical dataset.

### Traffic Provider Adapter

Keep the provider abstraction separate from business logic.

Benefits:
- Switch traffic sources without rewriting core logic.
- Add mock providers for testing.
- Blend multiple providers later.
- Support future government or local feeds.

Example adapters:
- `TomTomTrafficProvider`
- `HereTrafficProvider`
- `MockTrafficProvider`

### Collection Strategy

- Use **Celery Beat** for recurring collection every 15 minutes.
- Provide a **management command** for manual backfill or debugging.
- Persist every snapshot; do not overwrite historical data.

Task flow:
- Celery Beat → collect_traffic task → provider adapter → TrafficSnapshot model → enrichment

### TrafficSnapshot Model

Store each observation as a record rather than replacing it.

Example fields:
- `road_name`
- `timestamp`
- `average_speed`
- `travel_time`
- `congestion_level`
- `provider`
- `geometry`
- `incident_count`
- `camera_count`
- `weather_condition` (future)

### Why This Approach

- External providers give current state.
- Your system owns the history.
- The result is proprietary intelligence built from:
  - traffic flow
  - incidents
  - CCTV analytics
  - dispatch activity

### Phase 9 Deliverables

- traffic ingestion service
- provider adapter pattern
- historical traffic snapshot storage
- enriched traffic dataset using local incident and CCTV metadata
- dashboard/mobile API endpoints for congestion and routing insights
- proof of concept route recommendation and alerting

### Phase 9 Status

- `traffic` app exists and is wired into API routes.
- traffic intelligence remains **in progress** while the platform design is locked.
- Mobile APIs are **complete** and available for mobile integration.
- AI Prediction is now the next active phase.

## Phase Status Summary

**Finished phases:**
- Phase 1: Foundation
- Phase 2: GIS Data
- Phase 3: Incident Reporting
- Phase 4: Emergency Facilities
- Phase 7: Dispatch Management
- Phase 8: Real-Time Alerts
- Phase 10: Mobile APIs

**In progress:**
- UI Modernization: django-cotton, HTMX, Mobile-First
- Phase 5: Spatial Queries
- Phase 6: Hotspot Engine
- Phase 9: Traffic Intelligence
- Phase 11: AI Prediction

**Planned:**
- Phase 12: CCTV Streaming & Analytics

---

## Phase 11: AI Prediction

**Objective:** Introduce predictive analytics and model-driven insights for incident management, traffic intelligence, and surveillance.

**Focus Areas:**
- Incident classification and hotspot prediction
- Traffic pattern prediction and alerting
- Surveillance object detection pipelines
- AI-ready architecture for future YOLO/PyTorch integration

**Initial implementation plan:**
1. Catalog existing data sources in `reports`, `traffic`, `analytics`, and `surveillance`.
2. Define backend entry points for prediction services and model inference hooks.
3. Add prototype prediction API endpoints in `analytics` or `surveillance`.
4. Build asynchronous processing and task support for model workloads.
5. Document future camera feed and object detection pipelines.

**Deliverables:**
- documented Phase 11 architecture and data flow
- AI prediction service design in the codebase
- endpoint and model integration plan for dashboards and real-time alerts

## UI Modernization Phase

**Objective:** Transform the UI to use django-cotton, HTMX, and mobile-first design principles.

**Implementation Steps:**

### 1. django-cotton Setup
- Install and configure django-cotton
- Create component directory structure
- Set up Tailwind CSS integration
- Configure component template paths

### 2. Base Component Library
- **Button Component** - Multiple variants (primary, secondary, danger, ghost)
- **Card Component** - Container with header, body, footer slots
- **Modal Component** - Accessible dialog with HTMX integration
- **Form Component** - Form wrapper with CSRF and error handling
- **Input Component** - Text, select, textarea with validation styling
- **Alert Component** - Success, error, warning, info variants

### 3. Domain-Specific Components
- **Incident Card** - Display incident details with status indicators
- **Facility Marker** - Map popup with facility information
- **Dispatch Card** - Officer assignment details with actions
- **Statistics Card** - Dashboard metrics with trend indicators
- **Activity Feed** - Real-time activity timeline

### 4. HTMX Integration
- Convert existing AJAX calls to HTMX attributes
- Implement partial page updates
- Set up WebSocket triggers for real-time updates
- Configure error handling and loading states

### 5. Mobile-First Conversion
- Audit existing templates for mobile responsiveness
- Implement responsive breakpoints for all components
- Optimize touch interactions for mobile devices
- Test on various screen sizes and devices

### 6. Leaflet.js Optimization
- Ensure mobile-optimized map controls
- Implement touch-friendly markers and popups
- Optimize map performance for mobile devices
- Add offline tile caching (future)

**Benefits:**
- **Reduced JavaScript** - Minimal custom JS, mostly HTMX and Alpine.js
- **Better Maintainability** - Reusable components with consistent styling
- **Mobile Experience** - Native-like PWA experience
- **Faster Development** - Component-based development workflow
- **Consistent Design** - Shared component library ensures uniformity

## Security Architecture

### Authentication
- Django-allauth for authentication
- Session-based authentication for web
- Token-based authentication for APIs (future)
- Role-based access control (RBAC)

### Data Encryption
- Camera credentials encrypted at rest using `encryption`
- HTTPS/TLS for all communications
- Database encryption at rest (PostgreSQL)

### API Security
- `IsAuthenticatedOrReadOnly` for public read endpoints
- `IsAuthenticated` for write operations
- CSRF protection for web forms
- Rate limiting (future)

## CCTV Recording Strategy

### Segment-Based Recording

Instead of saving one huge 24-hour file, recordings are split into segments:

```
camera_2026-06-28_10-00.mp4
camera_2026-06-28_10-05.mp4
camera_2026-06-28_10-10.mp4
```

### Benefits
- Faster playback and seeking
- Easier deletion based on retention policies
- Simpler uploads to cloud storage
- Better resilience if recording is interrupted

### Production Stack

| Component | Technology |
|-----------|------------|
| Camera Output | RTSP with H.264 |
| Live Streaming | WebRTC (browser viewing) |
| Recording Format | MP4 (H.264) |
| Segment Duration | 5 minutes |
| Retention | Configurable (30/60/90 days) |
| Storage | Local SSD/NAS + cloud archival |
| Adaptive Streaming | 480p/720p for mobile, full resolution for evidence |

## Video, Picture, and Alert Processing Architecture

### 1. Video Ingestion Layer

**Purpose:** Receive and process RTSP streams from cameras.

**Components:**

#### MediaMTX (Stream Server)
- **Role:** RTSP to WebRTC conversion
- **Input:** RTSP streams from cameras
- **Output:** WebRTC streams for browser viewing
- **Benefits:** Low latency, browser-compatible, adaptive bitrate

**Configuration:**
```yaml
# MediaMTX config
paths:
  camera_001:
    source: rtsp://camera_ip:554/stream
    sourceOnDemand: yes
    sourceRedirect: no
```

#### FFmpeg (Recording Engine)
- **Role:** Segment-based recording
- **Input:** RTSP streams
- **Output:** MP4 segments (5-minute chunks)
- **Features:**
  - H.264 encoding
  - Multiple resolutions (1080p for evidence, 720p for mobile)
  - Automatic segment rotation
  - Retention policy enforcement

**Recording Pipeline:**
```
RTSP Camera
    │
    ▼
FFmpeg (Transcode)
    │
    ├── 1080p Segment (Evidence)
    │   └── camera_2026-06-28_10-00_1080p.mp4
    │
    └── 720p Segment (Mobile)
        └── camera_2026-06-28_10-00_720p.mp4
    │
    ▼
Storage (SSD/NAS)
    │
    ▼
Retention Policy (Celery)
    │
    ▼
Cloud Archival (S3/GCS)
```

### 2. Image Capture Layer

**Purpose:** Capture snapshots for alerts and evidence.

**Trigger Events:**
- Motion detection
- Alert generation
- Manual capture
- Scheduled intervals

**Capture Pipeline:**
```
RTSP Stream
    │
    ▼
FFmpeg (Frame Extraction)
    │
    ▼
Image Processing (OpenCV)
    │
    ├── Resize (if needed)
    ├── Timestamp overlay
    └── Metadata embedding
    │
    ▼
Storage (Snapshots)
    │
    ▼
Database (CameraAlert.snapshot_path)
```

**Storage Structure:**
```
/static/cameras/
├── camera_001/
│   ├── snapshots/
│   │   ├── 2026-06-28_10-00-00.jpg
│   │   └── 2026-06-28_10-05-00.jpg
│   └── recordings/
│       ├── 1080p/
│       │   ├── camera_2026-06-28_10-00.mp4
│       │   └── camera_2026-06-28_10-05.mp4
│       └── 720p/
│           ├── camera_2026-06-28_10-00.mp4
│           └── camera_2026-06-28_10-05.mp4
```

### 3. AI Detection Layer (Phase 11)

**Purpose:** Detect objects and events in video streams.

- **YOLOv8** - Object detection (fast, accurate)
- **OpenCV** - Image preprocessing (if needed)
- **TensorRT** - GPU acceleration (optional)

**Detection Pipeline:**
```
RTSP Stream
    │
    ▼
Frame Extraction (FFmpeg)
    │
    ▼
YOLO Detection
    │
    ├── Person Detection
    ├── Vehicle Detection
    ├── Weapon Detection
    ├── Fire Detection
    └── Crowd Detection
    │
    ▼
Confidence Filter (> 0.7)
    │
    ▼
Alert Engine
    │
    ▼
Django Notification
```

**Detection Classes:**
```python
DETECTION_CLASSES = {
    'person': 0,
    'bicycle': 1,
    'car': 2,
    'motorcycle': 3,
    'bus': 5,
    'truck': 7,
    'knife': 39,  # Custom class
    'fire': 41,   # Custom class
}
```

**Processing Flow:**
1. Extract frame every 2 seconds (configurable)
2. Run YOLO inference
3. Filter by confidence threshold (> 0.7)
4. Check for alert conditions
5. Generate alert if conditions met
6. Capture snapshot with bounding boxes
7. Send notification via Django

### 4. Alert Engine

**Purpose:** Generate and manage alerts based on detection results.

**Alert Types:**

#### Motion Detection
- **Trigger:** Significant motion in frame
- **Severity:** Low/Medium
- **Action:** Log alert, optional notification

#### Intrusion Detection
- **Trigger:** Person in restricted area
- **Severity:** High
- **Action:** Immediate alert to dispatchers

#### Object Left Behind
- **Trigger:** Object stationary > 5 minutes
- **Severity:** Medium
- **Action:** Alert to nearby officers

#### Face Detection
- **Trigger:** Face detected (optional)
- **Severity:** Medium
- **Action:** Log for investigation

#### License Plate Detection
- **Trigger:** Vehicle detected (future)
- **Severity:** Low
- **Action:** Log plate number

#### Camera Offline
- **Trigger:** No stream for > 5 minutes
- **Severity:** High
- **Action:** Alert to technical team

#### Camera Error
- **Trigger:** Stream corruption/error
- **Severity:** Critical
- **Action:** Immediate alert

**Alert Processing Pipeline:**
```
Detection Event
    │
    ▼
Rule Engine (Evaluate Conditions)
    │
    ├── Severity Assessment
    ├── Location Check (is it in critical area?)
    └── Time Check (is it during active hours?)
    │
    ▼
Alert Generation
    │
    ├── Capture Snapshot
    ├── Extract Video Clip (30s before/after)
    └── Generate Metadata
    │
    ▼
Database (CameraAlert)
    │
    ▼
Notification Service
    │
    ├── Send to Dispatchers (if high/critical)
    ├── Send to Nearby Officers (if intrusion)
    └── Log in Audit Trail
    │
    ▼
Dashboard Alert
```

**Alert Rules Configuration:**
```python
ALERT_RULES = {
    'intrusion': {
        'enabled': True,
        'severity': 'high',
        'notify_dispatchers': True,
        'notify_officers': True,
        'radius': 500,  # meters
    },
    'motion': {
        'enabled': True,
        'severity': 'low',
        'notify_dispatchers': False,
        'notify_officers': False,
    },
    'camera_offline': {
        'enabled': True,
        'severity': 'high',
        'notify_dispatchers': True,
        'notify_officers': False,
    },
}
```

### 5. Storage Management

**Retention Policy:**

| Data Type | Duration | Storage |
|-----------|----------|---------|
| Live Segments (1080p) | 7 days | Local SSD |
| Live Segments (720p) | 30 days | Local SSD |
| Alert Clips | 90 days | Local SSD + Cloud |
| Snapshots | 30 days | Local SSD |
| Evidence Clips | 365 days | Cloud (S3/GCS) |

**Cleanup Process (Celery Task):**
```python
@celery.task
def cleanup_old_recordings():
    """Delete recordings older than retention period"""
    cutoff_date = timezone.now() - timedelta(days=RETENTION_DAYS)
    old_recordings = CameraRecording.objects.filter(
        start_time__lt=cutoff_date
    )
    for recording in old_recordings:
        if os.path.exists(recording.file_path):
            os.remove(recording.file_path)
        recording.delete()
```

**Cloud Archival:**
```python
@celery.task
def archive_to_cloud():
    """Move old recordings to cloud storage"""
    cutoff_date = timezone.now() - timedelta(days=7)
    old_recordings = CameraRecording.objects.filter(
        start_time__lt=cutoff_date,
        archived=False
    )
    for recording in old_recordings:
        upload_to_s3(recording.file_path)
        recording.archived = True
        recording.save()
```

### 6. FastAPI Integration

**Purpose:** High-performance video processing and spatial queries.

**FastAPI Modules:**

#### `cctv_engine.py`
```python
from fastapi import FastAPI
from services.cctv_service import CCTVService

app = FastAPI()

@app.post("/cctv/detect")
async def detect_objects(frame: bytes):
    """Run YOLO detection on frame"""
    results = await cctv_service.detect_objects(frame)
    return results

@app.get("/cctv/cameras/nearby")
async def get_nearby_cameras(lat: float, lng: float, radius: int):
    """Get cameras within radius of location"""
    cameras = await cctv_service.get_nearby_cameras(lat, lng, radius)
    return cameras
```

### 7. Real-Time Alert Flow

**Complete Alert Flow:**
```
Camera Event (Motion/Object Detection)
    │
    ▼
MediaMTX (Stream Processing)
    │
    ▼
FFmpeg (Frame Extraction)
    │
    ▼
YOLO Detection (Phase 11)
    │
    ▼
Alert Engine (Rule Evaluation)
    │
    ▼
Django Notification Service
    │
    ├── Database (CameraAlert)
    ├── WebSocket (Real-time to dashboards)
    ├── Sound Alerts (Critical/Severity)
    └── Push Notifications (Mobile)
    │
    ▼
Dispatcher Dashboard
    │
    ├── Visual Alert
    ├── Sound Alert
    └── Map Highlight
    │
    ▼
Officer Assignment (if needed)
```

## Security Architecture

### Camera Credential Security

**Encryption at Rest:**
- Camera passwords encrypted using `django-encrypted-fields`
- RSA key pair for encryption/decryption
- Keys stored in environment variables (never in code)
- Admin interface collapses password field by default

**Stream Security:**
- RTSP authentication required
- WebRTC with DTLS encryption
- TLS for all HTTP/HTTPS communications
- Network-level access control

**Access Control:**
- Role-based access to camera feeds
- Audit logging for camera access
- Session timeout for live viewing
- IP whitelisting for camera networks

## Technology Stack

### Backend
- Django 5.2+ - Web framework
- Django REST Framework - API framework
- Django REST Framework GIS - Spatial API support
- PostGIS - Spatial database
- Redis - Caching and message broker
- Celery - Background tasks
- Channels - WebSocket support
- Daphne - ASGI server

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Tailwind CSS - Styling
- Alpine.js - Reactive components
- Leaflet.js - Maps
- Chart.js - Visualizations (future)

### Infrastructure
- Docker - Containerization
- Nginx - Reverse proxy
- PostgreSQL - Database
- Redis - Caching/message broker

### Future Additions
- FastAPI - High-performance GIS operations
- YOLO - Object detection
- TensorFlow/PyTorch - ML models
- MediaMTX - Video streaming

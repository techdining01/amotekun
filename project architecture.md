🏛️ Smart Community Surveillance & Emergency Response Platform
High-Level Architecture
                         Citizens / Officers / Dispatchers / Admin
                                         │
                                         │
                           Django Templates (Mobile First)
                                         │
                    django-shadcn-ui + HTMX + Alpine.js
                                         │
 ┌───────────────────────────────────────┴────────────────────────────────────────┐
 │                                 Django Core                                   │
 │-------------------------------------------------------------------------------│
 │ Authentication (django-allauth)                                               │
 │ Roles & Permissions                                                           │
 │ Dashboard                                                                     │
 │ Incident Management                                                           │
 │ Dispatch Workflow                                                             │
 │ Facility Management                                                           │
 │ User Management                                                               │
 │ Notifications                                                                 │
 │ Audit Logs                                                                    │
 │ REST APIs                                                                     │
 └───────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                     Internal REST / HTTP / Celery Tasks
                                         │
                ┌────────────────────────┴─────────────────────────┐
                │                                                  │
      ┌─────────▼──────────┐                           ┌──────────▼──────────┐
      │   FastAPI Service   │                           │ PostgreSQL + PostGIS│
      │---------------------│                           │---------------------│
      │ GIS Engine          │                           │ Users               │
      │ Routing Engine      │                           │ Geography           │
      │ Hotspot Engine      │                           │ Incidents           │
      │ AI Services         │                           │ Facilities          │
      │ CCTV Analytics      │                           │ Dispatch            │
      └─────────┬──────────┘                           └─────────────────────┘
                │
                │
     ┌──────────▼──────────┐
     │ External Services    │
     │----------------------│
     │ OpenStreetMap        │
     │ CCTV (RTSP/WebRTC)   │
     │ Push Notifications   │
     │ Weather (Future)     │
     │ Traffic Sources      │
     └──────────────────────┘
Technology Stack (Locked)
Frontend
Django Templates
django-shadcn-ui
django-components
HTMX
Alpine.js
Leaflet

No React, Vue, or Next.js.

Backend
Django
Django REST Framework
django-allauth

Django is the orchestrator of the system.

GIS & Analytics
FastAPI

FastAPI is responsible for:

Spatial analysis
Routing
Hotspot generation
AI services
CCTV analytics
Future ML models
Database
PostgreSQL
PostGIS

Everything location-related is stored here.

Background Processing
Redis
Celery

Used for:

Notifications
CCTV processing jobs
AI tasks
Report generation
Scheduled maintenance
Application Layers
Presentation Layer
        │
Business Layer
        │
GIS Layer
        │
AI Layer
        │
Infrastructure Layer
1. Presentation Layer

Handles what users see.

Map
Dashboard
Incident Forms
Facility Views
Reports
2. Business Layer

Lives mostly in Django.

Responsible for:

Authentication

Authorization

Incident lifecycle

Dispatch workflow

Notifications

Reporting

Audit logs
3. GIS Layer

Lives mostly in FastAPI.

Responsible for:

Nearest facility

Spatial search

GeoJSON

Buffer analysis

Polygon operations

Routing

Traffic

Heatmaps
4. AI Layer

Future phase.

Incident classification

Crime prediction

Traffic prediction

Object detection

Crowd detection

Vehicle detection

Face detection (optional)
5. Infrastructure Layer
Docker

Nginx

Redis

Celery

PostGIS
Major Django Apps (Planned)
accounts
core
geography
maps
incidents
facilities
dispatch
notifications
traffic
cctv
analytics
reports
audit
settings

More may be added as the project grows, but these are the planned core domains.

FastAPI Modules
routers/
    gis.py
    routing.py
    hotspots.py
    traffic.py
    ai.py
    cctv.py

services/
    geo_service.py
    hotspot_engine.py
    route_engine.py
    traffic_engine.py
    ai_engine.py
    cctv_engine.py
Data Flow Example

Citizen reports an accident:

Citizen
   │
   ▼
Leaflet Map
   │
   ▼
Django API
   │
   ▼
PostGIS
   │
   ▼
FastAPI Spatial Engine
   │
   ├── Find nearest Police
   ├── Find nearest Hospital
   ├── Calculate best route
   └── Update hotspot statistics
   │
   ▼
Dispatcher Dashboard
   │
   ▼
Officer Receives Assignment
CCTV Flow (Phase 12)
RTSP Camera
      │
      ▼
MediaMTX
      │
      ▼
WebRTC Stream
      │
      ▼
Browser
      │
      ▼
FastAPI
      │
      ▼
YOLO Detection
      │
      ▼
Alert Engine
      │
      ▼
Django Dashboard

Notice that YOLO is used for object detection. OpenCV is introduced only if we need custom video preprocessing or image manipulation beyond what the detection pipeline provides.

Our Locked Roadmap
Phase 1  Foundation
Phase 2  GIS Data
Phase 3  Incident Reporting
Phase 4  Emergency Facilities
Phase 5  Spatial Queries
Phase 6  Hotspot Engine
Phase 7  Dispatch Management
Phase 8  Real-Time Alerts
Phase 9  Traffic Intelligence
Phase 10 Mobile APIs
Phase 11 AI Prediction
Phase 12 CCTV Streaming & Analytics
Phase 13 Audit & Compliance (audit logs, evidence chain-of-custody, data retention)
Phase 14 Reporting & Analytics (operational dashboards, exports, KPIs)
Phase 15 Hardening & Scale (multi-tenant LGAs, HA, load/perf, DR)

Cross-cutting increments (delivered alongside phases, not a phase of their own)
- Realtime & Comms Increment — operative chat, sound alerts, WebSocket
  notifications, and the CCTV camera *registry*. Primarily satisfies Phase 8
  (Real-Time Alerts) and seeds Phase 12. See `REALTIME_COMMS_INCREMENT.md`.
  NOTE: this increment was previously mislabelled "Phase 9". Phase 9 remains
  Traffic Intelligence.



Recording strategy

Instead of saving one huge file:

24-hour recording

Split recordings into small segments, for example:

camera_2026-06-28_10-00.mp4
camera_2026-06-28_10-05.mp4
camera_2026-06-28_10-10.mp4

Benefits:

Faster playback
Easier deletion based on retention policies
Simpler uploads to cloud storage
Better resilience if recording is interrupted

Many professional VMS solutions use segment lengths between 1 and 10 minutes.

For the architecture we're building

I recommend the following production stack:

Camera output: RTSP with H.264
Live streaming: WebRTC (for browser viewing)
Recording format: MP4 (H.264)
Segment duration: 5 minutes
Retention: Configurable (e.g., 30, 60, or 90 days)
Storage: Local SSD/NAS for recent footage, with optional cloud archival for older recordings
Adaptive streaming: Generate lower-resolution streams (e.g., 480p or 720p) for mobile users while keeping full-resolution recordings for evidence

This combination gives you low-latency live viewing, efficient storage, broad device compatibility, and a solid foundation for future AI features like person detection, vehicle recognition, and event-based clip retrieval without unnecessary transcoding.
---

# Video / Image / Alert Processing Pipeline (Phase 12 design)

This section specifies how live video, snapshots/images, and alerts are processed
end-to-end, where each responsibility lives, and how data flows between Django,
FastAPI, Celery/Redis, and the media tier. It is the detailed design behind the
"CCTV Flow (Phase 12)" diagram above. The Realtime & Comms increment has already
shipped the **camera registry** (the `surveillance.Camera/CameraRecording/
CameraAlert` models); the pipeline below builds on that registry.

## Component responsibilities (who owns what)

| Concern | Owner | Why |
|---|---|---|
| Camera registry, RBAC, alert review, evidence metadata, dashboards | **Django** | Business layer; already has auth, models, admin |
| RTSP ingest, transcoding, recording/segmentation, live stream publishing | **MediaMTX + FFmpeg** | Purpose-built media servers; do not reinvent in Python |
| Detection / analytics (YOLO), snapshot generation, event extraction | **FastAPI (AI/CCTV engine)** | GIS/AI layer; GPU-friendly, isolated from web workers |
| Async fan-out (recording housekeeping, thumbnailing, retention, notifications) | **Celery + Redis** | Background processing layer |
| Frame/clip/snapshot storage | **Object storage (S3-compatible) + local SSD cache** | Durable evidence + low-latency recent footage |
| Live viewing in browser | **WebRTC (via MediaMTX)** | Sub-second latency for operators |

## End-to-end data flow

```
                         ┌──────────────────────────────────────┐
RTSP Camera (H.264) ───► │ MediaMTX (ingest + restream)          │
                         │  • publishes WebRTC (live view)       │
                         │  • publishes HLS (mobile/fallback)    │
                         │  • runs FFmpeg record → 5-min MP4      │
                         └───────┬───────────────┬───────────────┘
                                 │               │
                  segment frames │               │ recorded MP4 segments
                  (RTSP/HTTP)    ▼               ▼
                         ┌───────────────┐   ┌─────────────────────────┐
                         │ FastAPI CCTV  │   │ Object storage (S3)      │
                         │ analytics     │   │  + local SSD cache       │
                         │  • YOLO infer │   └───────────┬─────────────┘
                         │  • snapshot   │               │ presigned URL
                         │  • debounce   │               ▼
                         └──────┬────────┘   ┌─────────────────────────┐
              detection event   │            │ Django (evidence + UI)  │
              (HTTP POST,       └──────────► │  • CameraRecording row   │
               HMAC-signed)                  │  • CameraAlert row       │
                                             │  • dispatch/notify       │
                                             └───────────┬─────────────┘
                                                         │ Channels group_send
                                                         ▼
                                             Operator Dashboard (WebSocket)
                                              + sound alert + map marker
```

## 1. Live video (operator viewing)
- Cameras push **RTSP/H.264** to **MediaMTX** (one ingest per camera).
- MediaMTX re-publishes each stream as **WebRTC** (primary, sub-second latency for
  the control room) and **HLS** (fallback / mobile / high-latency networks).
- The browser never talks to the camera directly. It requests a short-lived,
  **per-session signed stream token** from Django, which authorizes a MediaMTX
  WebRTC/HLS path. This keeps RTSP credentials server-side and lets us revoke
  access per user/role.
- Adaptive streaming: MediaMTX/FFmpeg generate a 480p/720p variant for mobile while
  the full-resolution stream is reserved for recording/evidence.

## 2. Recording (evidence)
- FFmpeg (managed by MediaMTX) records each camera into **5-minute MP4 segments**
  named `camera_<id>_<YYYY-MM-DD_HH-MM>.mp4` (matches the recording strategy above).
- On each completed segment, a hook notifies Django (signed webhook) which creates a
  `CameraRecording` row with: camera, start/end time, duration, storage key, size,
  and a SHA-256 **content hash** (chain-of-custody / tamper evidence).
- Storage tiering: recent N days on **local SSD** for instant scrubbing; older
  segments lifecycle to **S3-compatible object storage**; retention is
  **configurable (30/60/90 days)** and enforced by a nightly **Celery beat** task.
- Segments are linked to incidents via `CameraRecording.incident` so dispatchers can
  pull "all footage around incident X within ±10 min and Y meters" (spatial+temporal
  query using the camera's PostGIS point).

## 3. Image / snapshot processing & detection
- FastAPI's **CCTV engine** pulls frames from MediaMTX (not from web workers) at a
  configurable sampling rate (e.g. 2–5 fps for detection, not every frame).
- **YOLO** runs object/vehicle/person detection; **OpenCV** is introduced only for
  custom pre/post-processing (cropping, license-plate ROI, image enhancement).
- On a positive detection the engine:
  1. captures a **snapshot** (JPEG) and a short **clip** (pre/post-roll),
  2. writes both to object storage,
  3. **debounces** (e.g. suppress duplicate "motion" on the same camera within a
     cooldown window) so we don't flood operators,
  4. POSTs a **detection event** to Django (HMAC-signed, idempotency key).

## 4. Alert lifecycle
- Django receives the detection event and creates a `CameraAlert`
  (type, severity, snapshot/clip keys, `metadata` JSON, optional `incident`).
- Severity maps to operator UX (reusing the Realtime & Comms increment):
  - `critical`/`high` → push to dashboard via **Channels `group_send`** +
    `critical_alert`/`severity_alert` sound + map marker; may auto-create/escalate
    a dispatch.
  - `low`/`medium` → recorded, surfaced in the alert queue, no interruptive sound.
- Operators **acknowledge** alerts (`CameraAlert.acknowledge(user)`); ack state,
  who, and when are stored for audit (Phase 13).
- All snapshots/clips are served to the UI via **short-lived presigned URLs**, never
  by exposing storage or camera credentials.

## 5. Security & privacy guardrails
- RTSP/camera credentials are **encrypted at rest** (see `EncryptedCharField` on the
  `Camera` model) and are **never** returned by the API.
- Browser access to streams is brokered by signed, expiring tokens; no direct RTSP.
- Detection→Django and recording→Django callbacks are **authenticated** (HMAC shared
  secret) and **idempotent**.
- Face detection is **optional/opt-in per deployment** and gated behind policy +
  audit logging, given its legal/privacy sensitivity.
- Evidence integrity: content hashing + immutable audit trail (Phase 13).

## 6. Scaling & failure modes
- One MediaMTX path per camera; scale MediaMTX horizontally and shard cameras across
  nodes. FastAPI detection workers scale independently (GPU pool).
- If FastAPI/detection is down, **recording and live view continue** (decoupled);
  alerts simply pause and backfill is optional.
- If object storage is unreachable, segments buffer on local SSD and a Celery task
  retries upload (resilience to interrupted recording).
- Redis/Channels outage degrades only the *real-time push*; alerts are still
  persisted and visible on dashboard refresh.

## Recommended Phase 12 build order
1. MediaMTX ingest + WebRTC live view (no analytics) behind signed tokens.
2. FFmpeg 5-min segment recording → `CameraRecording` + storage tiering + retention.
3. FastAPI YOLO detection → snapshots/clips → signed `CameraAlert` webhook.
4. Alert fan-out wiring into the existing notification/sound/dispatch pipeline.
5. Evidence hardening (hashing, presigned URLs, audit) — overlaps Phase 13.

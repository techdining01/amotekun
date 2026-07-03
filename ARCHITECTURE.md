# Amotekun System Architecture

## Overview

This document describes the current architecture of the Amotekun security and incident management system as implemented in this workspace.
It focuses on actual code, active app boundaries, current phase status, and the real UI / API connections.

## Current Architecture Layers

### 1. Presentation Layer

**Responsibility:** User-facing interfaces, dashboards, public pages, and camera preview experiences.

**Current technologies:**
- Django templates + `django-cotton` for reusable page structure.
- Tailwind CSS for styling and responsive layout.
- Alpine.js for lightweight client-side state within dashboard components.
- HTMX for progressive enhancement and server-driven interactions.
- Leaflet.js is available in the codebase for map-based incident and facility views.
- Django Channels / Daphne for WebSocket-backed notification and real-time updates.

**Active presentation components:**
- `dashboard/` - role-based dashboard entry points and UI layout.
- `templates/dashboard/dispatcher_dashboard.html` - dispatcher dashboard with quick actions.
- `templates/dashboard/camera_viewer.html` - floating camera batch/preview overlay.
- `templates/dashboard/camera_grid.html` - dedicated 24-camera grid and 8-camera batch page.
- `surveillance` DRF views and serializers powering camera metadata and PTZ control.
- `analytics` APIs for hotspot and prediction workflows.

### 2. Business Layer

**Responsibility:** Core application logic, request handling, state transitions, and cross-app behavior.

**Implemented apps and responsibilities:**
- `accounts` - user management, authentication, custom user model.
- `dashboard` - role routing and page rendering for Citizen, Officer, Dispatcher, Admin.
- `reports` - incident modeling and reporting workflows.
- `stations` - facility models for police and Amotekun stations.
- `geography` - geographic data models and spatial utilities.
- `dispatch` - officer assignment and dispatch management.
- `notifications` - notifications and alert infrastructure.
- `chat` - operative communications.
- `surveillance` - CCTV camera management, PTZ, registration, streaming URLs.
- `traffic` - traffic intelligence ingestion, snapshot storage, provider adapters.
- `analytics` - hotspot storage and Phase 11 prediction API scaffolding.
- `mobile` - mobile authentication and API support.
- `api` and `intelligence` - present as app shells for future API and intelligence-specific expansion.

**Key behavior in this codebase:**
- Role-based dashboard selection is handled in `dashboard/views.py`.
- `traffic` collects provider snapshots and stores historical `TrafficSnapshot` records.
- `surveillance` registers the current physical device by `CAMERA_DEVICE_ID` and exposes PTZ controls.
- `analytics` provides a prototype prediction endpoint and load/save model helpers.

### 3. Data & Spatial Layer

**Responsibility:** Persistent storage, GIS-aware models, snapshot history, and queryable spatial data.

**Implemented models:**
- `reports.Incident` - incident records with geometry and status.
- `stations.PoliceStation`, `stations.AmotekunStation` - facility locations.
- `geography` models - state, LGA, and other spatial boundaries.
- `traffic.Road` - monitored road segments with geometry and monitoring metadata.
- `traffic.TrafficSnapshot` - historical traffic provider snapshot storage.
- `surveillance.Camera` - camera metadata, stream URL, PTZ control URL.
- `analytics.Hotspot` / `HotspotAnalysis` - hotspot storage and analysis results.

**Important notes:**
- PostGIS is used for geospatial fields (`PointField`, `LineStringField`, `PolygonField`).
- Traffic and CCTV enrichment is stored together through snapshot and camera metadata.
- The current app does not yet contain a separate `core` or `audit` app; those behaviors are implemented inside namespaced apps such as `reports`, `stations`, `geography`, and `analytics`.

### 4. Infrastructure Layer

**Responsibility:** Background processing, caching, async tasks, and external service integration.

**Active infrastructure components:**
- Redis / Channels layer for WebSocket message passing.
- Celery tasks and beat schedules used for traffic collection.
- Django REST Framework for API endpoints.
- `django-allauth` for authentication.
- Postgres + PostGIS for database and geospatial storage.

**Current external integrations:**
- TomTom traffic API in `traffic/providers.py`.
- HERE traffic API in `traffic/providers.py`.
- Optional camera PTZ endpoints using `requests` from `surveillance.models.Camera.send_ptz_command()`.

## Actual App Map

| App | Current role in code | Status |
|---|---|---|
| `accounts` | User auth and roles | ✅ Implemented |
| `dashboard` | Role dashboard pages, camera grid UI | ✅ Implemented |
| `reports` | Incident reporting and spatial incident data | ✅ Implemented |
| `stations` | Facility models for police/Amotekun stations | ✅ Implemented |
| `geography` | Geographic data and boundaries | ✅ Implemented |
| `dispatch` | Dispatch workflow and assignments | ✅ Implemented |
| `notifications` | Real-time alerts and notification plumbing | ✅ Implemented |
| `chat` | Operative chat and messaging | ✅ Implemented |
| `surveillance` | CCTV camera metadata, registration, PTZ | ✅ Implemented |
| `traffic` | Traffic provider ingestion and snapshots | 🔄 In progress |
| `analytics` | Hotspots and prediction scaffold | ✅ Implemented |
| `mobile` | Mobile API support and auth | ✅ Implemented |
| `api` | App shell for API expansion | 📝 Present but not central |
| `intelligence` | App shell for intelligence expansion | 📝 Present but not central |

## Phase Status

### Completed
- Phase 1: Foundation and dashboard architecture
- Phase 2: GIS / geographic data models
- Phase 3: Incident reporting and response workflows
- Phase 4: Facility and station management
- Phase 7: Dispatch assignment workflows
- Phase 8: Real-time alerts and chat
- Phase 10: Mobile API authentication and endpoints
- Phase 11: AI prediction scaffold and prototype API

### In progress
- Phase 5: Spatial query enrichment and GIS feature set
- Phase 6: Hotspot engine and analysis refinement
- Phase 9: Traffic intelligence ingestion, enrichment, snapshot persistence
- UI Modernization: component reuse, HTMX, and mobile-first polish

### Planned
- Phase 12: CCTV streaming, WebRTC / MediaMTX integration, object detection, and analytics pipeline
- Additional audit / `core` app separation for cross-app shared services

## Traffic Intelligence (Phase 9)

**Implemented today:**
- `traffic/providers.py` contains adapters for TomTom, HERE, and a mock provider.
- `traffic/services.py` contains `TrafficCollectionService` that:
  - selects roads marked `is_monitored`
  - fetches provider snapshots
  - enriches snapshots with local incident and camera counts
  - persists `TrafficSnapshot` records
- `traffic/tasks.py` contains a Celery task that:
  - runs scheduled traffic collection
  - logs provider failures
  - falls back from TomTom to HERE if needed

**Current status:**
- Traffic ingestion is wired.
- Historical snapshot storage is implemented.
- The enrichment layer is present with incident and camera counts.
- Flow measurements are now created from provider snapshots and road metadata is updated.
- Dispatcher dashboard now surfaces traffic summary metrics and latest snapshots.
- A recommendation scaffold exists for monitored roads, with full route guidance still planned.

## CCTV / Surveillance Architecture

**Implemented today:**
- `surveillance.models.Camera` stores:
  - `rtsp_url`, `hls_url` stream URLs
  - `control_url` for PTZ commands
  - status metadata and camera location
- `surveillance.views.CameraViewSet` exposes:
  - camera list/detail CRUD
  - `register-current` device registration
  - `ptz` action endpoint
- `templates/dashboard/camera_viewer.html` and `camera_grid.html` implement:
  - an embedded batch camera browser
  - a toggleable 8-camera batch and 24-camera grid page
  - selected camera preview with live stream playback
  - PTZ command buttons for configured cameras

**What is still planned:**
- actual browser-grade WebRTC / adaptive streaming gateway
- camera feed ingest pipeline and object detection
- full CCTV analytics dashboard beyond metadata and preview UI

## Analytics & Prediction (Phase 11)

**Implemented today:**
- `analytics.prediction.PredictionService` provides a model inference scaffold.
- `analytics.model_io` supports loading and saving pickled models.
- `analytics.views.PredictTrafficAPIView` accepts `lat`, `lng`, and optional `snapshot`.
- `analytics.models` stores hotspots and hotspot analysis results.

**Current status:**
- Prediction scaffolding is implemented.
- The ML model is not yet persisted or trained in production.
- Real AI-driven incident or traffic forecasting remains future work.

## Mobile & API Flow

**Current API routes:**
- `/api/surveillance/` → surveillance camera CRUD, register-current, PTZ
- `/api/traffic/` → traffic endpoints and snapshots
- `/api/analytics/` → hotspots and `predict/`
- `/dashboard/` → role-based dashboards and camera grid
- `/accounts/` → auth and user management

**Mobile support:**
- `mobile` app provides JWT / token endpoints and mobile API structure.
- The PWA and mobile-friendly dashboard UI are present in templates.

## UI and Data Flow

### Dashboard to surveillance
1. User opens dispatcher dashboard.
2. `dispatcher_dashboard.html` exposes a `Camera Grid` button.
3. The button navigates to `/dashboard/cameras/`.
4. `camera_grid.html` fetches camera metadata from `/api/surveillance/cameras/`.
5. Users can select a camera, view its `stream_url`, and send PTZ commands.

### Traffic ingestion flow
1. Celery beat invokes `traffic.tasks.collect_traffic_snapshot`.
2. `TrafficCollectionService` fetches snapshots from TomTom or HERE.
3. Each snapshot is enriched with local incident and camera counts.
4. Snapshots are persisted to `traffic.TrafficSnapshot`.

### Prediction flow
1. Client calls `POST /api/analytics/predict/`.
2. `PredictTrafficAPIView` creates `PredictionService`.
3. The service returns a congestion probability.
4. The endpoint is a scaffold for future ML model deployment.

## What changed from the old draft

This version removes placeholder architecture items that were not present in the workspace.
Instead of separate `core`, `maps`, and `audit` apps, the current code implements those responsibilities inside the apps listed above.
It also clarifies that Phase 9 traffic intel is still in progress, and Phase 12 CCTV streaming / analytics is planned but not yet implemented.

## Future work priorities

1. Complete traffic intelligence dashboards and mobile endpoints.
2. Add persistent model training / inference for analytics predictions.
3. Implement full CCTV streaming gateway and browser playback pipeline.
4. Separate shared services into a true `core` or `audit` app if clean modularity is needed.
5. Expand `api` and `intelligence` into fully realized integration layers.

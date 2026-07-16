"""
Map data API — returns GeoJSON for incidents, facilities, traffic incidents, roads.
Used by the operations map JS to populate layers without page reload.
"""
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib.gis.serializers.geojson import Serializer as GeoJSONSerializer


@login_required
def map_incidents(request):
    from reports.models import Incident
    cached = cache.get("map:incidents")
    if cached:
        return JsonResponse(cached, safe=False)
    qs = Incident.objects.exclude(geometry=None).only(
        "id", "title", "priority", "status", "lga", "state", "created_at", "geometry"
    ).order_by("-created_at")[:300]
    features = []
    for inc in qs:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [inc.geometry.x, inc.geometry.y]},
            "properties": {
                "id": inc.id, "title": inc.title,
                "priority": inc.priority or "low", "status": inc.status,
                "lga": str(inc.lga) if inc.lga else "",
                "state": str(inc.state) if inc.state else "",
                "created_at": inc.created_at.isoformat() if inc.created_at else "",
            },
        })
    data = {"type": "FeatureCollection", "features": features}
    cache.set("map:incidents", data, 120)  # 2 min — incidents change frequently
    return JsonResponse(data)


@login_required
def map_facilities(request):
    cached = cache.get("map:facilities")
    if cached:
        return JsonResponse(cached, safe=False)
    from stations.models import PoliceStation, AmotekunStation, Hospital, Facility
    features = []

    # Police stations
    for f in PoliceStation.objects.only("name", "address", "location", "state", "lga"):
        loc = f.location
        if not loc:
            continue
        try:
            lat_str, lng_str = loc.split(",")
            lng, lat = float(lng_str.strip()), float(lat_str.strip())
        except (ValueError, AttributeError):
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "name": f.name, "type": "police",
                "address": f.address or "",
                "state": f.state or "", "lga": f.lga or "",
            },
        })

    # Amotekun stations
    for f in AmotekunStation.objects.only("name", "address", "location", "state", "lga"):
        loc = f.location
        if not loc:
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [loc.x, loc.y]},
            "properties": {
                "name": f.name, "type": "amotekun",
                "address": f.address or "",
                "state": f.state or "", "lga": f.lga or "",
            },
        })

    # Hospitals — full detail for popup
    tertiary_keywords = ("tertiary",)
    secondary_keywords = ("secondary", "general hospital", "specialist")
    for f in Hospital.objects.only(
        "name", "address", "location", "state", "lga", "ward",
        "has_emergency", "has_ambulance", "has_mortuary", "category", "ownership",
        "function_type", "status",
    ):
        loc = f.location
        if not loc:
            continue
        ft = (f.function_type or "").lower()
        has_ambulance = f.has_ambulance or any(k in ft for k in secondary_keywords + tertiary_keywords)
        has_mortuary = f.has_mortuary or any(k in ft for k in tertiary_keywords)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [loc.x, loc.y]},
            "properties": {
                "name": f.name, "type": "hospital",
                "address": f.address or "",
                "state": f.state or "", "lga": f.lga or "",
                "ward": f.ward or "",
                "has_emergency": f.has_emergency,
                "has_ambulance": has_ambulance,
                "has_mortuary": has_mortuary,
                "category": f.category or "",
                "ownership": f.ownership or "",
                "facility_type": f.function_type or "",
                "status": f.status or "",
            },
        })

    # Road Safety / Fire stations from Facility model
    for f in Facility.objects.only("name", "address", "location", "state", "lga"):
        loc = f.location
        if not loc:
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [loc.x, loc.y]},
            "properties": {
                "name": f.name, "type": f.name,
                "address": f.address or "",
                "state": f.state or "", "lga": f.lga or "",
            },
        })

    data = {"type": "FeatureCollection", "features": features}
    cache.set("map:facilities", data, 600)
    return JsonResponse(data)


@login_required
def map_traffic(request):
    from traffic.models import TrafficIncident, Road
    features = []
    # Active traffic incidents
    for inc in TrafficIncident.objects.filter(status="active").select_related()[:200]:
        loc = getattr(inc, "location", None)
        if not loc:
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [loc.x, loc.y]},
            "properties": {
                "type": "incident",
                "incident_type": inc.incident_type,
                "severity": inc.severity,
                "road": inc.road_name,
                "description": inc.description[:120] if inc.description else "",
            },
        })
    # Road segments with latest congestion
    for road in Road.objects.filter(is_monitored=True).prefetch_related("traffic_flows"):
        geom = getattr(road, "geometry", None)
        if not geom:
            continue
        flow = road.traffic_flows.order_by("-measured_at").first()
        congestion = flow.congestion_level if flow else "unknown"
        coords = list(geom.coords)  # list of (lng, lat) tuples
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "type": "road",
                "name": road.name or "",
                "congestion": congestion,
                "speed": flow.average_speed if flow else None,
            },
        })
    return JsonResponse({"type": "FeatureCollection", "features": features})


@login_required
def map_weather(request):
    cached = cache.get("map:weather")
    if cached:
        return JsonResponse(cached, safe=False)
    from traffic.models import Weather
    features = []
    for w in Weather.objects.select_related("road").order_by("-observed_at")[:50]:
        loc = getattr(w, "location", None)
        if not loc:
            continue
        area = w.road.name if w.road else ""
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [loc.x, loc.y]},
            "properties": {
                "condition": w.condition_type, "severity": w.severity,
                "temp": w.temperature, "wind": w.wind_speed,
                "rain": w.precipitation, "area": area,
                "description": w.description[:80] if w.description else "",
            },
        })
    data = {"type": "FeatureCollection", "features": features}
    cache.set("map:weather", data, 600)
    return JsonResponse(data)

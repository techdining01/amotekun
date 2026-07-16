from typing import Optional, Dict, Any
import os
from django.db.models import Count
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from ..model_io import load_model, MockModel
from analytics.models import Hotspot


class PredictionService:
    """Supports a persisted model (pickle) via model_io.
    Falls back to MockModel if no model file is found.
    """

    def __init__(self, model_path: Optional[str] = None):
        model_path = model_path or os.path.join(os.getcwd(), "models", "traffic_model.pkl")
        try:
            self.model = load_model(model_path)
        except Exception:
            self.model = MockModel()

    def predict(self, lat: float, lng: float, snapshot: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return a prediction dict: {'congestion_probability': float, 'meta': {...}}"""
        if hasattr(self.model, "predict"):
            try:
                prob = float(self.model.predict(lat=lat, lng=lng, snapshot=snapshot))
            except Exception:
                prob = float(self.model.simple_score(lat=lat, lng=lng, snapshot=snapshot))
        else:
            prob = float(self.model.simple_score(lat=lat, lng=lng, snapshot=snapshot))

        prob = max(0.0, min(1.0, prob))
        return {
            "congestion_probability": prob,
            "meta": {"model": getattr(self.model, "name", "mock")},
        }

    def hotspot_risk(self, lat: float, lng: float, radius_km: float = 2.0) -> Dict[str, Any]:
        """
        Returns a combined risk score for a point based on nearby hotspot
        intensity (60%) and ML congestion probability (40%).
        """
        point = Point(lng, lat, srid=4326)
        nearby = Hotspot.objects.filter(location__distance_lte=(point, D(km=radius_km)))

        if not nearby.exists():
            hotspot_score = 0.0
            dominant_type = None
        else:
            scores = list(nearby.values_list("intensity_score", flat=True))
            hotspot_score = min(1.0, sum(scores) / len(scores))
            dominant = (
                nearby.values("hotspot_type")
                .annotate(cnt=Count("id"))
                .order_by("-cnt")
                .first()
            )
            dominant_type = dominant.get("hotspot_type") if dominant else None

        prediction = self.predict(lat, lng)
        combined = round(prediction["congestion_probability"] * 0.4 + hotspot_score * 0.6, 4)

        return {
            "lat": lat,
            "lng": lng,
            "risk_score": combined,
            "hotspot_score": hotspot_score,
            "congestion_probability": prediction["congestion_probability"],
            "dominant_hotspot_type": dominant_type,
            "nearby_hotspot_count": nearby.count(),
        }

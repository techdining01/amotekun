import requests
from abc import ABC, abstractmethod
from django.utils import timezone
from decouple import config


class BaseTrafficProvider(ABC):
    name = "base"

    @abstractmethod
    def fetch_snapshot(self, road):
        """Return a dictionary of snapshot fields for the given road."""
        raise NotImplementedError

    @staticmethod
    def _point_from_geometry(road):
        if not getattr(road, "geometry", None):
            return None
        coords = list(road.geometry.coords)
        if not coords:
            return None
        first = coords[0]
        return float(first[1]), float(first[0])

    @staticmethod
    def _map_congestion(jam_factor):
        try:
            jam = float(jam_factor)
        except (TypeError, ValueError):
            return "unknown"
        if jam < 2:
            return "free"
        if jam < 4:
            return "moderate"
        if jam < 8:
            return "heavy"
        return "severe"


class MockTrafficProvider(BaseTrafficProvider):
    name = "mock"

    def fetch_snapshot(self, road):
        return {
            "provider": self.name,
            "road": road,
            "road_name": road.name,
            "timestamp": timezone.now(),
            "average_speed": 0.0,
            "travel_time": 0.0,
            "congestion_level": "unknown",
            "geometry": getattr(road, "geometry", None),
            "incident_count": 0,
            "camera_count": 0,
            "weather_condition": "",
            "raw_data": {"note": "mock provider placeholder"},
        }


class TomTomTrafficProvider(BaseTrafficProvider):
    name = "tomtom"

    def __init__(self, api_key=None):
        self.api_key = api_key or config("TOMTOM_API_KEY", default=None)
        if not self.api_key:
            raise RuntimeError("TOMTOM_API_KEY is not configured")

    def fetch_snapshot(self, road):
        point = self._point_from_geometry(road)
        if not point:
            raise ValueError("Road geometry is required for TomTom traffic lookup.")
        lat, lon = point
        url = (
            "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
        )
        params = {
            "point": f"{lat},{lon}",
            "unit": "KMH",
            "key": self.api_key,
        }
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json().get("flowSegmentData", {})

        speed = data.get("currentSpeed")
        travel_time = data.get("currentTravelTime")
        jam_factor = data.get("jamFactor")
        road_name = data.get("roadName") or road.name
        geometry = getattr(road, "geometry", None)

        return {
            "provider": self.name,
            "road": road,
            "road_name": road_name,
            "timestamp": timezone.now(),
            "average_speed": speed if speed is not None else 0.0,
            "travel_time": travel_time if travel_time is not None else 0.0,
            "congestion_level": self._map_congestion(jam_factor),
            "geometry": geometry,
            "incident_count": 0,
            "camera_count": 0,
            "weather_condition": "",
            "raw_data": data,
        }


class HereTrafficProvider(BaseTrafficProvider):
    name = "here"

    def __init__(self, api_key=None):
        self.api_key = api_key or config("HERE_API_KEY", default=None)
        if not self.api_key:
            raise RuntimeError("HERE_API_KEY is not configured")

    def fetch_snapshot(self, road):
        point = self._point_from_geometry(road)
        if not point:
            raise ValueError("Road geometry is required for HERE traffic lookup.")
        lat, lon = point
        url = "https://traffic.ls.hereapi.com/traffic/6.2/flow.json"
        params = {
            "apiKey": self.api_key,
            "prox": f"{lat},{lon},1000",
            "units": "metric",
        }
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()

        current_flow = None
        for rws in payload.get("RWS", []):
            for rw in rws.get("RW", []):
                for fis in rw.get("FIS", []):
                    for fi in fis.get("FI", []):
                        for cf in fi.get("CF", []):
                            current_flow = cf
                            break
                        if current_flow:
                            break
                    if current_flow:
                        break
                if current_flow:
                    break
            if current_flow:
                break

        if not current_flow:
            raise RuntimeError("HERE traffic response contains no flow measurement.")

        speed = current_flow.get("SP")
        travel_time = current_flow.get("TT")
        jam_factor = current_flow.get("JF")
        road_name = current_flow.get("DE") or road.name
        geometry = getattr(road, "geometry", None)

        return {
            "provider": self.name,
            "road": road,
            "road_name": road_name,
            "timestamp": timezone.now(),
            "average_speed": speed if speed is not None else 0.0,
            "travel_time": travel_time if travel_time is not None else 0.0,
            "congestion_level": self._map_congestion(jam_factor),
            "geometry": geometry,
            "incident_count": 0,
            "camera_count": 0,
            "weather_condition": "",
            "raw_data": current_flow,
        }


def get_traffic_provider(provider_name: str):
    provider_name = provider_name.lower()
    if provider_name == "tomtom":
        return TomTomTrafficProvider()
    if provider_name == "here":
        return HereTrafficProvider()
    if provider_name == "mock":
        return MockTrafficProvider()
    raise ValueError(f"Unknown traffic provider: {provider_name}")

import pickle
import os
from typing import Any, Optional


class MockModel:
    name = "mock-linear"

    def simple_score(
        self, lat: float, lng: float, snapshot: Optional[dict] = None
    ) -> float:
        """A deterministic scoring function for scaffolding purposes.

        Uses snapshot fields if present (incident_count, camera_count), falling
        back to a simple function of lat/lng.
        """
        base = ((abs(lat) % 1) + (abs(lng) % 1)) / 2.0
        if snapshot and isinstance(snapshot, dict):
            incidents = float(snapshot.get("incident_count", 0))
            cameras = float(snapshot.get("camera_count", 0))
            # simple heuristic: more incidents -> higher congestion
            score = min(
                1.0,
                base * 0.5
                + min(1.0, incidents / 20.0) * 0.7
                + min(1.0, cameras / 10.0) * 0.3,
            )
        else:
            score = min(1.0, base)

        return score


def save_model(path: str, model: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        pickle.dump(model, fh)


def load_model(path: str) -> Any:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "rb") as fh:
        return pickle.load(fh)

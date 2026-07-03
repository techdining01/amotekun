from typing import Optional, Dict, Any
import os
from .model_io import load_model, MockModel


class PredictionService:
    """This class supports loading a persisted model (pickle) via `model_io`.
    If no model is available, it uses a lightweight `MockModel` that
    computes a deterministic congestion probability from a snapshot.
    """

    def __init__(self, model_path: Optional[str] = None):
        model_path = model_path or os.path.join(
            os.getcwd(), "models", "traffic_model.pkl"
        )
        model = None
        try:
            model = load_model(model_path)
        except Exception:
            model = MockModel()

        self.model = model

    def predict(
        self, lat: float, lng: float, snapshot: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Return a prediction dictionary for the given point and optional snapshot.

        The contract is intentionally simple to make it easy to replace with a
        real ML model later: returns {'congestion_probability': float, 'meta': {...}}
        """
        # If the model exposes a `predict` method, call it.
        if hasattr(self.model, "predict"):
            try:
                prob = float(self.model.predict(lat=lat, lng=lng, snapshot=snapshot))
            except Exception:
                prob = float(
                    self.model.simple_score(lat=lat, lng=lng, snapshot=snapshot)
                )
        else:
            prob = float(self.model.simple_score(lat=lat, lng=lng, snapshot=snapshot))

        prob = max(0.0, min(1.0, prob))

        return {
            "congestion_probability": prob,
            "meta": {
                "model": getattr(self.model, "name", "mock"),
            },
        }

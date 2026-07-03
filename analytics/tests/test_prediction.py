from django.test import TestCase

from ..prediction import PredictionService


class PredictionServiceTest(TestCase):
    def test_predict_returns_probability(self):
        svc = PredictionService()
        res = svc.predict(
            6.5244, 3.3792, snapshot={"incident_count": 5, "camera_count": 2}
        )
        self.assertIn("congestion_probability", res)
        prob = res["congestion_probability"]
        self.assertIsInstance(prob, float)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

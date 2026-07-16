from django.db.models import Avg

from analytics.models import (
    Hotspot,
    HotspotAnalysis,
)

from chat.models import ChatMessage
from analytics.services.prediction_service import PredictionService

class AIService:
    """
    Central AI façade.
    Dashboard never imports PredictionService
    directly.
    All AI requests pass through here.
    """

    def __init__(self):
        self.predictor = PredictionService()
        
    def predict_traffic( self, lat, lng, snapshot=None,):

            return self.predictor.predict(

                lat=lat,

                lng=lng,

                snapshot=snapshot,

            )

    def crime_hotspots(self):

        return (

            Hotspot.objects

            .filter(

                hotspot_type="crime"

            )

            .order_by(

                "-intensity_score"

            )

        )

    def traffic_trends(self):

        return (
            HotspotAnalysis.objects
            .filter(
                analysis_type="traffic_trend"
            )
            .order_by("-created_at")
            .first()
        )

    def top_hotspots(self, limit=10):

        return (

            Hotspot.objects

            .order_by(

                "-intensity_score"

            )[:limit]

        )

    def latest_analysis(self):

        return (

            HotspotAnalysis.objects

            .first()

        )

    def recent_analysis(self, limit=10):

        return (

            HotspotAnalysis.objects

            .order_by(

                "-created_at"

            )[:limit]

        )

    def statistics(self):

        return {

            "total_hotspots":

                Hotspot.objects.count(),

            "crime":

                Hotspot.objects.filter(
                    hotspot_type="crime"
                ).count(),

            "traffic":

                Hotspot.objects.filter(
                    hotspot_type="traffic"
                ).count(),

            "violence":

                Hotspot.objects.filter(
                    hotspot_type="violence"
                ).count(),

            "average_intensity":

                Hotspot.objects.aggregate(
                    Avg("intensity_score")
                )["intensity_score__avg"] or 0,

            "analysis":

                HotspotAnalysis.objects.count(),

        }       

    def dashboard_summary(self):

        return (

            Hotspot.objects

            .order_by(

                "-intensity_score"

            )[:10]

        )

    def national_summary(self):

        stats = self.statistics()

        highest = (

            Hotspot.objects

            .order_by(

                "-intensity_score"

            )

            .first()

        )

        return {

            "stats": stats,

            "highest_hotspot": highest,

            "recent_analysis":

                self.recent_analysis(5),

        }

    def recommendations(self):

        recommendations = []

        hotspot = (

            Hotspot.objects

            .order_by(

                "-intensity_score"

            )

            .first()

        )

        if hotspot:

            recommendations.append({

                "priority": "HIGH",

                "title": "Deploy Patrol",

                "description":

                    f"High {hotspot.hotspot_type} activity detected.",

            })

        return recommendations



    def unread_messages(self):

        return ChatMessage.objects.filter(is_read=False).count()
from collections import defaultdict
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.measure import D
from reports.models import Incident
from analytics.models import Hotspot


class ClusteringService:
    """
    DBSCAN-inspired spatial clustering of incidents.
    Groups nearby incidents into clusters and returns Hotspot instances.
    """

    def __init__(self, radius_km: float = 1.0, min_samples: int = 2):
        self.radius_km = radius_km
        self.min_samples = min_samples

    def _get_neighbors(self, incident, candidates):
        return [
            c for c in candidates
            if c.pk != incident.pk
            and incident.geometry.distance(c.geometry) <= D(km=self.radius_km).m / 111320
        ]

    def cluster(self, hotspot_type: str = "crime"):
        type_map = {
            "crime": ["crime", "violence"],
            "violence": ["violence"],
            "traffic": ["accident"],
        }
        report_types = type_map.get(hotspot_type, [hotspot_type])
        incidents = list(Incident.objects.filter(report_type__in=report_types))

        labels = {i.pk: -1 for i in incidents}  # -1 = noise
        cluster_id = 0

        for incident in incidents:
            if labels[incident.pk] != -1:
                continue

            neighbors = self._get_neighbors(incident, incidents)

            if len(neighbors) < self.min_samples - 1:
                labels[incident.pk] = -1  # noise
                continue

            labels[incident.pk] = cluster_id
            queue = list(neighbors)

            while queue:
                neighbor = queue.pop(0)
                if labels[neighbor.pk] == -1:
                    labels[neighbor.pk] = cluster_id
                if labels[neighbor.pk] != -1:
                    continue
                labels[neighbor.pk] = cluster_id
                sub_neighbors = self._get_neighbors(neighbor, incidents)
                if len(sub_neighbors) >= self.min_samples - 1:
                    queue.extend(sub_neighbors)

            cluster_id += 1

        # Group incidents by cluster
        clusters = defaultdict(list)
        for incident in incidents:
            cid = labels[incident.pk]
            if cid != -1:
                clusters[cid].append(incident)

        return clusters

    def build_hotspots(self, hotspot_type: str = "crime"):
        """
        Runs clustering and saves a Hotspot for each cluster centroid.
        Returns list of created Hotspot instances.
        """
        clusters = self.cluster(hotspot_type=hotspot_type)
        hotspots = []

        for members in clusters.values():
            count = len(members)
            points = MultiPoint([m.geometry for m in members], srid=4326)
            centroid = points.centroid
            intensity = min(1.0, count / 20.0)

            hotspot = Hotspot.objects.create(
                location=centroid,
                hotspot_type=hotspot_type,
                intensity_score=intensity,
                incident_count=count,
            )
            hotspots.append(hotspot)

        return hotspots

    def cluster_summary(self, hotspot_type: str = "crime"):
        """Returns a summary dict of cluster stats without saving to DB."""
        clusters = self.cluster(hotspot_type=hotspot_type)
        return {
            "total_clusters": len(clusters),
            "total_incidents_clustered": sum(len(v) for v in clusters.values()),
            "clusters": [
                {
                    "cluster_id": cid,
                    "incident_count": len(members),
                    "centroid": {
                        "lat": MultiPoint([m.geometry for m in members], srid=4326).centroid.y,
                        "lon": MultiPoint([m.geometry for m in members], srid=4326).centroid.x,
                    },
                    "intensity_score": min(1.0, len(members) / 20.0),
                }
                for cid, members in clusters.items()
            ],
        }

from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


class VehicleQuerySet(models.QuerySet):

    def available(self):
        return self.filter(status="AVAILABLE")

    def assigned(self):
        return self.filter(status="ASSIGNED")

    def on_patrol(self):
        return self.filter(status="ON_PATROL")

    def maintenance(self):
        return self.filter(status="MAINTENANCE")

    def active(self):
        return self.exclude(status="OUT_OF_SERVICE")


class VehicleManager(models.Manager):

    def get_queryset(self):
        return VehicleQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def assigned(self):
        return self.get_queryset().assigned()

    def on_patrol(self):
        return self.get_queryset().on_patrol()

    def maintenance(self):
        return self.get_queryset().maintenance()

    def active(self):
        return self.get_queryset().active()


class PatrolMissionQuerySet(models.QuerySet):

    def active(self):
        return self.exclude(status="COMPLETED").exclude(status="CANCELLED")

    def completed(self):
        return self.filter(status="COMPLETED")

    def today(self):
        from django.utils import timezone
        return self.filter(started_at__date=timezone.now().date())

    def in_progress(self):
        return self.filter(status="EN_ROUTE")

    def arrived(self):
        return self.filter(status="ARRIVED")


class PatrolMissionManager(models.Manager):

    def get_queryset(self):
        return PatrolMissionQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def completed(self):
        return self.get_queryset().completed()

    def today(self):
        return self.get_queryset().today()

    def in_progress(self):
        return self.get_queryset().in_progress()


class PatrolTeamQuerySet(models.QuerySet):

    def available(self):
        return self.filter(status="AVAILABLE")

    def dispatched(self):
        return self.filter(status="DISPATCHED")

    def on_patrol(self):
        return self.filter(status="ON_PATROL")

    def active(self):
        return self.filter(active=True)


class PatrolTeamManager(models.Manager):

    def get_queryset(self):
        return PatrolTeamQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def on_patrol(self):
        return self.get_queryset().on_patrol()

    def active(self):
        return self.get_queryset().active()


class GPSQuerySet(models.QuerySet):

    def most_recent(self):
        return self.order_by("-recorded_at")

    def today(self):
        from django.utils import timezone
        return self.filter(recorded_at__date=timezone.now().date())

    def recent(self, minutes=30):
        from django.utils import timezone
        from datetime import timedelta
        return self.filter(recorded_at__gte=timezone.now() - timedelta(minutes=minutes))


class GPSManager(models.Manager):

    def get_queryset(self):
        return GPSQuerySet(self.model, using=self._db)

    def most_recent(self):
        return self.get_queryset().most_recent()

    def recent(self, minutes=30):
        return self.get_queryset().recent(minutes)


class GISManager(models.Manager):

    def nearby(self, point, radius=5):
        return self.get_queryset().filter(
            location__distance_lte=(point, D(km=radius))
        )

    def ordered_by_distance(self, point):
        return self.get_queryset().annotate(
            distance=Distance("location", point)
        ).order_by("distance")


class PatrolAnalyticsManager(models.Manager):

    def summary(self):
        from django.utils import timezone
        qs = self.get_queryset()
        return {
            "missions": qs.count(),
            "active": qs.exclude(status="COMPLETED").exclude(status="CANCELLED").count(),
            "completed": qs.filter(status="COMPLETED").count(),
            "today": qs.filter(started_at__date=timezone.now().date()).count(),
        }

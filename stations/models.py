from django.db import models
from django.contrib.gis.db import models as gis_models


class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = gis_models.PointField(srid=4326, geography=True, null=True, blank=True)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AmotekunStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = gis_models.PointField(srid=4326, geography=True, null=True, blank=True)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    location = gis_models.PointField(srid=4326, geography=True, null=True, blank=True)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
    has_emergency = models.BooleanField(default=True)

    def __str__(self):
        return self.name

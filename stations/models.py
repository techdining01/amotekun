from unicodedata import category

from django.db import models
from django.contrib.gis.db import models as gis_models


class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=255, null=True, blank=True)  # Store as "lat,lng" string for SQLite
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
    address = models.CharField(max_length=200, blank=True, null=True)
    location = gis_models.PointField(srid=4326, geography=True, null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    lga = models.CharField(max_length=100, blank=True, null=True)
    has_emergency = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)
    ownership = models.CharField(max_length=100, blank=True, null=True)
    function_type = models.CharField(max_length=100, blank=True, null=True)
    function = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

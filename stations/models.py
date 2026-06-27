from django.contrib.gis.db import models


class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = models.PointField(srid=4326, null=True, blank=True)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AmotekunStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = models.PointField(srid=4326, null=True, blank=True)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)

    def __str__(self):
        return self.name

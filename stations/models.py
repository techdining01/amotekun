from django.contrib.gis.db import models 


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
    location = models.PointField(srid=4326, geography=True, null=True, blank=True)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    location = models.PointField(srid=4326, geography=True, null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    lga = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    has_emergency = models.BooleanField(default=False)
    has_ambulance = models.BooleanField(default=False)
    has_mortuary = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)
    ownership = models.CharField(max_length=100, blank=True, null=True)
    function_type = models.CharField(max_length=100, blank=True, null=True)
    function = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        ft = (self.function_type or "").lower()
        if "secondary" in ft:
            self.has_ambulance = True
        if "tertiary" in ft:
            self.has_ambulance = True
            self.has_mortuary = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Facility(models.Model):
    FACILITY_TYPE = [
        ("police", "Police Station"),
        ("amotekun", "Amotekun Station"),
        ("hospital", "Hospital"),
        ("fire_station", "Fire Station"),
        ("road_safety", "Road Safety Center"),
    ]
    
    name = models.CharField(max_length=100, choices=FACILITY_TYPE)
    address = models.CharField(max_length=200, blank=True, null=True)
    location = models.PointField(srid=4326, geography=True, null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    lga = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
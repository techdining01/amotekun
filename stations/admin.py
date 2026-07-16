from django.contrib import admin
from .models import PoliceStation, AmotekunStation, Hospital, Facility


@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'lga', 'address']
    list_filter = ['state', 'lga']
    search_fields = ['name', 'address']


@admin.register(AmotekunStation)
class AmotekunStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'lga', 'address']
    list_filter = ['state', 'lga']
    search_fields = ['name', 'address']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'lga', 'has_emergency', 'category', 'ownership']
    list_filter = ['state', 'has_emergency', 'category', 'ownership']
    search_fields = ['name', 'address']


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'lga', 'address']
    list_filter = ['state', 'lga']
    search_fields = ['name']

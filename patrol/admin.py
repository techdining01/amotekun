from django.contrib import admin
from .models import (
    VehicleType, Vehicle, PatrolTeam, PatrolMembership, VehicleAssignment,
    PatrolMission, PatrolCheckpoint, GPSPosition, PatrolShift,
    PatrolEquipment, EquipmentAssignment, VehicleMaintenance, VehicleFuelLog,
)


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'make', 'model', 'status', 'fuel_type', 'agency']
    list_filter = ['status', 'fuel_type', 'agency']
    search_fields = ['registration_number', 'make', 'model']
    readonly_fields = ['created_at']


@admin.register(PatrolTeam)
class PatrolTeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'team_type', 'status', 'active', 'agency', 'commander']
    list_filter = ['status', 'team_type', 'active', 'agency']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(PatrolMission)
class PatrolMissionAdmin(admin.ModelAdmin):
    list_display = ['dispatch', 'patrol_team', 'priority', 'status', 'started_at', 'completed_at']
    list_filter = ['status', 'priority']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(PatrolShift)
class PatrolShiftAdmin(admin.ModelAdmin):
    list_display = ['team', 'shift_type', 'starts_at', 'ends_at', 'active']
    list_filter = ['shift_type', 'active']


@admin.register(PatrolEquipment)
class PatrolEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'serial_number', 'status', 'agency']
    list_filter = ['equipment_type', 'status']
    search_fields = ['name', 'serial_number']


@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'status', 'scheduled_date', 'completed_date']
    list_filter = ['status']


@admin.register(VehicleFuelLog)
class VehicleFuelLogAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'litres', 'amount', 'odometer', 'created_at']
    readonly_fields = ['created_at']


admin.site.register(PatrolMembership)
admin.site.register(VehicleAssignment)
admin.site.register(PatrolCheckpoint)
admin.site.register(GPSPosition)
admin.site.register(EquipmentAssignment)

from django.contrib import admin
from .models import MobileDevice, PushNotification


@admin.register(MobileDevice)
class MobileDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'device_name', 'is_active', 'last_used', 'registered_at']
    list_filter = ['device_type', 'is_active', 'registered_at']
    search_fields = ['user__username', 'device_id', 'device_name']
    readonly_fields = ['registered_at', 'last_used']


@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'status', 'created_at', 'sent_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'recipient__username']
    readonly_fields = ['created_at', 'sent_at']

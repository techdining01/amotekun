from django.contrib import admin
from .models import Dispatch, DispatchHistory


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ['reference', 'status', 'priority', 'state', 'lga', 'created_at']
    list_filter = ['status', 'priority', 'state']
    search_fields = ['reference', 'state', 'lga']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DispatchHistory)
class DispatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['dispatch', 'user', 'action', 'created_at']
    list_filter = ['created_at']
    search_fields = ['dispatch__reference', 'action']
    readonly_fields = ['created_at']

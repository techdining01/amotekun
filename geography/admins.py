from django.contrib import admin
from .models import GeographyBoundary

@admin.register(GeographyBoundary)
class GeographyBoundaryAdmin(admin.ModelAdmin):
    list_display = ("name", "boundary_type", "created_at")
    search_fields = ("name",)
    list_filter = ("boundary_type",)



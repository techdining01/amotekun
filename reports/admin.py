from django.contrib import admin
from .models import LGA, FloodZone, Incident, IncidentMedia, IncidentHistory, State, LGA, Ward



admin.site.register(Incident)
admin.site.register(IncidentMedia)
admin.site.register(IncidentHistory)
admin.site.register(FloodZone)
admin.site.register(State)
admin.site.register(LGA)
admin.site.register(Ward)
      

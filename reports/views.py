from django.shortcuts import render
from rest_framework import viewsets
from .models import Incident,  LGA
from .serializers import IncidentSerializer, LGASerializer
from rest_framework.generics import ListAPIView

def home(request):
    return render(request, "index.html")


class IncidentViewset(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class YorubaLGAAPIView(ListAPIView):
    serializer_class = LGASerializer

    def get_queryset(self):

        yoruba_states = ["Lagos", "Ogun", "Oyo", "Osun", "Ondo", "Ekiti"]

        return LGA.objects.filter(state__name__in=yoruba_states)
    
class StateLGAAPIView(ListAPIView):
    serializer_class = LGASerializer

    def get_queryset(self):

        state_name = self.kwargs["state_name"]

        return LGA.objects.filter(state__name=state_name)
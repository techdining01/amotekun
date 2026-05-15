from django.shortcuts import render
from rest_framework import viewsets
from .models import Reports, LGA
from .serializers import ReportsSerializer, LGASerializer
from rest_framework.generics import ListAPIView

def home(request):
    return render(request, "index.html")


class ReportViewset(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer


class YorubaLGAAPIView(ListAPIView):
    serializer_class = LGASerializer

    def get_queryset(self):

        yoruba_states = ["Lagos", "Ogun", "Oyo", "Osun", "Ondo", "Ekiti"]

        return LGA.objects.filter(state__name__in=yoruba_states)
    
    
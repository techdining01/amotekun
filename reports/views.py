from django.shortcuts import render
from rest_framework import viewsets
from .models import Reports
from .serializers import ReportsSerializer


def home(request):
    return render(request, "index.html")


class ReportViewset(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

from django.shortcuts import render
from rest_framework import viewsets
from .models import Reports
from .serializers import ReportsSerializer


class ReportView(viewsets.ModelViewset):
    


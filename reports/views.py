from django.shortcuts import render
from django.contrib.gis.geos import Point
from rest_framework import viewsets
from .models import Incident,  LGA
from .serializers import IncidentSerializer, LGASerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


def incident_create_view(request):
    """HTMX view for creating incidents"""
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        title = request.POST.get('title')
        description = request.POST.get('description')
        report_type = request.POST.get('report_type')
        
        if latitude and longitude:
            try:
                lng = float(longitude)
                lat = float(latitude)
                point = Point(lng, lat, srid=4326)
                
                state_name, lga_name = get_location_from_point(point)
                
                incident = Incident.objects.create(
                    title=title,
                    description=description,
                    report_type=report_type,
                    state=state_name or 'Unknown',
                    lga=lga_name or 'Unknown',
                    geometry=point
                )
                from django.http import HttpResponse
                return HttpResponse(status=204, headers={'HX-Trigger': 'incidentAdded'})
            except (ValueError, TypeError):
                pass
    
    return render(request, 'cotton/incident_form_modal.html')


def get_location_from_point(point):
    """Determine state and LGA from coordinates"""
    try:
        from .models import LGA
        lga = LGA.objects.filter(geometry__contains=point).first()
        if lga:
            state_name = lga.state.name if lga.state else 'Unknown'
            return state_name, lga.name
    except Exception:
        pass
    return None, None


class IncidentCreateAPIView(CreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        latitude = data.get('latitude') or request.POST.get('latitude')
        longitude = data.get('longitude') or request.POST.get('longitude')
        
        if latitude and longitude:
            try:
                lng = float(longitude)
                lat = float(latitude)
                data['geometry'] = Point(lng, lat, srid=4326)
                
                state_name = data.get('state') or request.POST.get('state')
                lga_name = data.get('lga') or request.POST.get('lga')
                
                if not state_name or state_name == 'Unknown':
                    state_name, lga_name = self.get_location_from_point(Point(lng, lat))
                
                data['state'] = state_name or 'Unknown'
                data['lga'] = lga_name or 'Unknown'
            except (ValueError, TypeError):
                pass
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        if request.htmx:
            from django.http import HttpResponse
            return HttpResponse(status=204, headers={'HX-Trigger': 'incidentAdded'})
        
        return Response(serializer.data, status=201, headers=headers)
    
    def get_location_from_point(self, point):
        try:
            from .models import LGA
            lga = LGA.objects.filter(geometry__contains=point).first()
            if lga:
                state_name = lga.state.name if lga.state else 'Unknown'
                return state_name, lga.name
        except Exception:
            pass
        return None, None


class IncidentViewset(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude and longitude:
            try:
                lng = float(longitude)
                lat = float(latitude)
                data['geometry'] = Point(lng, lat, srid=4326)
                
                state_name = data.get('state')
                lga_name = data.get('lga')
                
                if not state_name or state_name == 'Unknown':
                    state_name, lga_name = get_location_from_point(Point(lng, lat))
                
                data['state'] = state_name or 'Unknown'
                data['lga'] = lga_name or 'Unknown'
            except (ValueError, TypeError):
                pass
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


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
    
class HotspotAPIView(APIView):
    def get(self, request):

        hotspots = []

        lgas = LGA.objects.all()

        for lga in lgas:
            count = Incident.objects.filter(geometry__within=lga.geometry).count()

            hotspots.append({"id": lga.id, "name": lga.name, "count": count})

        return Response(hotspots)


class LGACentroidAPIView(APIView):
    def get(self, request, pk):
        try:
            lga = LGA.objects.get(pk=pk)
            centroid = lga.geometry.centroid
            return Response({
                "id": lga.id,
                "name": lga.name,
                "latitude": centroid.y,
                "longitude": centroid.x,
                "state": lga.state.name if lga.state else None
            })
        except LGA.DoesNotExist:
            return Response({"error": "LGA not found"}, status=404)


class IncidentTypeFilterView(APIView):
    def get(self, request, report_type=None):
        incidents = Incident.objects.all()
        if report_type:
            incidents = incidents.filter(report_type=report_type)
        incidents_geojson = IncidentSerializer(incidents, many=True)
        return Response(incidents_geojson.data)

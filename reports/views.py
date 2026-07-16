from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from django.core.cache import cache
from rest_framework import viewsets
from .models import Incident, State, LGA, Ward
from .serializers import IncidentSerializer, LGASerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import IncidentForm


def get_lgas(request):
    state_id = request.GET.get('state')
    css = 'w-full px-4 py-2 border border-slate-200 rounded-lg'
    if state_id:
        cache_key = f"lgas_html:{state_id}"
        html = cache.get(cache_key)
        if not html:
            try:
                lgas = LGA.objects.filter(state_id=state_id).order_by('name')
                options = '<option value="">Select an LGA</option>'
                for lga in lgas:
                    options += f'<option value="{lga.id}" data-centroid-url="/api/lga-centroid/{lga.id}/">{lga.name}</option>'
                html = f'<select name="lga" id="id_lga" class="{css}" hx-get="/api/get-wards/" hx-target="#ward-select-wrapper" hx-swap="innerHTML" hx-trigger="change" onchange="onLgaChange(this)">{options}</select>'
                cache.set(cache_key, html, 3600)
            except Exception:
                html = None
        if html:
            return HttpResponse(html)
    return HttpResponse(f'<select name="lga" id="id_lga" class="{css}" hx-get="/api/get-wards/" hx-target="#ward-select-wrapper" hx-swap="innerHTML" hx-trigger="change"><option value="">Select an LGA</option></select>')


def get_wards(request):
    lga_id = request.GET.get('lga')
    css = 'w-full px-4 py-2 border border-slate-200 rounded-lg'
    if lga_id:
        cache_key = f"wards_html:{lga_id}"
        html = cache.get(cache_key)
        if not html:
            try:
                wards = Ward.objects.filter(lga_id=lga_id).order_by('name')
                options = '<option value="">Select a Ward</option>'
                for ward in wards:
                    options += f'<option value="{ward.id}">{ward.name}</option>'
                html = f'<select name="ward" id="id_ward" class="{css}">{options}</select>'
                cache.set(cache_key, html, 3600)
            except Exception:
                html = None
        if html:
            return HttpResponse(html)
    return HttpResponse(f'<select name="ward" id="id_ward" class="{css}"><option value="">Select a Ward</option></select>')


def incident_create_view(request):
    req_type = request.GET.get('type', '')  # 'emergency', 'support', 'evidence', or ''
    is_support = req_type == 'support'

    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reporter = request.user if request.user.is_authenticated else None

            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')
            state_obj = form.cleaned_data.get('state')
            lga_obj = form.cleaned_data.get('lga')

            if latitude is not None and longitude is not None:
                try:
                    incident.geometry = Point(float(longitude), float(latitude), srid=4326)
                except (ValueError, TypeError):
                    pass

            if not incident.geometry:
                if lga_obj and lga_obj.geometry:
                    incident.geometry = lga_obj.geometry.centroid
                elif state_obj and state_obj.geometry:
                    incident.geometry = state_obj.geometry.centroid
                else:
                    incident.geometry = Point(3.3792, 6.5244, srid=4326)

            if state_obj:
                incident.state = state_obj.name
            else:
                state_name, _ = get_location_from_point(incident.geometry)
                incident.state = state_name or 'Unknown'

            if lga_obj:
                incident.lga = lga_obj.name
            else:
                _, lga_name = get_location_from_point(incident.geometry)
                incident.lga = lga_name or 'Unknown'

            incident.save()
            return HttpResponse('', status=204, headers={'HX-Trigger': 'incidentAdded'})
    else:
        initial = {}
        if req_type == 'emergency':
            initial['report_type'] = 'crime'
        form = IncidentForm(initial=initial)

    modal_title = {
        'emergency': '🚨 Report Emergency',
        'support':   '🤝 Request Support',
        'evidence':  '📸 Upload Evidence',
    }.get(req_type, '📝 Report Incident')

    return render(request, 'reports/incident_modal.html', {
        'form': form,
        'modal_title': modal_title,
        'is_support': is_support,
    })


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

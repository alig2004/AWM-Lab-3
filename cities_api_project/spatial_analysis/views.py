from django.shortcuts import render
from django.contrib.gis.db.models import Q
from django.contrib.gis.geos import Point
from .models import DublinAdminArea, DublinRoad, DublinPOI, LandUseZone
from django.contrib.gis.measure import D

def spatial_analysis_dashboard(request):
    """Dashboard showing spatial analysis of Dublin data"""

    context = {
        'total_admin_areas': DublinAdminArea.objects.count(),
        'total_roads': DublinRoad.objects.count(),
        'total_pois': DublinPOI.objects.count(),
        'total_zones': LandUseZone.objects.count(),

        'admin_areas': DublinAdminArea.objects.all(),
        'major_roads': DublinRoad.objects.filter(
            road_type__in=['motorway', 'main_street']
        ).order_by('-speed_limit'),
        'attractions': DublinPOI.objects.filter(
            poi_type__in=['attraction', 'historic']
        ).order_by('-rating'),
        'zones': LandUseZone.objects.all(),
        'dublin_lat': 53.3498,
        'dublin_lon':-6.2603,
    }

    return render(request, 'spatial_analysis/dashboard.html', context)

def poi_detail(request, pk):
    """Detail view for a single POI"""
    poi = DublinPOI.objects.get(pk=pk)

    # Find nearby roads (within 1km)
    nearby_roads = DublinRoad.objects.filter(
        geom__distance_lte=(poi.geom, D(m=1000))  # Approximately 1km at equator
    )#.order_by('geom__distance_to', poi.geom)[:5]

    #^ this creates a list/array of roads with a distance of less than 1km from poi
    #geom_distance_lte is a tuple?
    #is geom__distance_lte a specific thing? can i call it?

    context = {
        'poi': poi,
        'nearby_roads': nearby_roads,
        'poi_json': poi.geom.json,
    }

    return render(request, 'spatial_analysis/poi_detail.html', context)
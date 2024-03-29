import json
from .forms import RestaurantForm
from django.contrib.gis.geos import Point, Polygon, LinearRing
from django.contrib.gis.db.models.functions import Distance
from .models import Restaurant, Polygons
from .common import response, handling_badrequest, handling_server

def add_restaurant(request):
    try:   
        data = json.loads(request.body)
        
        restaurant_name = data['name']
        distance = data ['distance']
        location = Point(data['longitude'], data['latitude'], srid=4326)
        address = data['address']


        restaurant_data = {
            "restaurant_name" : restaurant_name,
            "distance" : distance,
            "location" : location,
            "address" : address
        }
        restaurant = RestaurantForm(restaurant_data)
        
        if(restaurant.is_valid):
            restaurant.save()


        return response("Restaurant Addedd!!!!")
    
    except Exception as e:
        return handling_server(str(e))

def nearby_restaurant(request):
    try:
        data = json.loads(request.body)

        lat = data['lat']
        long = data['long']
        distance = 0.1
        point = Point(long, lat, srid=4326)

        restaurant_within_radius = Restaurant.objects.filter(
            location__distance_lte = (
                point,
                distance
            )
        )
        
        restaurants = []
        for i in restaurant_within_radius:
            restaurant_data = {
                "name" : i.restaurant_name,
                "address" : i.address
            }
            restaurants.append(restaurant_data)
        
        return response(restaurants)
    except Exception as e:
        return handling_server(str(e))


def sortby_restaurant(request):
    try:
        data = json.loads(request.body)

        lat = data['lat']
        long = data['long']

        point = Point(long, lat, srid=4326)

        restaurant_sort_by_distance = Restaurant.objects.annotate(
            dis=Distance('location', point)
            ).order_by('dis').all()
            
        restaurants = []
        for i in restaurant_sort_by_distance:

            if isinstance(i.dis, float):
                formatted_distance = '{:.3f}'.format(i.dis)+"m"
            else:
                formatted_distance = '{:.3f}'.format(i.dis.km)+"km"

            restaurant_data = {
                "name" : i.restaurant_name,
                "address" : i.address,
                'distance': formatted_distance 
            }
            restaurants.append(restaurant_data)
        
        return response(restaurants, safe=False)
    
    except Exception as e:
        return handling_server(str(e))

def store_polygon(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        polygon_values = data.get('polygon_values')

        if not name or not polygon_values:
            return handling_badrequest('Name and polygon_values are required')

        points = [Point(p['longitude'], p['latitude']) for p in polygon_values]

        if points[0] != points[-1]:
            return handling_badrequest('Polygon is not closed')

        ring = LinearRing(points)

        polygon = Polygon(ring)

        try:
            polygon_obj = Polygons(name=name, geom=polygon)
            polygon_obj.save()
            return response('Polygon stored successfully')
        except Exception as e:
            return handling_badrequest(str(e))
        
    except Exception as e:
        return handling_server(str(e))
    

def point_in_polygon(request):
    try:
        data = json.loads(request.body)

        lat = data['lat']
        long = data['long']

        point = Point(long, lat, srid=4326) 

        polygons_containing_point = Polygons.objects.filter(geom__contains=point).all()
        
        polygon_name = ""
        for i in polygons_containing_point:
            polygon_name = i.name

        if polygons_containing_point.exists():
            result = f"Point is inside a polygon : {polygon_name}."
        else:
            result = "Point is outside all polygons."

        return response(result)
    except Exception as e:
        return handling_server(str(e))
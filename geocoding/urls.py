
from django.urls import path
from . import views

urlpatterns = [
    path('api/v2/add_restaurant', views.add_restaurant, name = 'add_restaurant'),
    path('api/v2/nearby_restaurant', views.nearby_restaurant, name='nearby_restaurant'),
    path('api/v2/sortby_restaurant', views.sortby_restaurant, name='sortby_restaurant'),
    path('api/v2/store_polygon', views.store_polygon, name='store_polygon'),
    path('api/v2/point_in_polygon', views.point_in_polygon, name='point_in_polygon')
]

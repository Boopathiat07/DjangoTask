from django.urls import path, include

urlpatterns = [
    path('', include('operation.urls')),
    path('', include('geocoding.urls'))
]

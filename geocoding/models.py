from django.contrib.gis.db import models


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant_name = models.CharField(max_length=200)
    distance = models.IntegerField()
    location = models.PointField()
    address = models.CharField(max_length=500)

    class Meta:
        db_table = 'restaurant' 


class Polygons(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    geom = models.PolygonField()

    class Meta:
        db_table = 'polygons'



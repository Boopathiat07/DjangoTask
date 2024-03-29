from django.db import models
from djongo import models as djongo_models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=10)
    password = models.CharField(max_length=500)

class Session(models.Model):

    jti = models.CharField(primary_key=True, max_length=200)
    email = models.EmailField()
    islogin = models.BooleanField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'session' 

class Employee(djongo_models.Model):
    id = djongo_models.ObjectIdField(primary_key = True)
    email = djongo_models.EmailField(unique=True)
    name = djongo_models.CharField(max_length=200)
    mobile_no = djongo_models.CharField(max_length=10)

    class Meta:
        db_table = 'employee'
        # app_label = 'mongodb'


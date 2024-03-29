from rest_framework import serializers
from .models import User, Session, Employee

from django import forms

class UserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class SessionForms(forms.ModelForm):
    class Meta:
        model = Session
        # fields =['jti', 'email', 'islogin', 'login_time']
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        






        
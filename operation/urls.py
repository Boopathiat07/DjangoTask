from django.urls import path
from . import views

urlpatterns = [
    #Class Views
    path('users', views.UserView.as_view(), name='user_view'),
    path('employees', views.EmployeeView.as_view(), name='employee_view'),
    #Google Views
    path('auth_login', views.google_auth_redirect, name='oauth_redirect'),
    path('auth/google/callback', views.google_auth_callback, name='oauth_google_callback'),
    path('google_view', views.GoogleView.as_view(), name='google_view'),
    # Function Views
    path('create_user', views.create_user, name='create_user'),
    path('get_user', views.fetch_user, name='get_user'),
    path('update_user', views.update_user, name='update_user'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('hello', views.home, name='home')
]

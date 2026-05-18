from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',register,name='register'),
    path('login/',log_in,name='log_in')
]
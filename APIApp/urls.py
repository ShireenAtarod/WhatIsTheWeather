from django.urls import path, include
from django.urls.resolvers import RoutePattern
from rest_framework import routers
from . import views


urlpatterns = [
    path('', views.getTemperature),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
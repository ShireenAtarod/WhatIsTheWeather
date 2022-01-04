from django.urls import path, include
from django.urls.resolvers import RoutePattern
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api', views.cityViewSet)

urlpatterns = [
    path('<cityname>', views.getTemperature),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
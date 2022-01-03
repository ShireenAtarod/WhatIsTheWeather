import requests
import redis
from django.http import JsonResponse
from django.conf import settings
# from requests.models import Response
from rest_framework.response import Response
from rest_framework import status
from .models import City
from .serializer import CitySerializer

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)

    
def getTemperature(request, cityname):
    if request.method == "GET":
        cityname = cityname.capitalize()

        # If the City Temperature exists Cache
        if redis_instance.exists(cityname):
            temp = redis_instance.get(cityname)
            city = City()
            city.name = cityname
            city.temperature = temp
            serializer = CitySerializer(city)
            return JsonResponse(serializer.data)

        # If the City Temperature exists in Database
        elif City.objects.filter(name = cityname).exists():
            query = City.objects.get(name = cityname)
            serializer = CitySerializer(query)
            return JsonResponse(serializer.data)
        
        # Then ask the outsource API
        else:
            url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=56d22c5baf937734fcfe1bd0e9b267fc"
            city_weather = requests.get(url.format(cityname)).json()

            if city_weather['cod'] == '200':
                newcity = City()
                newcity.name = cityname
                newcity.temperature = ConvertToCelsius(city_weather['main']['temp'])
                newcity.save()
                redis_instance.set(cityname, newcity.temperature, ex=68400)
                serializer = CitySerializer(newcity)
                return JsonResponse(serializer.data)
            else:
                response = {'message': 'City Not Found!'}
                return JsonResponse(response, status=404)
            

        
# Convert Fahrenheit to Celsuis
def ConvertToCelsius(fahrenheit):
    return round((fahrenheit - 32)*(5/9), 2)

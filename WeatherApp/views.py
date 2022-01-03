import requests
from django.shortcuts import render
from .forms import CityForm

def index(request):
    if request.method == "GET":
        form = CityForm()
        context = {'form': form}

    elif request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

        # Send request to local API
        url = "http://127.0.0.1:8000/city/{}"
        response = requests.get(url.format(name))

        if response.status_code == 200:
            city_weather = response.json()
            weather = {
                'city': city_weather['name'],
                'temp': city_weather['temperature']
            }
            context = {'data': weather, 'form': form}

        elif response.status_code == 404:
            error_message = response.json()
            error = {
                'city' : name,
                'message' : error_message['message']
            }
            context = {'error': error, 'form': form}

    return render(request, 'WeatherApp/index.html', context)

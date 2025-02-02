import requests
from django.shortcuts import render
from .forms import CityForm

API_KEY = '07e33c3da9b7aeb88be6580b521af1ca'

def get_weather_data(city=None, lat=None, lon=None):
    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    elif lat and lon:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    else:
        return None

    response = requests.get(url)
    return response.json()

def index(request):
    weather_data = None
    error_message = None
    form = CityForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        city = form.cleaned_data['city']
        weather_data = get_weather_data(city=city)
        if weather_data.get('cod') != 200:
            error_message = "City not found. Please try again."

    elif request.method == 'GET' and 'lat' in request.GET and 'lon' in request.GET:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        weather_data = get_weather_data(lat=lat, lon=lon)
        if weather_data.get('cod') != 200:
            error_message = "Could not retrieve weather for your location."

    return render(request, 'weather/index.html', {
        'form': form,
        'weather_data': weather_data,
        'error_message': error_message,
    })

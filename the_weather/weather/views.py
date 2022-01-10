import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=83b3df7530e04f0a54eba757f0992f41'
    err_msg=''
    if request.method=='POST':
        form=CityForm(request.POST)
        form.save()

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()

            if existing_city_count==0:
                r=requests.get(url.format(new_city)).json()
                if r['cod']== 200:
                    form.save()
                else:
                    err_msg="City doesnt exits"
            else:
                err_msg="City already exists"

    form = CityForm()

    cities=City.objects.all()
    weather_data=[]

    for city in cities:
        r=requests.get(url.format(city)).json()

        city_weather={
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
    }

        weather_data.append(city_weather)
    context={'weather_data':weather_data,'form':form}
    return render(request,'weather/weather.html',context)

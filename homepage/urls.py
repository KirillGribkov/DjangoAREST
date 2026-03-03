"""
URL configuration for personal_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from homepage import views
from adrf import routers


router = routers.DefaultRouter()
router.register('api/city',views.CityViewSet)
router.register('api/WeatherUser',views.WeatherUserSet)
router.register('api/WeatherUserCity',views.WeatherUserCitySet)

app_name = "homepage"

urlpatterns = [
    path('', include(router.urls)), 
    path('api/citys/', views.Citys.as_view(), name='citys'),
    path('apiurl/CitDayWeatherURL/', views.CitDayWeatherURL.as_view(), name='CitDayWeatherURL'),
    path('api/CitDayWeather/', views.CitDayWeather.as_view(), name='CitDayWeather'),
    path('apiurl/CoordsWeatherURL/', views.CoordsWeatherURL.as_view(), name='CoordsWeatherURL'),
    path('api/CoordsWeather/', views.CoordsWeather.as_view(), name='CoordsWeather'),
    path('apiurl/CityAppendURL/', views.CityAppendURL.as_view(), name='CityAppendURL'),
    path('api/CityAppend/', views.CityAppend.as_view(), name='CityAppend'),
    path('api/CityList/', views.CityList.as_view(), name='CityList'),
    path('apiurl/SavedCityWeatherURL/', views.SavedCityWeatherURL.as_view(), name='SavedCityWeatherURL'),
    path('api/SavedCityWeather/', views.SavedCityWeather.as_view(), name='SavedCityWeather'),
    path('apiurl/WeatherUserAppendURL/', views.WeatherUserAppendURL.as_view(), name='WeatherUserAppendURL'),
    path('api/WeatherUserAppend/', views.WeatherUserAppend.as_view(), name='WeatherUserAppend'),
    path('api/WeatherUsers/', views.WeatherUsers.as_view(), name='WeatherUsers'),
    path('apiurl/WeatherUserCityAppendURL/', views.WeatherUserCityAppendURL.as_view(), name='WeatherUserCityAppendURL'),
    path('api/WeatherUserCityAppend/', views.WeatherUserCityAppend.as_view(), name='WeatherUserCityAppend'),
    path('api/WeatherUserCities/', views.WeatherUserCities.as_view(), name='WeatherUserCities'),
    path('apiurl/SavedWeatherUserCityWeatherURL/', views.SavedWeatherUserCityWeatherURL.as_view(), name='SavedWeatherUserCityWeatherURL'),
    path('api/SavedWeatherUserCityWeather/', views.SavedWeatherUserCityWeather.as_view(), name='SavedWeatherUserCityWeather'),
    path('apiurl/WeatherUserCitDayWeatherURL/', views.WeatherUserCitDayWeatherURL.as_view(), name='WeatherUserCitDayWeatherURL'),
    path('api/WeatherUserCitDayWeather/', views.WeatherUserCitDayWeather.as_view(), name='WeatherUserCitDayWeather'),
    path('apiurl/WeatherUserCityListURL/', views.WeatherUserCityListURL.as_view(), name='WeatherUserCityListURL'),
    path('api/WeatherUserCityList/', views.WeatherUserCityList.as_view(), name='WeatherUserCityList'),
]

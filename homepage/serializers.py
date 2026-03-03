from adrf import serializers as async_serializers
from .models import City, WeatherUser, WeatherUserCity

class CitySerializer(async_serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'latitude', 'longitude']

class CityUpdateSerializer(async_serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'temperature', 'wind_speed', 'surface_pressure']

class CityNameSerializer(async_serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']

class WeatherUserIdSerializer(async_serializers.ModelSerializer):
    class Meta:
        model = WeatherUser
        fields = ['id']

class WeatherUserNameSerializer(async_serializers.ModelSerializer):
    class Meta:
        model = WeatherUser
        fields = ['name']

class WeatherUserSerializer(async_serializers.ModelSerializer):
    class Meta:
        model = WeatherUser
        fields = '__all__'

class WeatherUserCitySerializer(async_serializers.ModelSerializer):
    class Meta:
        model = WeatherUserCity
        fields = ['user_id','name', 'latitude', 'longitude']

class WeatherUserCityUpdateSerializer(async_serializers.ModelSerializer):
    class Meta:
        model = WeatherUserCity
        fields = ['name', 'temperature', 'wind_speed', 'surface_pressure']

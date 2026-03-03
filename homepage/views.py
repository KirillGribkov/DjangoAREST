from homepage.services.weather import get_weater, get_weater_date
from rest_framework.response import Response
from .models import City, WeatherUser, WeatherUserCity
from .serializers import *
from adrf.views import APIView
from adrf import viewsets
from asgiref.sync import sync_to_async

# Create your views here.
class Citys(APIView):
    async def get(self, request):
        items = City.objects.all()
        serializer = CityNameSerializer(items, many=True)
        return Response(await serializer.adata)

    async def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            await serializer.asave()
            return Response(await serializer.adata, status=201)
        return Response(serializer.errors, status=400)
 
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityUpdateSerializer

'''
example: (get) http://127.0.0.1:8000/apiurl/CitDayWeatherURL/?city=London&date_time=2026-01-21T00:00&parameters=temperature_2m
http://127.0.0.1:8000/apiurl/CitDayWeatherURL/?city={city}&date_time={date_time}&parameters={parameters}
parameters propisivautsya cherez zapytuyu example: "temperature_2m,wind_speed_10m,surface_pressure,precipitation"
answer:
{
    "temperature_2m": 8.5
}
'''
class CitDayWeatherURL(APIView):
    async def get(self, request):
        try:
            city_name = request.query_params.get("city")
            date_time = request.query_params.get("date_time")
            parameters = request.query_params.get("parameters")
            #parameters = ["temperature_2m","wind_speed_10m","surface_pressure","precipitation"]
            city = await City.objects.aget(name=city_name)
            weather_data = await get_weater_date([city.latitude,city.longitude],date_time,parameters)
            return Response(weather_data)
        except Exception:
                return Response(status=404)
        
'''
example: (get) http://127.0.0.1:8000/apiurl/CitDayWeatherURL/
body = {
    "city":"London",
    "date_time": "2026-01-21T00:00",
    "parameters":"temperature_2m,wind_speed_10m,surface_pressure,precipitation"
}
answer:
{
    "temperature_2m": 8.5,
    "wind_speed_10m": 16.7,
    "surface_pressure": 995.1,
    "precipitation": 1.2
}
'''
class CitDayWeather(APIView):
    async def get(self, request):
        try:
            #parameters = ["temperature_2m","wind_speed_10m","surface_pressure","precipitation"]
            city = await City.objects.aget(name=request.data["city"])
            weather_data = await get_weater_date([city.latitude,city.longitude],request.data["date_time"],request.data["parameters"])
            return Response(weather_data)
        except Exception:
                return Response(status=404)
    
'''
example: (get) http://127.0.0.1:8000/apiurl/CoordsWeatherURL/?latitude=50&longitude=50
http://127.0.0.1:8000/apiurl/CoordsWeatherURL/?latitude={latitude}&longitude={longitude}
answer:
{
    "temperature_2m": -6.5,
    "wind_speed_10m": 12.7,
    "surface_pressure": 1021.8
}
'''
class CoordsWeatherURL(APIView):
    async def get(self, request):
        try:
            latitude = request.query_params.get("latitude")
            longitude = request.query_params.get("longitude")
            return Response(await get_weater([latitude,longitude]))
        except Exception:
                return Response(status=404)
'''
example: (get) http://127.0.0.1:8000/api/CoordsWeather/
body = {
    "latitude": 50,
    "longitude":50
}
answer:
{
    "temperature_2m": -6.5,
    "wind_speed_10m": 12.7,
    "surface_pressure": 1021.8
}
'''
class CoordsWeather(APIView):
    async def get(self, request):
        try:
            return Response(await get_weater([request.data["latitude"],request.data["longitude"]]))
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/apiurl/CityAppendURL/?name=TestCity&latitude=50.0&longitude=50.0
http://127.0.0.1:8000/apiurl/CityAppendURL/?name={name}&latitude={latitude}&longitude={longitude}
answer:
{
    "name": "TestCity",
    "latitude": 50.0,
    "longitude": 50.0
}
sohraneniye v bd
'''    
class CityAppendURL(APIView):
    async def get(self, request):
        try:
            name = request.query_params.get("name")
            latitude = request.query_params.get("latitude")
            longitude = request.query_params.get("longitude")
            data={
                "name": name,
                "latitude": latitude,
                "longitude": longitude
            }
            serializer = CitySerializer(data=data)
            if serializer.is_valid():
                await serializer.asave()
                return Response(await serializer.adata, status=201)
            return Response(serializer.errors, status=400)
        except Exception:
                return Response(status=404)
'''
example: (get) http://127.0.0.1:8000/api/CoordsWeather/
body = {
    "name": "TestCity",
    "latitude": 50.0,
    "longitude": 50.0
}
answer:
{
    "name": "TestCity",
    "latitude": 50.0,
    "longitude": 50.0
}
sohraneniye v bd
'''
class CityAppend(APIView):
    async def get(self, request):
        try:
            serializer = CitySerializer(data=request.data)
            if serializer.is_valid():
                await serializer.asave()
                return Response(await serializer.adata, status=201)
            return Response(serializer.errors, status=400)
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/api/CityList/
answer like:
[
    "London",
    "\"Moscow\"",
    "Moscow",
    "Tomsk",
    "Tomsk",
    "Tomsk2",
    "Lob",
    "Lob1",
    "TestCity",
    "TestCity"
]
'''
class CityList(APIView): 
    async def get(self, request):
        try:
            cities = await sync_to_async(list)(City.objects.all())
            city_list = []
            for city in cities:
                city_list.append(city.name)
            return Response(city_list)
        except Exception:
            return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name=London
http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name={name}
answer like:{
    "name": "London",
    "temperature": 9.0,
    "wind_speed": 15.9,
    "surface_pressure": 988.8
}
doljno proyti 15 min s sozdanya goroda inache pogoda None
'''
class SavedCityWeatherURL(APIView):
    async def get(self, request):
        try:
            city_name = request.query_params.get("name")
            city = await City.objects.aget(name=city_name)
            serializer = CityUpdateSerializer(city)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/api/SavedCityWeather/
body={
    "name":"London"
}
answer like:{
    "name": "London",
    "temperature": 9.0,
    "wind_speed": 15.9,
    "surface_pressure": 988.8
}
doljno proyti 15 min s sozdanya goroda inache pogoda None
'''
class SavedCityWeather(APIView):
    async def get(self, request):
        try:
            city = await City.objects.aget(name=request.data["name"])
            serializer = CityUpdateSerializer(city)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)
        

'''
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserAppendURL/?name=TestUser
http://127.0.0.1:8000/apiurl/WeatherUserAppendURL/?name={name}
answer like:{
    "id": 11
}
id ispolzuetsya dalee dlya sobstvenih spiscow gorodow
'''        
class WeatherUserAppendURL(APIView):
    async def get(self, request):
        try:
            name = request.query_params.get("name")
            data={
                "name": name
            }
            serializer = WeatherUserSerializer(data=data)
            if serializer.is_valid():
                await serializer.asave()
                serializer = WeatherUserIdSerializer(await serializer.adata)
                return Response(await serializer.adata, status=201)
            return Response(serializer.errors, status=400)
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/api/WeatherUserAppend/
body={
    "name":"TestUser"
}
answer like:{
    "id": 11
}
'''
class WeatherUserAppend(APIView):
    async def get(self, request):
        try:
            serializer = WeatherUserSerializer(data=request.data)
            if serializer.is_valid():
                await serializer.asave()
                serializer = WeatherUserIdSerializer(await serializer.adata)
                return Response(await serializer.adata, status=201)
            return Response(serializer.errors, status=400)
        except Exception:
                return Response(status=404)

       
class WeatherUsers(APIView):
    async def get(self, request):
        try:
            items = WeatherUser.objects.all()
            serializer = WeatherUserSerializer(items, many=True)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)

    async def post(self, request):
        serializer = WeatherUserSerializer(data=request.data)
        if serializer.is_valid():
            await serializer.asave()
            return Response(await serializer.adata, status=201)
        return Response(serializer.errors, status=400)

    
class WeatherUserSet(viewsets.ModelViewSet):
    try:
        queryset = WeatherUser.objects.all()
        serializer_class = WeatherUserSerializer
    except Exception:
        pass


'''
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserCityAppendURL/?user_id=1&name=SPB&latitude=50&longitude=50
http://127.0.0.1:8000/apiurl/WeatherUserCityAppendURL/?user_id={user_id}&name={name}&latitude={latitude}&longitude={longitude}
answer like:{
    "user_id": 1,
    "name": "SPB",
    "latitude": 50.0,
    "longitude": 50.0
}
doljno proyti 15 min s sozdanya goroda inache pogoda None
'''
class WeatherUserCityAppendURL(APIView):
    async def get(self, request):
        try:
            data = {
                "user_id": request.query_params.get("user_id"),
                "name": request.query_params.get("name"),
                "latitude": request.query_params.get("latitude"),
                "longitude": request.query_params.get("longitude")
            }
            serializer = WeatherUserCitySerializer(data=data)
            is_valid = await sync_to_async(serializer.is_valid)()
            if is_valid:
                await sync_to_async(serializer.save)()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name=London
body={
    "user_id": 1,
    "name": "SPB2",
    "latitude": 50.0,
    "longitude": 50.0
}
answer like:{
    "user_id": 1,
    "name": "SPB2",
    "latitude": 50.0,
    "longitude": 50.0
}
doljno proyti 15 min s sozdanya goroda inache pogoda None
'''
class WeatherUserCityAppend(APIView):
    async def get(self, request):
        try:
            serializer = WeatherUserCitySerializer(data=request.data)
            is_valid = await sync_to_async(serializer.is_valid)()
            if is_valid:
                await sync_to_async(serializer.save)()
                return Response(await serializer.adata, status=201)
            return Response(serializer.errors, status=400)
        except Exception:
                return Response(status=404)



class WeatherUserCities(APIView):
    async def get(self, request):
        try:
            items = WeatherUserCity.objects.all()
            serializer = WeatherUserCitySerializer(items, many=True)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)

    async def post(self, request):
        serializer = WeatherUserCitySerializer(data=request.data)
        if serializer.is_valid():
            await serializer.asave()
            return Response(await serializer.adata, status=201)
        return Response(serializer.errors, status=400)

    
class WeatherUserCitySet(viewsets.ModelViewSet):
    try:
        queryset = WeatherUserCity.objects.all()
        serializer_class = WeatherUserCitySerializer
    except Exception:
        pass

'''
example: (get) http://127.0.0.1:8000/apiurl/SavedWeatherUserCityWeatherURL/?user_id=1&name=Tom
http://127.0.0.1:8000/apiurl/SavedWeatherUserCityWeatherURL/?user_id={user_id}&name={name}
answer like:{
    "name": "Tom",
    "temperature": -9.0,
    "wind_speed": 9.5,
    "surface_pressure": 1022.2
}
doljno proyti 15 min s sozdanya goroda inache pogoda None
'''
class SavedWeatherUserCityWeatherURL(APIView):
    async def get(self, request):
        try:
            user_id = request.query_params.get("user_id")
            city_name = request.query_params.get("name")
            city = await WeatherUserCity.objects.aget(user_id=user_id,name=city_name)
            serializer = WeatherUserCityUpdateSerializer(city)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name=London
body={
    "user_id": 1,
    "name": "Tom"
}
answer like:{
    "name": "Tom",
    "temperature": -9.0,
    "wind_speed": 9.5,
    "surface_pressure": 1022.2
}
doljno proyti 15 min s sozdanya goroda inache pogoda None
'''
class SavedWeatherUserCityWeather(APIView):
    async def get(self, request):
        try:
            city = await WeatherUserCity.objects.aget(user_id=request.data["user_id"],name=request.data["name"])
            serializer = WeatherUserCityUpdateSerializer(city)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserCitDayWeatherURL/?user_id=1&name=Tom&date_time=2026-01-19T00:00&parameters=temperature_2m
http://127.0.0.1:8000/apiurl/WeatherUserCitDayWeatherURL/?user_id={user_id}&name=Tom&date_time={date_time}&parameters={parameters}
parameters propisivautsya cherez zapytuyu example: "temperature_2m,wind_speed_10m,surface_pressure,precipitation"
answer like:{
    "temperature_2m": -17.6
}

'''
class WeatherUserCitDayWeatherURL(APIView):#
    async def get(self, request):
        try:
            user_id = request.query_params.get("user_id")
            city_name = request.query_params.get("name")
            date_time = request.query_params.get("date_time")
            parameters = request.query_params.get("parameters")
            #parameters = ["temperature_2m","wind_speed_10m","surface_pressure","precipitation"]
            city = await WeatherUserCity.objects.aget(user_id=user_id,name=city_name)
            weather_data = await get_weater_date([city.latitude,city.longitude],date_time,parameters)
            return Response(weather_data)
        except Exception:
                return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/api/WeatherUserCitDayWeather/
body={
    "user_id": 1,
    "name": "Tom",
    "date_time": "2026-01-19T00:00",
    "parameters": "precipitation,surface_pressure"
}
answer like:{
    "precipitation": 0.0,
    "surface_pressure": 1039.9
}
parameters propisivautsya cherez zapytuyu example: "temperature_2m,wind_speed_10m,surface_pressure,precipitation"
'''
class WeatherUserCitDayWeather(APIView):
    async def get(self, request):
        try:
            #parameters = ["temperature_2m","wind_speed_10m","surface_pressure","precipitation"]
            city = await WeatherUserCity.objects.aget(user_id=request.data["user_id"],name=request.data["name"])
            weather_data = await get_weater_date([city.latitude,city.longitude],request.data["date_time"],request.data["parameters"])
            return Response(weather_data)
        except Exception:
                return Response(status=404)


'''
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserCityListURL/?user_id=1
http://127.0.0.1:8000/apiurl/WeatherUserCityListURL/?user_id={user_id}

answer like:[
    "Tom",
    "1",
    "1",
    "tt",
    "3",
    "SPB",
    "SPB2"
]
'''
class WeatherUserCityListURL(APIView): 
    async def get(self, request):
        try:
            user_id = request.query_params.get("user_id")
            cities = await sync_to_async(list)(WeatherUserCity.objects.filter(user_id=user_id))
            city_list = []
            for city in cities:
                city_list.append(city.name)
            return Response(city_list)
        except Exception:
            return Response(status=404)

'''
example: (get) http://127.0.0.1:8000/api/WeatherUserCityList/
body={
    "user_id": 1
}
answer like:[
    "Tom",
    "1",
    "1",
    "tt",
    "3",
    "SPB",
    "SPB2"
]
'''
class WeatherUserCityList(APIView): 
    async def get(self, request):
        try:
            cities = await sync_to_async(list)(WeatherUserCity.objects.filter(user_id=request.data["user_id"]))
            city_list = []
            for city in cities:
                city_list.append(city.name)
            return Response(city_list)
        except Exception:
            return Response(status=404)
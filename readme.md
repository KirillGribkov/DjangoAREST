
# HTTP-сервер для предоставления информации по погоде с использованием асинхронного фреймворка.
## Контактная информация:
Если возьникнут вопросы или предложения  
# Почта:  
KirillGribkov2001@yandex.ru  
# Телефон:  
89050898833  
## Описание:
Это HTTP-сервер для предоставления информации по погоде с использованием асинхронного фреймворка(adrf и asinc.io).
Сервер реализован при помощи Django, База данных SQLite. Сервер работает на ASGIмодуле Uvicorn.
Сервер выполняет задачи указанные в ТЗ.
А именно:
1. Метод принимает координаты и возвращает данные о температуре, скорости ветра и атмосферном давлении на момент запроса.
2. Метод принимает название города и его координаты и добавляет в список городов, для которых отслеживается прогноз погоды. Сервер должен хранить прогноз погоды для указанных городов на текущий день и обновлять его каждые 15 минут.
3. Метод возвращает список городов, для которых доступен прогноз погоды.
4. Метод принимает название города и время и возвращает для него погоду на текущий день в указанное время. Должна быть возможность выбирать, какие параметры погоды получать в ответе — температура, влажность, скорость ветра, осадки.
Дополнительно:
5. Были реализованы методы выполняющие выше описаные методы, но с использованием юзера и его айди.
## Требования:
1. Python>=12
## Установка:
1. Скачать архив.
2. Разпаковать в любой дериктории где имеется разрешение на чтение и запись файлов.
3. Запустить script.py (Перейти в директорию с файлом и командой:python3 script.py или python script.py запустить скрипт)
Все необходимые библиотеки должны установиться самостоятельно из файла reqirements.txt  
4. Постадарту сервер идёт с базой данных, если необходима пустая база данных( 1 Удалить файд db.sqlite3 2 в командной строке в директории проекта прописать python manage.py makemigrations далее python manage.py migrate)   


Рекомендуется использовать Conda environment или Docker container.
## Использование:
1. Метод принимает координаты и возвращает данные о температуре, скорости ветра и атмосферном давлении на момент запроса.  
vid1:

example: http://127.0.0.1:8000/apiurl/CoordsWeatherURL/?latitude=50&longitude=50

http://127.0.0.1:8000/apiurl/CoordsWeatherURL/?latitude={latitude}&longitude={longitude}

Числа вводить через точку (5.1)  
answer:
```
{
    "temperature_2m": -6.5,
    "wind_speed_10m": 12.7,
    "surface_pressure": 1021.8
}  
```
class:
```
class CoordsWeatherURL(APIView):
    async def get(self, request):
        try:
            latitude = request.query_params.get("latitude")
            longitude = request.query_params.get("longitude")
            return Response(await get_weater([latitude,longitude]))
        except Exception:
                return Response(status=404)
```

vid2:  
example: (get) http://127.0.0.1:8000/api/CoordsWeather/  
body:
```
{
    "latitude": 50,
    "longitude":50
}
```
answer:
```
{
    "temperature_2m": -6.5,
    "wind_speed_10m": 12.7,
    "surface_pressure": 1021.8
}
```
class:
```
class CoordsWeather(APIView):
    async def get(self, request):
        try:
            return Response(await get_weater([request.data["latitude"],request.data["longitude"]]))
        except Exception:
                return Response(status=404)
```
path: homepage/views.py

2.1. Метод принимает название города и его координаты и добавляет в список городов, для которых отслеживается прогноз погоды.   

vid1:  
example: (get) http://127.0.0.1:8000/apiurl/CityAppendURL/?name=TestCity&latitude=50.0&longitude=50.0  

http://127.0.0.1:8000/apiurl/CityAppendURL/?name={name}&latitude={latitude}&longitude={longitude}  

answer:
```
{
    "name": "TestCity",
    "latitude": 50.0,
    "longitude": 50.0
}
```
Сохраняет в базу данных  
class:
```
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
```

vid2:  
example: (get) http://127.0.0.1:8000/api/CoordsWeather/
body: 
```
{
    "name": "TestCity",
    "latitude": 50.0,
    "longitude": 50.0
}
```
answer:
```
{
    "name": "TestCity",
    "latitude": 50.0,
    "longitude": 50.0
}
```
Сохраняет в базу данных
class:
```
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
```
path: homepage/views.py~

2.2 Сервер должен хранить прогноз погоды для указанных городов на текущий день и обновлять его каждые 15 минут.

Cтороний API для получения прогноз погоды а текущий день  
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude={a}&longitude={b}&daily=temperature_2m_mean,surface_pressure_mean,wind_speed_10m_mean&timezone=auto&forecast_days=1"  
Функция get_weater получает прогноз погоды для координат на текущий день.  
Функция update_city обновляет прогноз погоды для городов в базе данных городов на текущий день функцией get_weater каждые 15 минут.  
Функция update_city начинает работать со старта сервера.  
path: homepage/task.py  

get_weater:
```
async def get_weater(coords: list) -> dict[str, str]:
    url = WEATHER_API_URL.format(a=coords[0],b=coords[1])
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        data = {key: data["daily"][key] for key in ["temperature_2m_mean","surface_pressure_mean","wind_speed_10m_mean"]}
        return data

```
update_city:
```
async def update_city():
    while True:
        try:
            async for city in City.objects.all():
                data = await get_weater([city.latitude, city.longitude])
                city.temperature = data["temperature_2m_mean"][0]
                city.surface_pressure = data["surface_pressure_mean"][0]
                city.wind_speed = data["wind_speed_10m_mean"][0]
                await city.asave()
            async for city in WeatherUserCity.objects.all():
                data = await get_weater([city.latitude, city.longitude])
                city.temperature = data["temperature_2m_mean"][0]
                city.surface_pressure = data["surface_pressure_mean"][0]
                city.wind_speed = data["wind_speed_10m_mean"][0]
                await city.asave()
            await asyncio.sleep(900)
        except Exception:
            pass
```
Вход в бесконечный цикл:
```
class HomepageConfig(AppConfig):
    name = 'homepage'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            threading.Thread(target=self.start_async_loop, daemon=True).start()

    def start_async_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        from homepage.task import update_city
        loop.run_until_complete(update_city())
```
path: homepage/apps.py

3 Метод возвращает список городов, для которых доступен прогноз погоды.

vid1:  
example: (get) http://127.0.0.1:8000/api/CityList/  
answer like:  
```
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
```
class:
```
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
```
path: homepage/views.py

3 (Дополнительно были сделаны API для просмотра температуры города из списка)

Рекомендуется подождать 15 мин после создания города или перезапустить сервер. Иначе погода вернётся как None.  
vid1:  
example: (get) http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name=London  
http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name={name}  
answer like:
```
{
    "name": "London",
    "temperature": 9.0,
    "wind_speed": 15.9,
    "surface_pressure": 988.8
}
```
class:
```
class SavedCityWeatherURL(APIView):
    async def get(self, request):
        try:
            city_name = request.query_params.get("name")
            city = await City.objects.aget(name=city_name)
            serializer = CityUpdateSerializer(city)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)
```

Рекомендуется подождать 15 мин после создания города или перезапустить сервер. Иначе погода вернётся как None.  
vid2:  
example: (get) http://127.0.0.1:8000/api/SavedCityWeather/?name=London  
body: 
```
{
    "name":"London"
}
```
answer like:
```
{
    "name": "London",
    "temperature": 9.0,
    "wind_speed": 15.9,
    "surface_pressure": 988.8
}
```
class:
```
class SavedCityWeather(APIView):
    async def get(self, request):
        try:
            city = await City.objects.aget(name=request.data["name"])
            serializer = CityUpdateSerializer(city)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)
```
path: homepage/views.py

4 Метод принимает название города и время и возвращает для него погоду на текущий день в указанное время.  

vid1:  
example: (get) http://127.0.0.1:8000/apiurl/CitDayWeatherURL/?city=London&date_time=2026-01-21T00:00&parameters=temperature_2m  
http://127.0.0.1:8000/apiurl/CitDayWeatherURL/?city={city}&date_time={date_time}&parameters={parameters}  
answer:
```
{
    "temperature_2m": 8.5
}
```
Возможность выбирать, какие параметры погоды получать в ответе — температура, влажность, скорость ветра, осадки и тд, реализована полем parameters.  
parameters  это строка в неё вписываются необходимые парметры погоды через запятую без пробелов.  
parameters example: "temperature_2m,wind_speed_10m,surface_pressure,precipitation"  
class:
```
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
```

vid2:  
example: (get) http://127.0.0.1:8000/apiurl/CitDayWeatherURL/  
body:
```
{
    "city":"London",
    "date_time": "2026-01-21T00:00",
    "parameters":"temperature_2m,wind_speed_10m,surface_pressure,precipitation"
}
```
answer:
```
{
    "temperature_2m": 8.5,
    "wind_speed_10m": 16.7,
    "surface_pressure": 995.1,
    "precipitation": 1.2
}
```
Возможность выбирать, какие параметры погоды получать в ответе — температура, влажность, скорость ветра, осадки и тд, реализована полем parameters.  
parameters  это строка в неё вписываются необходимые парметры погоды через запятую без пробелов.  
parameters example: "temperature_2m,wind_speed_10m,surface_pressure,precipitation"  
class:
```
class CitDayWeather(APIView):
    async def get(self, request):
        try:
            #parameters = ["temperature_2m","wind_speed_10m","surface_pressure","precipitation"]
            city = await City.objects.aget(name=request.data["city"])
            weather_data = await get_weater_date([city.latitude,city.longitude],request.data["date_time"],request.data["parameters"])
            return Response(weather_data)
        except Exception:
                return Response(status=404)
```
path: homepage/views.py

Дополнительные задания:  
1. Добавить возможность работы с несколькими пользователями — реализовать метод регистрации
пользователя, который принимает имя пользователя и возвращает его ID.  

vid1:  
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserAppendURL/?name=TestUser  
http://127.0.0.1:8000/apiurl/WeatherUserAppendURL/?name={name}  
answer like:
```
{
    "id": 11
}
```
Возвращёный id используется для собственных списков городов.  
class:
```
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
```

vid2:  
example: (get) http://127.0.0.1:8000/api/WeatherUserAppend/  
body:
```
{
    "name":"TestUser"
}
```
answer like:
```
{
    "id": 11
}
```
Возвращёный id используется для собственных списков городов. 
class:
```
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
```
path: homepage/views.py

2.1 Метод принимает айди пользователя название города и его координаты и добавляет в список городов пользователя, для которых отслеживается прогноз погоды.  

vid1:  
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserCityAppendURL/?user_id=1&name=SPB&latitude=50&longitude=50  
http://127.0.0.1:8000/apiurl/WeatherUserCityAppendURL/?user_id={user_id}&name={name}&latitude={latitude}&longitude={longitude}  
answer like:
```
{
    "user_id": 1,
    "name": "SPB",
    "latitude": 50.0,
    "longitude": 50.0
}
```
Сохраняет в базу данных.  

class:
```
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
```

vid2:  
example: (get) http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name=London  
body:
```
{
    "user_id": 1,
    "name": "SPB2",
    "latitude": 50.0,
    "longitude": 50.0
}
```
answer like:
```
{
    "user_id": 1,
    "name": "SPB2",
    "latitude": 50.0,
    "longitude": 50.0
}
```
Сохраняет в базу данных.  
class:
```
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
```
path: homepage/views.py

2.2 Сервер должен хранить прогноз погоды для указанных городов пользователей на текущий день и обновлять его каждые 15 минут.  

Cтороний API для получения прогноз погоды на текущий день.  
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude={a}&longitude={b}&daily=temperature_2m_mean,surface_pressure_mean,wind_speed_10m_mean&timezone=auto&forecast_days=1"  
Функция get_weater получает прогноз погоды для координат на текущий день.  
Функция update_city обновляет прогноз погоды для городов в базе данных городов пользователей на текущий день функцией get_weater каждые 15 минут.  
Функция update_city начинает работать со старта сервера.  
path homepage/task.py  
get_weater:
```
async def get_weater(coords: list) -> dict[str, str]:
    url = WEATHER_API_URL.format(a=coords[0],b=coords[1])
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        data = {key: data["daily"][key] for key in ["temperature_2m_mean","surface_pressure_mean","wind_speed_10m_mean"]}
        return data
```
update_city:
```
async def update_city():
    while True:
        try:
            async for city in City.objects.all():
                data = await get_weater([city.latitude, city.longitude])
                city.temperature = data["temperature_2m_mean"][0]
                city.surface_pressure = data["surface_pressure_mean"][0]
                city.wind_speed = data["wind_speed_10m_mean"][0]
                await city.asave()
            async for city in WeatherUserCity.objects.all():
                data = await get_weater([city.latitude, city.longitude])
                city.temperature = data["temperature_2m_mean"][0]
                city.surface_pressure = data["surface_pressure_mean"][0]
                city.wind_speed = data["wind_speed_10m_mean"][0]
                await city.asave()
            await asyncio.sleep(900)
        except Exception:
            pass
```
Вход в бесконечный цикл:
```
    class HomepageConfig(AppConfig):
        name = 'homepage'

        def ready(self):
            if os.environ.get('RUN_MAIN') == 'true':
                threading.Thread(target=self.start_async_loop, daemon=True).start()

        def start_async_loop(self):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            from homepage.task import update_city
            loop.run_until_complete(update_city())
```
path: homepage/apps.py

3 Метод принимает айди пользователя и возвращает список городов пользователя, для которых доступен прогноз погоды.  

vid1:  
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserCityListURL/?user_id=1  
http://127.0.0.1:8000/apiurl/WeatherUserCityListURL/?user_id={user_id}  

answer like:
```
[
    "Tom",
    "1",
    "1",
    "tt",
    "3",
    "SPB",
    "SPB2"
]
```
class:
```
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
```
vid2:  
example: (get) http://127.0.0.1:8000/api/WeatherUserCityList/  
body:
```
{
    "user_id": 1
}
```
answer like:
```
[
    "Tom",
    "1",
    "1",
    "tt",
    "3",
    "SPB",
    "SPB2"
]
```
class:
```
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
```
path: homepage/views.py

3 (Дополнительно были сделаны API для просмотра температуры города из списка)  

Рекомендуется подождать 15 мин после создания города или перезапустить сервер. Иначе погода вернётся как None.  
vid1:  
example: (get) http://127.0.0.1:8000/apiurl/SavedWeatherUserCityWeatherURL/?user_id=1&name=Tom  
http://127.0.0.1:8000/apiurl/SavedWeatherUserCityWeatherURL/?user_id={user_id}&name={name}  
answer like:
```
{
    "name": "Tom",
    "temperature": -9.0,
    "wind_speed": 9.5,
    "surface_pressure": 1022.2
}
```
class:
```
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
```

Рекомендуется подождать 15 мин после создания города или перезапустить сервер. Иначе погода вернётся как None.  
vid2:  
example: (get) http://127.0.0.1:8000/apiurl/SavedCityWeatherURL/?name=London  
body:
```
{
    "user_id": 1,
    "name": "Tom"
}
```
answer like:
```
{
    "name": "Tom",
    "temperature": -9.0,
    "wind_speed": 9.5,
    "surface_pressure": 1022.2
}
```
class:
```
class SavedWeatherUserCityWeather(APIView):
    async def get(self, request):
        try:
            city = await WeatherUserCity.objects.aget(user_id=request.data["user_id"],name=request.data["name"])
            serializer = WeatherUserCityUpdateSerializer(city)
            return Response(await serializer.adata)
        except Exception:
                return Response(status=404)
```
path: homepage/views.py

4 Метод принимает айди пользователя, название города и время и возвращает для него погоду на текущий день в указанное время.  

vid1:  
example: (get) http://127.0.0.1:8000/apiurl/WeatherUserCitDayWeatherURL/?user_id=1&name=Tom&date_time=2026-01-19T00:00&parameters=temperature_2m  
http://127.0.0.1:8000/apiurl/WeatherUserCitDayWeatherURL/?user_id={user_id}&name=Tom&date_time={date_time}&parameters={parameters}  
answer like:
```
{
    "temperature_2m": -17.6
}
```
Возможность выбирать, какие параметры погоды получать в ответе — температура, влажность, скорость ветра, осадки и тд, реализована полем parameters  
parameters  это строка в неё вписываются необходимые парметры погоды через запятую без пробелов.  
parameters example: "temperature_2m,wind_speed_10m,surface_pressure,precipitation"  
class:
```
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
```

vid2:  
example: (get) http://127.0.0.1:8000/api/WeatherUserCitDayWeather/  
body:
```
{
    "user_id": 1,
    "name": "Tom",
    "date_time": "2026-01-19T00:00",
    "parameters": "precipitation,surface_pressure"
}
```
answer like:
```
{
    "precipitation": 0.0,
    "surface_pressure": 1039.9
}
```
Возможность выбирать, какие параметры погоды получать в ответе — температура, влажность, скорость ветра, осадки и тд, реализована полем parameters  
parameters  это строка в неё вписываются необходимые парметры погоды через запятую без пробелов.  
parameters example: "temperature_2m,wind_speed_10m,surface_pressure,precipitation"  
class:
```
class WeatherUserCitDayWeather(APIView):
    async def get(self, request):
        try:
            #parameters = ["temperature_2m","wind_speed_10m","surface_pressure","precipitation"]
            city = await WeatherUserCity.objects.aget(user_id=request.data["user_id"],name=request.data["name"])
            weather_data = await get_weater_date([city.latitude,city.longitude],request.data["date_time"],request.data["parameters"])
            return Response(weather_data)
        except Exception:
                return Response(status=404)
```
path: homepage/views.py

Дополнительно:  
Были сделаны функции для просмотра списков созданых городов юзеров и городов юзеров.
1 Функции для просмотра списков созданых городов  

Все города:  
    http://127.0.0.1:8000/api/city/  
Город по айди:  
    http://127.0.0.1:8000/api/city/3/  
class:
```
    class CityViewSet(viewsets.ModelViewSet):
        queryset = City.objects.all()
        serializer_class = CityUpdateSerializer
```
path: homepage/views.py

Все города списком:  
    http://127.0.0.1:8000/api/citys/  

class:
```
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
```
path: homepage/views.py

2 Функции для просмотра списков юзеров:  

Все юзеры:  
    http://127.0.0.1:8000/api/WeatherUser/  
Юер по айди:  
    http://127.0.0.1:8000/api/WeatherUser/3/  
class:
```
    class CityViewSet(viewsets.ModelViewSet):
        queryset = City.objects.all()
        serializer_class = CityUpdateSerializer
```
path: homepage/views.py

Все юзеры списком:  
    http://127.0.0.1:8000/api/WeatherUsers/  

class:
```
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
```
path: homepage/views.py

3 Функции для просмотра списков созданых городов юзеров  

Все города юзеров:  
    http://127.0.0.1:8000/api/city/  
Город юзеров по айди:  
    http://127.0.0.1:8000/api/city/3/  
class:
```
    class WeatherUserCitySet(viewsets.ModelViewSet):
        try:
            queryset = WeatherUserCity.objects.all()
            serializer_class = WeatherUserCitySerializer
        except Exception:
            pass
```
path: homepage/views.py

Все города юзеров списком:  
    http://127.0.0.1:8000/api/citys/  

class:
```
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
```
path: homepage/views.py

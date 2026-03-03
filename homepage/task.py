import httpx
from homepage.models import City, WeatherUserCity
import asyncio






WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude={a}&longitude={b}&daily=temperature_2m_mean,surface_pressure_mean,wind_speed_10m_mean&timezone=auto&forecast_days=1"

async def get_weater(coords: list) -> dict[str, str]:
    url = WEATHER_API_URL.format(a=coords[0],b=coords[1])
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        data = {key: data["daily"][key] for key in ["temperature_2m_mean","surface_pressure_mean","wind_speed_10m_mean"]}
        return data

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


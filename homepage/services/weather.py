import httpx

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude={a}&longitude={b}&current=temperature_2m,wind_speed_10m,surface_pressure"

async def get_weater(coords: list) -> dict[str, str]:
    url = WEATHER_API_URL.format(a=coords[0],b=coords[1])
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        data = {key: data["current"][key] for key in ["temperature_2m","wind_speed_10m","surface_pressure"]}
        return data

WEATHERD_API_URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone=auto&start_date={date}&end_date={date}&hourly={parameters}"

async def get_weater_date(coords: list,dates: str,parameters: str) -> dict[str, str]:
    dates=dates.split('T')
    dated=dates[0]
    datet=dates[1]
    datet=datet.split(":")
    if int(datet[1])>=30 and int(datet[0])==23:
        datet[0]="23"
        datet[1]="00"
    elif int(datet[1])>=30:
        datet[1]="00"
        datet[0]="0"+str(int(datet[0])+1)
    else:
        datet[1]="00"
    time=dated+'T'+datet[0]+':'+datet[1]
    if parameters:
        url = WEATHERD_API_URL.format(latitude=coords[0],longitude=coords[1],date=dated,parameters=parameters)
    else:
        url = WEATHERD_API_URL.format(latitude=coords[0],longitude=coords[1],date=dated,parameters='')
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if parameters:
            parameters = parameters.split(',')
            parameters.append("time")
            data = {key: data["hourly"][key] for key in parameters}
            a=0
            for i in range(len(data["time"])):
                if data["time"][i]==time:
                    a=i
            parameters.pop()
            end_data={key: data[key][a] for key in parameters}
            return end_data
        else:
            parameters=[]
            parameters.append("time")
            data = {key: data["hourly"][key] for key in parameters}
            a=0
            for i in range(len(data["time"])):
                if data["time"][i]==time:
                    a=i
            parameters.pop()        
            end_data={key: data[key][a] for key in parameters}
            return end_data


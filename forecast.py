import os
import requests
import datetime
import pytz

base_url = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

location = input("Enter a location: ")
query_params = {
    "q": location,
    "appid": api_key,
    "units": "metric"
}

try:
    response = requests.get(base_url, params=query_params)
    response.raise_for_status()
    data = response.json()

    # Get the timezone offset from UTC for the location
    timezone_offset = data["city"]["timezone"]
    timezone = pytz.timezone(pytz.country_timezones(data["city"]["country"])[0])

    forecast = {}
    for forecast_data in data["list"]:
        timestamp = forecast_data["dt"]
        # Add the timezone offset to the Unix timestamp to convert to UTC time
        utc_time = datetime.utcfromtimestamp(timestamp) + datetime.timedelta(seconds=timezone_offset)
        # Convert to the local timezone
        local_time = timezone.localize(utc_time).astimezone(timezone)

        hour = local_time.strftime("%H:%M")
        day = local_time.strftime("%a")

        temperature = forecast_data["main"]["temp"]
        description = forecast_data["weather"][0]["description"]
        wind_speed = forecast_data["wind"]["speed"]

        if day not in forecast:
            forecast[day] = []

        forecast[day].append({
            "hour": hour,
            "temperature": temperature,
            "description": description,
            "wind_speed": wind_speed
        })

    for day, forecasts in forecast.items():
        print(day)
        for f in forecasts:
            print(f"{f['hour']}: {f['temperature']}°C, {f['description']}, {f['wind_speed']} m/s")
        print()

except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")

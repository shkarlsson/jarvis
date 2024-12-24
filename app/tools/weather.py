# %%
import requests
from app.helpers.env_vars import OPEN_WEATHER_API_KEY, WEATHER_LOCATION
import json

# %%


def get_current_weather():
    current_weather_base_url = "http://api.openweathermap.org/data/2.5/weather"
    # Parameters for current weather
    params = {"q": WEATHER_LOCATION, "appid": OPEN_WEATHER_API_KEY, "units": "metric"}

    response = requests.get(current_weather_base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "description": data["weather"][0]["description"],
            "temperature": f"{data['main']['temp']} °C",
            "feels_like": f"{data['main']['feels_like']} °C",
            "temp_min": f"{data['main']['temp_min']} °C",
            "temp_max": f"{data['main']['temp_max']} °C",
            "humidity": f"{data['main']['humidity']} %",
            "wind_speed": f"{data['wind']['speed']} m/s",
            "rain": f"{data.get('rain', {}).get('1h', 0)} mm",
            "snow": f"{data.get('snow', {}).get('1h', 0)} mm",
            "thunderstorm": "thunderstorm" in data["weather"][0]["description"].lower(),
        }
        return weather_info
    else:
        return {
            "error": f"Failed to get current weather data. Error code: {response.status_code}"
        }


def get_forecast_weather(days=1):
    forecast_base_url = "http://api.openweathermap.org/data/2.5/forecast"

    # Parameters for forecast weather
    params = {
        "q": WEATHER_LOCATION,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric",
        "cnt": days * 8,  # 8 data points per day (every 3 hours)
    }

    response = requests.get(forecast_base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        forecasts = []
        for item in data["list"][: days * 8]:
            forecast_info = {
                "datetime": item["dt_txt"],
                "description": item["weather"][0]["description"],
                "temperature": f"{item['main']['temp']} °C",
                "feels_like": f"{item['main']['feels_like']} °C",
                "temp_min": f"{item['main']['temp_min']} °C",
                "temp_max": f"{item['main']['temp_max']} °C",
                "humidity": f"{item['main']['humidity']} %",
                "wind_speed": f"{item['wind']['speed']} m/s",
                "rain": f"{item.get('rain', {}).get('3h', 0)} mm",
                "snow": f"{item.get('snow', {}).get('3h', 0)} mm",
                "thunderstorm": "thunderstorm"
                in item["weather"][0]["description"].lower(),
            }
            forecasts.append(forecast_info)

        return forecasts
    else:
        return {
            "error": f"Failed to get forecast data. Error code: {response.status_code}"
        }


def get_weather(n):
    """Returns the weather data for the current location. If n is 0, it returns the current weather. Otherwise, it returns the forecast for n days ahead."""
    if n == 0:
        return get_current_weather()

    else:
        return get_forecast_weather(n)


def test_weather_tool():
    try:
        current_weather = get_weather(0)
        if "error" in current_weather:
            print("Error getting current weather")
            return False

        forecast_weather = get_weather(1)
        if "error" in forecast_weather:
            print("Error getting forecast weather")
            return False

        return True
    except Exception as e:
        print(f"Error testing weather tool: {e}")
        return False


# %%

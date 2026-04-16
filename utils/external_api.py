import requests

def get_weather_info():
    """Vienkāršs piemērs datu iegūšanai no Open-Meteo API."""
    try:
        res = requests.get(
            "[api.open-meteo.com](https://api.open-meteo.com/v1/forecast?latitude=56.97&longitude=21.97&current=temperature_2m)"
        )
        return res.json()["current"]["temperature_2m"]
    except Exception:
        return "N/A"

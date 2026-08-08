from flask import Blueprint, request, jsonify
import requests
from app import AppConfig

weather_bp = Blueprint("weather", __name__)
OPENWEATHER_API_KEY = AppConfig.OPENWEATHER_API_KEY

@weather_bp.route("/", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    state = request.args.get("state")
    country = "US"

    if not OPENWEATHER_API_KEY:
        return jsonify({"error": "API Key is missing!"}), 500
    if not city:
        return jsonify({"error": "Please provide a city name."}), 400

    try:
        # 1. Get city coordinates
        if state:
            query = f"{city},{state},{country}"
        else:
            query = f"{city},{country}"

        coord_url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={OPENWEATHER_API_KEY}&units=imperial"
        coord_res = requests.get(coord_url).json()

        if "coord" not in coord_res:
            return jsonify({"error": "City not found."}), 404

        lat = coord_res["coord"]["lat"]
        lon = coord_res["coord"]["lon"]
        city_name = coord_res["name"]

        # 2. Use One Call API to get daily forecast
        one_call_url = (
            f"https://api.openweathermap.org/data/3.0/onecall?"
            f"lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=imperial&appid={OPENWEATHER_API_KEY}"
        )
        forecast_data = requests.get(one_call_url).json()

        current = forecast_data["current"]
        today = forecast_data["daily"][0]

        weather_info = {
            "city": city_name,
            "temperature": current["temp"],
            "temp_min": today["temp"]["min"],
            "temp_max": today["temp"]["max"],
            "humidity": current["humidity"],
            "weather": current["weather"][0]["description"],
            "icon": current["weather"][0]["icon"]
        }

        return jsonify(weather_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

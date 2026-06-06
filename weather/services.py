import requests

class WeatherService:
    """
    Handles communications with Open-Meteo API for geocoding locations
    and getting precipitation forecasts.
    """
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    @classmethod
    def get_coordinates(cls, location_name):
        """
        Translates a location name into latitude, longitude, and formatted name.
        """
        params = {
            "name": location_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        try:
            response = requests.get(cls.GEO_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get("results")
            if results and len(results) > 0:
                loc = results[0]
                country_suffix = f", {loc['country']}" if "country" in loc else ""
                return {
                    "latitude": loc["latitude"],
                    "longitude": loc["longitude"],
                    "name": f"{loc['name']}{country_suffix}",
                }
        except Exception:
            pass
        return None

    @classmethod
    def get_rain_prediction(cls, latitude, longitude, start_date, end_date):
        """
        Fetches daily rain / precipitation predictions for the given coordinates and date range.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "precipitation_sum,precipitation_probability_max",
            "timezone": "auto"
        }
        try:
            response = requests.get(cls.FORECAST_URL, params=params, timeout=10)
            if response.status_code == 400:
                # Provide a friendly message for date out of bounds
                return {
                    "success": False,
                    "error": "Dates must be within the weather forecast window (from today up to 16 days in the future)."
                }
            response.raise_for_status()
            data = response.json()
            daily = data.get("daily", {})
            
            precipitation_sums = daily.get("precipitation_sum", [])
            probability_maxes = daily.get("precipitation_probability_max", [])

            # Aggregate precipitation sum and find max probability of rain
            total_rain = sum(p for p in precipitation_sums if p is not None) if precipitation_sums else 0.0
            max_prob = max(p for p in probability_maxes if p is not None) if probability_maxes else 0.0
            is_rainy = total_rain > 0.5 or max_prob > 35.0  # Thresholds for predicting rain

            return {
                "success": True,
                "total_rain": round(total_rain, 2),
                "max_probability": round(max_prob, 2),
                "is_rainy": is_rainy,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to retrieve weather data: {str(e)}"
            }

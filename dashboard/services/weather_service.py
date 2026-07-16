import json
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import ssl
from decouple import config
from datetime import datetime, timezone as tz

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE


def _get(url, params, timeout=8):
    full_url = f"{url}?{urlencode(params)}"
    try:
        with urlopen(full_url, timeout=timeout, context=_SSL_CTX) as resp:
            return json.loads(resp.read())
    except Exception:
        raise


class OpenWeatherService:
    BASE = "https://api.openweathermap.org/data/2.5"

    def __init__(self):
        self.key = config("OPENWEATHER_API_KEY", default=None)
        if not self.key:
            raise RuntimeError("OPENWEATHER_API_KEY is not configured")

    def _p(self, lat, lon, extra=None):
        p = {"lat": lat, "lon": lon, "appid": self.key, "units": "metric"}
        if extra:
            p.update(extra)
        return p

    def current_conditions(self, lat, lon):
        d = _get(f"{self.BASE}/weather", self._p(lat, lon))
        main    = d.get("main", {})
        wind    = d.get("wind", {})
        sys     = d.get("sys", {})
        weather = (d.get("weather") or [{}])[0]
        rain    = d.get("rain", {})
        snow    = d.get("snow", {})
        sunrise = sys.get("sunrise")
        sunset  = sys.get("sunset")
        sun_hours = round((sunset - sunrise) / 3600, 1) if sunrise and sunset else None

        uv = None
        try:
            uv = _get(f"{self.BASE}/uvi", self._p(lat, lon), timeout=4).get("value")
        except Exception:
            pass

        aqi_label = None
        try:
            aqi = _get(f"{self.BASE}/air_pollution", self._p(lat, lon), timeout=4)
            aqi_val = aqi.get("list", [{}])[0].get("main", {}).get("aqi")
            aqi_label = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}.get(aqi_val)
        except Exception:
            pass

        return {
            "temperature":    main.get("temp"),
            "feels_like":     main.get("feels_like"),
            "temp_min":       main.get("temp_min"),
            "temp_max":       main.get("temp_max"),
            "humidity":       main.get("humidity"),
            "pressure":       main.get("pressure"),
            "visibility":     round(d.get("visibility", 0) / 1000, 1),
            "wind_speed":     wind.get("speed"),
            "wind_direction": wind.get("deg"),
            "wind_gust":      wind.get("gust"),
            "phrase":         weather.get("description", "").title(),
            "icon_code":      weather.get("icon"),
            "icon_url":       f"https://openweathermap.org/img/wn/{weather.get('icon','01d')}@2x.png",
            "clouds":         d.get("clouds", {}).get("all"),
            "rainfall_1h":    rain.get("1h"),
            "rainfall_3h":    rain.get("3h"),
            "snowfall_1h":    snow.get("1h"),
            "sunrise":        datetime.fromtimestamp(sunrise, tz.utc).strftime("%H:%M") if sunrise else None,
            "sunset":         datetime.fromtimestamp(sunset,  tz.utc).strftime("%H:%M") if sunset  else None,
            "sun_hours":      sun_hours,
            "uv_index":       uv,
            "aqi":            aqi_label,
        }

    def forecast_daily(self, lat, lon):
        d = _get(f"{self.BASE}/forecast", self._p(lat, lon, {"cnt": 40}))
        seen, days = set(), []
        for item in d.get("list", []):
            date = item["dt_txt"][:10]
            if date in seen:
                continue
            seen.add(date)
            w = (item.get("weather") or [{}])[0]
            days.append({
                "date":                    date,
                "min_temp":                item["main"].get("temp_min"),
                "max_temp":                item["main"].get("temp_max"),
                "phrase":                  w.get("description", "").title(),
                "icon_url":                f"https://openweathermap.org/img/wn/{w.get('icon','01d')}@2x.png",
                "precipitation_probability": round((item.get("pop") or 0) * 100),
                "rainfall_3h":             item.get("rain", {}).get("3h"),
                "humidity":                item["main"].get("humidity"),
            })
            if len(days) == 5:
                break
        return days

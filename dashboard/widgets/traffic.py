import json
import ssl
from urllib.request import urlopen
from urllib.parse import urlencode
from django.shortcuts import render
from django.core.cache import cache
from decouple import config
from datetime import datetime

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# Most densely populated areas / major traffic corridors in Nigeria
NIGERIA_AREAS = {
    # Lagos — most congested city in Africa
    "lagos_island":      {"name": "Lagos — Lagos Island",        "lat":  6.4541, "lon":  3.3947},
    "lagos_victoria":    {"name": "Lagos — Victoria Island",     "lat":  6.4281, "lon":  3.4219},
    "lagos_lekki":       {"name": "Lagos — Lekki",               "lat":  6.4698, "lon":  3.5852},
    "lagos_ikeja":       {"name": "Lagos — Ikeja (Airport Rd)",  "lat":  6.6018, "lon":  3.3515},
    "lagos_oshodi":      {"name": "Lagos — Oshodi",              "lat":  6.5567, "lon":  3.3500},
    "lagos_apapa":       {"name": "Lagos — Apapa (Port)",        "lat":  6.4500, "lon":  3.3667},
    "lagos_surulere":    {"name": "Lagos — Surulere",            "lat":  6.5000, "lon":  3.3500},
    "lagos_ikorodu":     {"name": "Lagos — Ikorodu",             "lat":  6.6194, "lon":  3.5064},
    # Abuja
    "abuja_center":      {"name": "Abuja — City Centre",         "lat":  9.0579, "lon":  7.4951},
    "abuja_airport":     {"name": "Abuja — Airport Road",        "lat":  9.0067, "lon":  7.2631},
    "abuja_wuse":        {"name": "Abuja — Wuse",                "lat":  9.0667, "lon":  7.4833},
    "abuja_maitama":     {"name": "Abuja — Maitama",             "lat":  9.0833, "lon":  7.5000},
    # Kano
    "kano_center":       {"name": "Kano — City Centre",          "lat": 12.0022, "lon":  8.5920},
    "kano_sabon_gari":   {"name": "Kano — Sabon Gari",           "lat": 12.0167, "lon":  8.5333},
    # Ibadan
    "ibadan_center":     {"name": "Ibadan — City Centre",        "lat":  7.3775, "lon":  3.9470},
    "ibadan_challenge":  {"name": "Ibadan — Challenge",          "lat":  7.3833, "lon":  3.9167},
    # Port Harcourt
    "ph_center":         {"name": "Port Harcourt — Centre",      "lat":  4.8156, "lon":  7.0498},
    "ph_rumuola":        {"name": "Port Harcourt — Rumuola",     "lat":  4.8500, "lon":  7.0167},
    "ph_trans_amadi":    {"name": "Port Harcourt — Trans Amadi", "lat":  4.8333, "lon":  7.0333},
    # Benin City
    "benin_center":      {"name": "Benin City — Centre",         "lat":  6.3350, "lon":  5.6270},
    "benin_ring_road":   {"name": "Benin City — Ring Road",      "lat":  6.3333, "lon":  5.6167},
    # Kaduna
    "kaduna_center":     {"name": "Kaduna — City Centre",        "lat": 10.5222, "lon":  7.4383},
    # Enugu
    "enugu_center":      {"name": "Enugu — City Centre",         "lat":  6.4584, "lon":  7.5464},
    # Onitsha (busiest market in Africa)
    "onitsha":           {"name": "Onitsha (Anambra)",           "lat":  6.1667, "lon":  6.7833},
    # Aba
    "aba":               {"name": "Aba (Abia)",                  "lat":  5.1167, "lon":  7.3667},
    # Warri
    "warri":             {"name": "Warri (Delta)",               "lat":  5.5167, "lon":  5.7500},
    # Maiduguri
    "maiduguri":         {"name": "Maiduguri (Borno)",           "lat": 11.8333, "lon": 13.1500},
    # Ilorin
    "ilorin":            {"name": "Ilorin (Kwara)",              "lat":  8.4966, "lon":  4.5426},
    # Jos
    "jos":               {"name": "Jos (Plateau)",               "lat":  9.8965, "lon":  8.8583},
    # Abeokuta
    "abeokuta":          {"name": "Abeokuta (Ogun)",             "lat":  7.1557, "lon":  3.3451},
    # Owerri
    "owerri":            {"name": "Owerri (Imo)",                "lat":  5.4836, "lon":  7.0333},
    # Calabar
    "calabar":           {"name": "Calabar (Cross River)",       "lat":  4.9517, "lon":  8.3220},
    # Sokoto
    "sokoto":            {"name": "Sokoto",                      "lat": 13.0059, "lon":  5.2476},
    # Zaria
    "zaria":             {"name": "Zaria (Kaduna)",              "lat": 11.0855, "lon":  7.7199},
}

OWM_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"


def _weather_traffic_impact(weather_data):
    """Derive traffic impact from weather conditions."""
    weather_id = weather_data.get("id", 800)
    rain_1h    = weather_data.get("rain_1h", 0) or 0
    visibility = weather_data.get("visibility", 10)  # km
    wind_speed = weather_data.get("wind_speed", 0) or 0

    # OWM weather condition codes: 2xx=thunderstorm, 3xx=drizzle, 5xx=rain, 6xx=snow, 7xx=atmosphere, 800=clear
    if weather_id < 300:          # thunderstorm
        impact, color, label = 9, "red",    "Severe — Thunderstorm"
    elif weather_id < 400:        # drizzle
        impact, color, label = 4, "yellow", "Moderate — Drizzle"
    elif weather_id < 600:        # rain
        if rain_1h > 10:
            impact, color, label = 8, "red",    "Heavy — Heavy Rain"
        elif rain_1h > 2:
            impact, color, label = 6, "orange", "Heavy — Rain"
        else:
            impact, color, label = 4, "yellow", "Moderate — Light Rain"
    elif weather_id < 700:        # snow
        impact, color, label = 7, "orange", "Heavy — Snow/Hail"
    elif weather_id < 800:        # fog/mist/haze
        if visibility < 1:
            impact, color, label = 7, "orange", "Heavy — Dense Fog"
        else:
            impact, color, label = 3, "yellow", "Moderate — Haze/Mist"
    else:                         # clear/clouds
        if wind_speed > 15:
            impact, color, label = 3, "yellow", "Moderate — Strong Wind"
        else:
            impact, color, label = 1, "emerald", "Free Flow — Clear"

    return {
        "jam_factor":           impact,
        "jam_bar_width":        impact * 10,
        "congestion":           label,
        "congestion_color":     color,
        "weather_driven":       True,
    }


def traffic_widget(request):
    area_key = request.GET.get("area", "abuja_center")
    area = NIGERIA_AREAS.get(area_key, NIGERIA_AREAS["abuja_center"])
    lat, lon = area["lat"], area["lon"]
    owm_key = config("OPENWEATHER_API_KEY", default=None)

    context = {
        "flow": None, "incidents": [], "error": None,
        "areas": NIGERIA_AREAS,
        "selected_area": area_key,
        "area_name": area["name"],
    }

    if not owm_key:
        context["error"] = "OpenWeather API key not configured."
        return render(request, "dashboard/widgets/traffic_data.html", context)

    cache_key = f"traffic:{area_key}"
    cached = cache.get(cache_key)
    if cached:
        context["flow"] = cached
    else:
        try:
            params = urlencode({"lat": lat, "lon": lon, "appid": owm_key, "units": "metric"})
            with urlopen(f"{OWM_CURRENT_URL}?{params}", timeout=10, context=_SSL_CTX) as resp:
                d = json.loads(resp.read())
            main    = d.get("main", {})
            wind    = d.get("wind", {})
            weather = (d.get("weather") or [{}])[0]
            rain    = d.get("rain", {})
            vis_km  = round(d.get("visibility", 10000) / 1000, 1)
            impact = _weather_traffic_impact({
                "id":         weather.get("id", 800),
                "rain_1h":    rain.get("1h", 0),
                "visibility": vis_km,
                "wind_speed": wind.get("speed", 0),
            })
            flow = {
                **impact,
                "temperature":    main.get("temp"),
                "humidity":       main.get("humidity"),
                "wind_speed":     wind.get("speed"),
                "wind_direction": wind.get("deg"),
                "visibility_km":  vis_km,
                "weather_desc":   weather.get("description", "").title(),
                "weather_icon":   f"https://openweathermap.org/img/wn/{weather.get('icon','01d')}@2x.png",
                "rain_1h":        rain.get("1h"),
                "road_closure":   False,
                "updated_at":     datetime.now().strftime("%H:%M"),
            }
            cache.set(cache_key, flow, 600)
            context["flow"] = flow
        except Exception as e:
            context["error"] = str(e)

    return render(request, "dashboard/widgets/traffic_data.html", context)

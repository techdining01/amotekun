from django.shortcuts import render
from django.core.cache import cache
from dashboard.services.weather_service import OpenWeatherService

NIGERIA_CITIES = {
    "abuja":          {"name": "Abuja (FCT)",             "lat":  9.0579, "lon":  7.4951},
    "lagos":          {"name": "Lagos",                   "lat":  6.5244, "lon":  3.3792},
    "kano":           {"name": "Kano",                    "lat": 12.0022, "lon":  8.5920},
    "ibadan":         {"name": "Ibadan (Oyo)",            "lat":  7.3775, "lon":  3.9470},
    "port_harcourt":  {"name": "Port Harcourt (Rivers)",  "lat":  4.8156, "lon":  7.0498},
    "benin":          {"name": "Benin City (Edo)",        "lat":  6.3350, "lon":  5.6270},
    "kaduna":         {"name": "Kaduna",                  "lat": 10.5222, "lon":  7.4383},
    "enugu":          {"name": "Enugu",                   "lat":  6.4584, "lon":  7.5464},
    "jos":            {"name": "Jos (Plateau)",           "lat":  9.8965, "lon":  8.8583},
    "maiduguri":      {"name": "Maiduguri (Borno)",       "lat": 11.8333, "lon": 13.1500},
    "owerri":         {"name": "Owerri (Imo)",            "lat":  5.4836, "lon":  7.0333},
    "abeokuta":       {"name": "Abeokuta (Ogun)",         "lat":  7.1557, "lon":  3.3451},
    "akure":          {"name": "Akure (Ondo)",            "lat":  7.2526, "lon":  5.1932},
    "asaba":          {"name": "Asaba (Delta)",           "lat":  6.1986, "lon":  6.7356},
    "awka":           {"name": "Awka (Anambra)",          "lat":  6.2104, "lon":  7.0739},
    "bauchi":         {"name": "Bauchi",                  "lat": 10.3158, "lon":  9.8442},
    "birnin_kebbi":   {"name": "Birnin Kebbi (Kebbi)",    "lat": 12.4539, "lon":  4.1975},
    "calabar":        {"name": "Calabar (Cross River)",   "lat":  4.9517, "lon":  8.3220},
    "damaturu":       {"name": "Damaturu (Yobe)",         "lat": 11.7469, "lon": 11.9606},
    "dutse":          {"name": "Dutse (Jigawa)",          "lat": 11.6667, "lon":  9.3333},
    "ado_ekiti":      {"name": "Ado-Ekiti (Ekiti)",       "lat":  7.6211, "lon":  5.2213},
    "gombe":          {"name": "Gombe",                   "lat": 10.2791, "lon": 11.1670},
    "gusau":          {"name": "Gusau (Zamfara)",         "lat": 12.1704, "lon":  6.6640},
    "ilorin":         {"name": "Ilorin (Kwara)",          "lat":  8.4966, "lon":  4.5426},
    "jalingo":        {"name": "Jalingo (Taraba)",        "lat":  8.8937, "lon": 11.3730},
    "lafia":          {"name": "Lafia (Nasarawa)",        "lat":  8.4930, "lon":  8.5220},
    "lokoja":         {"name": "Lokoja (Kogi)",           "lat":  7.8036, "lon":  6.7333},
    "minna":          {"name": "Minna (Niger)",           "lat":  9.6139, "lon":  6.5569},
    "makurdi":        {"name": "Makurdi (Benue)",         "lat":  7.7337, "lon":  8.5212},
    "osogbo":         {"name": "Osogbo (Osun)",           "lat":  7.7719, "lon":  4.5624},
    "sokoto":         {"name": "Sokoto",                  "lat": 13.0059, "lon":  5.2476},
    "umuahia":        {"name": "Umuahia (Abia)",          "lat":  5.5320, "lon":  7.4860},
    "uyo":            {"name": "Uyo (Akwa Ibom)",         "lat":  5.0377, "lon":  7.9128},
    "warri":          {"name": "Warri (Delta)",           "lat":  5.5167, "lon":  5.7500},
    "yenagoa":        {"name": "Yenagoa (Bayelsa)",       "lat":  4.9267, "lon":  6.2676},
    "yola":           {"name": "Yola (Adamawa)",          "lat":  9.2035, "lon": 12.4954},
    "zaria":          {"name": "Zaria (Kaduna)",          "lat": 11.0855, "lon":  7.7199},
}


def weather_widget(request):
    city_key = request.GET.get("city", "abuja")
    city = NIGERIA_CITIES.get(city_key, NIGERIA_CITIES["abuja"])
    lat, lon = city["lat"], city["lon"]

    context = {
        "current": None, "forecast": [],
        "error": None,
        "cities": NIGERIA_CITIES,
        "selected_city": city_key,
        "city_name": city["name"],
    }

    cache_key = f"weather:{city_key}"
    cached = cache.get(cache_key)
    if cached:
        context["current"]  = cached["current"]
        context["forecast"] = cached["forecast"]
    else:
        try:
            svc = OpenWeatherService()
            context["current"]  = svc.current_conditions(lat, lon)
            context["forecast"] = svc.forecast_daily(lat, lon)
            cache.set(cache_key, {"current": context["current"], "forecast": context["forecast"]}, 600)
        except Exception as e:
            context["error"] = str(e)

    return render(request, "dashboard/widgets/weather_data.html", context)

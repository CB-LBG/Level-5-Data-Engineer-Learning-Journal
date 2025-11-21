import pandas as pd

EDINBURGH_PATH = "data/Edinburgh-daytime.xlsx"
STRATHSPEY_PATH = "data/Strathspey-weather.xlsx"

EDINBURGH_COLUMNS = {
    'date':pd.Timestamp,
    'sunrise': str,
    'sunset': str,
    'daylength': str,
    'day_length_diff': str,
    'astro_twilight_start': str,
    'astro_twilight_end': str,
    'nautical_twilight_start': str,
    'nautical_twilight_end': str,
    'civil_twilight_start': str,
    'civil_twilight_end': str,
    'solar_noon_time': str,
    'solar_noon_distance':float
}

STRATHSPEY_COLUMNS = {
    'date':pd.Timestamp,
    'temp_mean': str,
    'temp_min': str,
    'temp_max': str,
    'rain_mm': str,
    'pressure_early': int,
    'pressure_late': int,
    'wind_mean':float,
    'wind_max':float,
    'wind_dir':str,
    'sun_hours': float
}

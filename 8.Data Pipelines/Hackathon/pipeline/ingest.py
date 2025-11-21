import pandas as pd
import numpy as np
from pipeline import utils

def interpolate_day(date, temp_mean, min_temp, max_temp, solar_noon_time):
    # Generate time points for 1 day at 1-min intervals
    times = pd.date_range(start=date, periods=1440, freq="min")
    temp_mean = float(temp_mean)
    max_temp = float(max_temp)
    min_temp = float(min_temp)

    # Build a sinusoidal pattern
    minutes = np.arange(1440)
    t_peak = utils.get_mins_from_time(solar_noon_time) + 120

    # Example model: daily sinusoidal curve (simplified)
    temps = temp_mean + (max_temp - min_temp) / 2 * np.sin((minutes - t_peak) * np.pi / 720)

    df = pd.DataFrame({"datetime": times, "estimated_temp": temps})
    df['estimated_temp'] = round(df['estimated_temp'], 3)
    return df

def generate_minute_estimates(final_df):
    all_days = []
    for _, row in final_df.iterrows():
        try:
            all_days.append(interpolate_day(row['date'],
                                            row['temp_mean'],
                                            row['temp_min'],
                                            row['temp_max'],
                                            row['solar_noon_time']))
        except Exception as e:
            print(f"Skipping {row.get('Date')}: {e}")

    return pd.concat(all_days, ignore_index=True)

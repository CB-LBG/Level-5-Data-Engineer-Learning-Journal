import pandas as pd
import numpy as np
import sys
import os

# Force local import logic
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from pipeline import utils
except ImportError:
    from . import utils


def interpolate_day(date, temp_mean, min_temp, max_temp, solar_noon_time):
    times = pd.date_range(start=date, periods=1440, freq="min")

    # 1. Safe parsing of inputs
    try:
        temp_mean = float(temp_mean)
        max_temp = float(max_temp)
        min_temp = float(min_temp)
    except (ValueError, TypeError):
        # If temp data is missing, we can't model the day
        raise ValueError("Missing temperature data")

    minutes = np.arange(1440)

    # 2. Get Peak Time (Critical Fix)
    noon_mins = utils.get_mins_from_time(solar_noon_time)

    if noon_mins is None:
        # FALLBACK: If we don't know when solar noon is, assume 12:00 PM (720 mins)
        noon_mins = 720

    t_peak = noon_mins + 120  # Peak is usually 2 hours after solar noon

    # 3. Calculate Curve
    amplitude = (max_temp - min_temp) / 2
    temps = temp_mean + amplitude * np.sin((minutes - t_peak) * np.pi / 720)

    df = pd.DataFrame({"datetime": times, "estimated_temp": temps})
    df['estimated_temp'] = round(df['estimated_temp'], 3)
    return df


def generate_minute_estimates(final_df):
    all_days = []
    print(f"   -> Resampling {len(final_df)} days...")

    for i, row in final_df.iterrows():
        try:
            daily_df = interpolate_day(
                row['date'],
                row['temp_mean'],
                row['temp_min'],
                row['temp_max'],
                row['solar_noon_time']
            )
            all_days.append(daily_df)
        except Exception as e:
            # FIX: Use row['date'] so we actually see the date in the error log
            date_val = row.get('date', f"Row {i}")
            print(f"   [Warning] Skipping {date_val}: {e}")

    if not all_days:
        print("   [Error] No days were processed successfully. Returning empty DataFrame.")
        return pd.DataFrame()

    return pd.concat(all_days, ignore_index=True)

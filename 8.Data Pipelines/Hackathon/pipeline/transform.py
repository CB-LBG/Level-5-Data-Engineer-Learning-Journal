import pandas as pd


def transform_weather(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms weather data:
    1. Converts Date column to datetime objects.
    2. Calculates T_avg and Amplitude (A) for the sinusoidal model.
    """
    try:
        # Ensure Date is datetime for merging logic
        # Using errors='coerce' handles unexpected formats by setting them to NaT
        df['Date'] = pd.to_datetime(df['Date'])

        # FEATURE ENGINEERING
        # We calculate these here using Vectorization (fast) rather than
        # inside the resample loop (slow).

        # T_avg = (Max + Min) / 2
        df['T_avg'] = (df['Max Temp'] + df['Min Temp']) / 2

        # Amplitude (A) = (Max - Min) / 2
        df['Amplitude'] = (df['Max Temp'] - df['Min Temp']) / 2

        print(f"   -> Transformed Weather Data: {len(df)} rows processed.")
        return df

    except KeyError as e:
        print(f"   [Error] Missing column in Weather Data: {e}")
        raise
    except Exception as e:
        print(f"   [Error] Failed to transform Weather Data: {e}")
        raise


def transform_astronomy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms astronomical data:
    1. Converts Date column to datetime objects.
    2. Ensures consistency for the merge.
    """
    try:
        df['Date'] = pd.to_datetime(df['Date'])

        # Optional: If you need to perform calculations on Sunrise/Sunset
        # you would convert them to datetime/timedelta here.
        # For now, we just need the Date to align.

        print(f"   -> Transformed Astronomical Data: {len(df)} rows processed.")
        return df

    except Exception as e:
        print(f"   [Error] Failed to transform Astronomical Data: {e}")
        raise

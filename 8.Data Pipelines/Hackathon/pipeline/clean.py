import datetime
import pandas as pd

# --- ROBUST IMPORT BLOCK ---
# This allows the script to run directly AND as part of the pipeline
try:
    # Try relative import first (works when running main.py)
    from .utils import drop_empty_rows, clean_str_columns, remove_degrees
except ImportError:
    # Fallback to absolute import (works when running this file directly)
    from utils import drop_empty_rows, clean_str_columns, remove_degrees


# ---------------------------

def clean_edinburgh(edinburgh_excel, edinburgh_columns):
    """Clean Edinburgh weather data from Excel files."""

    # 1. Create a list to store dataframes (Faster than repeated concat)
    all_frames = []

    for key in edinburgh_excel.keys():
        # Extract Year/Month from sheet name (e.g. "1201" -> 2012, 1)
        try:
            year = 2000 + int(key[:2])
            month = int(key[2:])
            print(f"   -> Processing Edinburgh: {year}-{month:02d}")
        except ValueError:
            print(f"   [Warning] Skipping sheet with invalid name: {key}")
            continue

        df = edinburgh_excel[key]

        # Drop header noise (Rows 0 and 1)
        df = df.drop([0, 1]).reset_index(drop=True)
        df = drop_empty_rows(df)

        # Ensure column count matches before assigning
        if len(df.columns) == len(edinburgh_columns):
            df.columns = edinburgh_columns
        else:
            print(
                f"   [Warning] Sheet {key} has {len(df.columns)} columns, expected {len(edinburgh_columns)}. Skipping.")
            continue

        # Convert 'day' column to actual Date
        # Safety: Ensure 'day' is numeric before converting
        df['day_num'] = pd.to_numeric(df['date'], errors='coerce')
        df = df.dropna(subset=['day_num'])  # Drop rows where day isn't a number

        # Create the actual date object
        df['date'] = df['day_num'].apply(lambda x: datetime.date(year, month, int(x)))
        df = df.drop(columns=['day_num'])  # cleanup temp column

        # Clean string columns
        for col in df.columns:
            # Apply cleaning to all object (string) columns
            if df[col].dtype == 'object':
                df[col] = df[col].apply(clean_str_columns)

        # Clean degree symbols specific to Edinburgh
        for col in ['sunrise', 'sunset', 'solar_noon_time']:
            if col in df.columns:
                df[col] = df[col].apply(remove_degrees)

        all_frames.append(df)

    # Combine all sheets at once
    if all_frames:
        return pd.concat(all_frames, ignore_index=True)
    else:
        return pd.DataFrame(columns=edinburgh_columns)


def clean_strathspey(strathspey_excel, strathspey_columns):
    """Clean Strathspey weather data from Excel files."""

    all_frames = []

    for key in strathspey_excel.keys():
        try:
            year = 2000 + int(key[:2])
            month = int(key[2:])
            print(f"   -> Processing Strathspey: {year}-{month:02d}")
        except ValueError:
            continue

        df = strathspey_excel[key]

        # Drop header noise (Rows 0-4 usually for Strathspey)
        df = df.drop(list(range(5))).reset_index(drop=True)
        df = drop_empty_rows(df)

        if len(df.columns) == len(strathspey_columns):
            df.columns = strathspey_columns
        else:
            print(f"   [Warning] Sheet {key} mismatch. Skipping.")
            continue

        # Convert Date
        df['day_num'] = pd.to_numeric(df['date'], errors='coerce')
        df = df.dropna(subset=['day_num'])
        df['date'] = df['day_num'].apply(lambda x: datetime.date(year, month, int(x)))
        df = df.drop(columns=['day_num'])

        # Clean Strings
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(clean_str_columns)

        all_frames.append(df)

    if all_frames:
        return pd.concat(all_frames, ignore_index=True)
    else:
        return pd.DataFrame(columns=strathspey_columns)

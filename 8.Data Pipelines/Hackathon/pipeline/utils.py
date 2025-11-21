import re
import unicodedata
import pandas as pd
import numpy as np
import datetime

def remove_degrees(value):
    if pd.isna(value):
        return value
    value = str(value)
    return value.split(' ')[0].replace('°', '').strip()

def drop_empty_rows(df, thresh=0.5):
    return df.dropna(thresh=int(thresh * len(df.columns)))

def clean_str_columns(value):
    if pd.isna(value) or value == "":
        return None
    value = str(value)
    value = re.sub('−', '-', value)
    value = re.sub(r'[^:().\-°\d]', '', value) # Allow dots for decimals
    value = re.sub(' +', ' ', unicodedata.normalize('NFKD', value)).strip()
    if value in ['Restofnight', 'Rest of night', 'nan']:
        return None
    return value

def combine(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(df1, df2, on="date", how="inner")
    return merged

def get_mins_from_time(time_val):
    """
    Robustly converts time to minutes from midnight.
    Handles: "12:30", "12:30:00", datetime.time(12, 30)
    """
    if pd.isna(time_val) or time_val == "nan":
        return None

    # Case 1: It's already a python datetime.time object (Pandas often does this)
    if isinstance(time_val, datetime.time):
        return time_val.hour * 60 + time_val.minute

    # Case 2: It's a string
    if isinstance(time_val, str):
        try:
            # Cleanup just in case
            time_val = time_val.strip()
            if ':' not in time_val:
                return None
            parts = time_val.split(':')
            return 60 * int(parts[0]) + int(parts[1])
        except (ValueError, IndexError):
            return None

    return None

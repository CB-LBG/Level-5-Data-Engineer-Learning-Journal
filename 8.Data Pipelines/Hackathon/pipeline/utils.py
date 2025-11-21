import re
import unicodedata
import pandas as pd

def remove_degrees(value):
    return value.split(' ')[0]

def drop_empty_rows(df, thresh=0.5):
    """ Drop rows with more than 50% NaN values. """
    return df.dropna(thresh=int(thresh * len(df.columns)))

def clean_str_columns(value):
    value = str(value)
    # fix minus sign
    value = re.sub('−', '-', value)
    # remove unwanted characters
    value = re.sub('[^:()-°\d]', '', value)
    # remove extra spaces
    value = re.sub(' +', ' ', unicodedata.normalize('NFKD', value)).strip()
    if value in ['Restofnight', 'Rest of night']:
        return None
    return value

def combine(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Combine two dataframes on the 'date' columns"""
    merged = pd.merge(df1, df2, on="date", how="inner")
    return merged

def get_mins_from_time(time):
    return 60*int(time.split(':')[0]) + int(time.split(':')[1])

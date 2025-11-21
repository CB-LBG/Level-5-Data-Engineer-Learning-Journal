import datetime
import pandas as pd
from pipeline.utils import drop_empty_rows, clean_str_columns, remove_degrees

def clean_edinburgh(edinburgh_excel, edinburgh_columns):
    """Clean Edinburgh weather data from Excel files."""
    for i, key in enumerate(edinburgh_excel.keys()):
        year = 2000 + int(key[:2])
        month = int(key[2:])
        print(f"Processing data for {year}-{month:02d}")
        df = edinburgh_excel[key]
        # drop unnecessary rows
        df = df.drop([0, 1], ).reset_index(drop=True)
        df = drop_empty_rows(df)
        df.columns = edinburgh_columns
        # convert day to date
        df['date'] = pd.to_datetime(df['date'].apply(lambda x: datetime.date(year, month, x)))
        for col in df.columns:
            if isinstance(df[col][0], str):
                df[col] = df[col].apply(clean_str_columns)
        for col in ['sunrise', 'sunset', 'solar_noon_time']:
            df[col] = df[col].apply(remove_degrees)
        if i == 0:
            edinburgh_df = df
        else:
            edinburgh_df = pd.concat([edinburgh_df, df], ignore_index=True)
    return edinburgh_df

def clean_strathspey(strathspey_excel, strathspey_columns):
    for i, key in enumerate(strathspey_excel.keys()):
        year = 2000 + int(key[:2])
        month = int(key[2:])
        print(f"Processing data for {year}-{month:02d}")
        df = strathspey_excel[key]
        # drop unnecessary rows
        df = df.drop([x for x in range(5)], ).reset_index(drop=True)
        df = drop_empty_rows(df)
        df.columns = strathspey_columns
        # convert day to date
        df['date'] = pd.to_datetime(df['date'].apply(lambda x: datetime.date(year, month, x)))
        for col in df.columns:
            if isinstance(df[col][0], str):
                df[col] = df[col].apply(clean_str_columns)
        if i == 0:
            strathspey_df = df
        else:
            strathspey_df = pd.concat([strathspey_df, df], ignore_index=True)
    return strathspey_df

import pandas as pd


def merge_datasets(weather_df: pd.DataFrame, astro_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges weather and astronomical data on the 'Date' column.
    """
    try:
        print("   -> Merging datasets...")

        # Merge on 'Date'
        # how='inner' ensures we only keep days when we have BOTH weather and sun data.
        merged_df = pd.merge(weather_df, astro_df, on='Date', how='inner')

        # Data Quality Check
        row_count = len(merged_df)
        if row_count != 366:
            print(f"   [Warning] Expected 366 rows (Leap Year 2012), but resulting merged data has {row_count}.")

        print(f"   -> Merge Complete. Combined shape: {merged_df.shape}")
        return merged_df

    except KeyError:
        print("   [Error] Merge failed. Ensure both DataFrames have a 'Date' column.")
        raise
    except Exception as e:
        print(f"   [Error] Merge failed: {e}")
        raise

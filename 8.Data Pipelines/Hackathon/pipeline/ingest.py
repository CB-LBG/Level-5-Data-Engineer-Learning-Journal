import pandas as pd
from typing import Dict

def load_sheets(file_path: str) -> Dict[str, pd.DataFrame]:
    """Load all sheets from an Excel file as a dictionary of DataFrames."""
    try:
        return pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return {}

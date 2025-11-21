import pandas as pd
from pipeline import ingest, clean, utils, resample
from config.config import EDINBURGH_PATH, EDINBURGH_COLUMNS, STRATHSPEY_PATH, STRATHSPEY_COLUMNS

def main():
    edin_raw = ingest.load_sheets(EDINBURGH_PATH)
    strat_raw = ingest.load_sheets(STRATHSPEY_PATH)
    
    print("Processing Edinburgh data...")
    edin_clean = clean.clean_edinburgh(edin_raw, EDINBURGH_COLUMNS)
    print("Processing Strathspey data...")
    strat_clean = clean.clean_strathspey(strat_raw, STRATHSPEY_COLUMNS)
    
    final_df = utils.combine(edin_clean, strat_clean)
    final_df.to_csv("output/merged_summary.csv", index=False)
    
    minute_df = resample.generate_minute_estimates(final_df)
    minute_df.to_csv("output/minute_level_estimates.csv", index=False)

    print("Pipeline complete. Outputs saved to 'output' folder.")

if __name__ == "__main__":
    main()

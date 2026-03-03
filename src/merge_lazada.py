import pandas as pd
import glob
import os

def merge_and_label():
    # 1. Grab all Lazada CSVs
    files = glob.glob('data/raw/lazada_*.csv')
    all_data = []

    for f in files:
        df = pd.read_csv(f)
        
        # Extract deity or product name from filename (e.g., 'lazada_wessuwan.csv' -> 'wessuwan')
        category = os.path.basename(f).replace('lazada_', '').replace('.csv', '')
        df['search_keyword'] = category
        
        all_data.append(df)

    # 2. Combine all into one master file
    master_df = pd.concat(all_data, ignore_index=True)
    master_df.to_csv('data/raw/lazada_master_raw.csv', index=False)
    print(f"✅ Merged {len(files)} files into lazada_master_raw.csv")

if __name__ == "__main__":
    merge_and_label()
import pandas as pd
from pytrends.request import TrendReq
import time

# 1. Simplified Initialization
# Removed the custom 'retries' argument to avoid the urllib3 conflict
pytrends = TrendReq(hl='th-TH', tz=420)

# 2. Define Groups (Max 5 per group)
groups = {
    "deities": ["ท้าวเวสสุวรรณ", "พระแม่ลักษมี", "พระพิฆเนศ", "พญานาค"],
    "products": ["สีเสื้อมงคล 2569", "วอลเปเปอร์สายมู", "เบอร์มงคล", "กำไลสายมู"],
    "travel": ["คำชะโนด", "วัดเจดีย์ไอ้ไข่", "วัดสมานรัตนาราม", "พระแม่ลักษมี เกษร", "วัดดอยคำ"]
}

def fetch_all_groups():
    all_dfs = []
    
    for category, kw_list in groups.items():
        print(f"🚀 Fetching group: {category}...")
        try:
            # Request data
            pytrends.build_payload(kw_list, timeframe='today 12-m', geo='TH')
            df = pytrends.interest_over_time()
            
            if not df.empty:
                # Clean and keep only the keyword columns
                df = df.drop(columns=['isPartial'])
                all_dfs.append(df)
                print(f"✅ Group '{category}' successful.")
            
            # Sleep to avoid 429 "Too Many Requests" errors
            time.sleep(10) 
            
        except Exception as e:
            print(f"❌ Error in {category}: {e}")

    # 3. Combine and Save
    if all_dfs:
        master_df = pd.concat(all_dfs, axis=1)
        output_file = 'data/raw/mutelu_master_trends.csv'
        master_df.to_csv(output_file)
        print(f"\n✨ DONE! File saved to: {output_file}")
    else:
        print("😭 No data collected. Try using a VPN or waiting 15 minutes.")

if __name__ == "__main__":
    fetch_all_groups()
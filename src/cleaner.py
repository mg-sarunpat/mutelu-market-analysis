import pandas as pd
import re

def clean_data():
    # 1. Load the messy master file
    df = pd.read_csv('data/raw/lazada_master_raw.csv')

    # 2. Keep only the needed columns and rename them
    cols_to_keep = {
        'RfADt': 'product_name',
        'ooOxS': 'price',
        '_1cEkb': 'sold_count',
        'oa6ri': 'location',
        'search_keyword': 'category'
    }
    
    # Filter to keep only these columns (if they exist)
    df = df[list(cols_to_keep.keys())].rename(columns=cols_to_keep)

    # 3. Wipe out "Cat Food" and Junk using Inclusion & Exclusion filters
    # Keywords to KEEP (Inclusion)
    mu_keywords = (
        'พระ|มงคล|สายมู|ท้าวเวส|ลักษมี|พิฆเนศ|นาค|กำไล|เบอร์|เสื้อ|วอลเปเปอร์|'
        'อาร์ตทอย|art toy|ยันต์|หินมงคล|ปี่เซียะ|สาริกา|เชือกแดง|แก้ชง|โชค'
    )
    # Keywords to DROP (Exclusion)
    exclude_keywords = 'อาหารแมว|อาหารสุนัข|กรงแมว|ทรายแมว'

    # Apply Inclusion
    df = df[df['product_name'].str.contains(mu_keywords, case=False, na=False)]
    # Apply Exclusion
    df = df[~df['product_name'].str.contains(exclude_keywords, case=False, na=False)]

    # 4. Fix the Price (Remove ฿ and commas, handle ranges)
    def clean_price(price_str):
        if pd.isna(price_str): return 0.0
        price_str = str(price_str).replace('฿', '').replace(',', '').strip()
        if '-' in price_str:
            parts = [float(p) for p in price_str.split('-')]
            return sum(parts) / len(parts)
        try:
            return float(price_str)
        except:
            return 0.0

    df['price'] = df['price'].apply(clean_price)

    # 5. Fix Sold Count (Handle "k" and missing values)
    def clean_sold(sold_str):
        if pd.isna(sold_str): return 0
        sold_str = str(sold_str).lower().replace('ขายแล้ว', '').replace('ชิ้น', '').strip()
        
        # Regex to find numbers (handles 3.1 or 3,100)
        match = re.search(r"(\d+\.?\d*)", sold_str)
        if not match: return 0
        
        num = float(match.group(1))
        if 'k' in sold_str:
            return int(num * 1000)
        return int(num)

    df['sold_count'] = df['sold_count'].apply(clean_sold)

    # 6. Save the Clean Dataset
    output_path = 'data/processed/mutelu_market_clean.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✨ Cleaning Complete!")
    print(f"📉 Rows before: {len(pd.read_csv('data/raw/lazada_master_raw.csv'))}")
    print(f"📈 Rows after (No junk): {len(df)}")
    print(f"📁 Saved to: {output_path}")

if __name__ == "__main__":
    clean_data()